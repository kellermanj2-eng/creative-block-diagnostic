"""
diagnostic.py – Pure scoring logic. No I/O, no network calls.

Public API
----------
diagnose(answers: dict[str, int], user_context: str = "") -> DiagnosisResult

  answers      – maps question id (e.g. "q1") to the chosen option index (0-9).
                 Missing questions are simply skipped; partial submissions work.
  user_context – optional free-text description of the user's creative situation.
                 When provided and watsonx is enabled/available, a small secondary
                 signal (≤ 20% of one quiz question's weight) is added to the
                 quiz-derived scores.  Entirely skipped when watsonx is
                 disabled, unavailable, or the call fails — pure quiz scoring
                 is always the fallback.

  returns  – DiagnosisResult with:
               primary              : str   – category with highest weighted score
               secondary            : str | None  – second category if it scores
                                                    within 25 % of the primary
               scores               : dict[str, float]  – raw scores for all categories
               confidence           : str   – "high confidence" | "moderate confidence"
                                             | "mixed signals"
               confidence_score     : float – 0.0 (all signal) → 1.0 (evenly spread)
               contributing_answers : list[dict] – top 2-3 questions that most drove
                                                   the primary category, each with
                                                   {qid, question_text, weight}
               context_influence    : dict  – per-category boost applied from watsonx
                                             context analysis (empty when not applied)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from questions import CATEGORIES, FOLLOWUP_QUESTIONS, QUESTIONS


@dataclass
class DiagnosisResult:
    primary: str
    secondary: Optional[str]
    scores: dict[str, float] = field(default_factory=dict)
    confidence: str = "mixed signals"
    confidence_score: float = 1.0
    contributing_answers: list[dict] = field(default_factory=list)
    context_influence: dict[str, float] = field(default_factory=dict)


# Index questions by id for O(1) lookup.
_QUESTION_MAP = {q["id"]: q for q in QUESTIONS}

# Threshold: secondary is reported only if it reaches this fraction of primary.
_SECONDARY_THRESHOLD = 0.75  # i.e. within 25 % of primary

# Context-boost cap: LLM scores are 0-10; normalised to at most 20% of one
# quiz question's typical max weight (4 pts).  Max boost per category = 0.8 pts.
_CONTEXT_MAX_BOOST = 0.8   # points added per category at LLM score = 10

# Number of categories — used for entropy normalisation.
_N_CATEGORIES = len(CATEGORIES)  # 5

# Maximum possible Shannon entropy for _N_CATEGORIES equally-weighted categories.
_MAX_ENTROPY = math.log(_N_CATEGORIES)  # log(5) ≈ 1.609

# Confidence label thresholds (normalised entropy, 0-1).
_HIGH_CONF_THRESHOLD     = 0.40   # normalised entropy ≤ 0.40 → high confidence
_MODERATE_CONF_THRESHOLD = 0.70   # normalised entropy ≤ 0.70 → moderate confidence
                                   # above 0.70             → mixed signals

# How many top contributing questions to surface.
_TOP_N_CONTRIBUTORS = 3


# Index follow-up questions by id for O(1) lookup during scoring.
_FOLLOWUP_QUESTION_MAP: dict[str, dict] = {
    q["id"]: q
    for questions in FOLLOWUP_QUESTIONS.values()
    for q in questions
}


def get_followup_questions(result: DiagnosisResult) -> list[dict]:
    """
    Return 1–2 follow-up questions that disambiguate the top-2 categories
    when confidence is "mixed signals", or [] otherwise.
    """
    if result.confidence != "mixed signals":
        return []

    ranked = sorted(result.scores.items(), key=lambda kv: (-kv[1], kv[0]))
    if len(ranked) < 2 or ranked[0][1] == 0:
        return []

    top_two = frozenset({ranked[0][0], ranked[1][0]})
    return list(FOLLOWUP_QUESTIONS.get(top_two, []))


def diagnose(
    answers: dict[str, int],
    user_context: str = "",
    followup_answers: dict[str, int] | None = None,
) -> DiagnosisResult:
    """
    Score the submitted answers and return a DiagnosisResult.

    Parameters
    ----------
    answers : dict[str, int]
        Maps question id to chosen option index (0-based).
        Extra keys that don't match any question id are silently ignored.
        Option indices outside the valid range for a question are skipped.
    user_context : str, optional
        Free-text description of the user's creative situation.  When non-empty
        and watsonx is available, a small secondary adjustment (capped at
        _CONTEXT_MAX_BOOST pts per category) is applied on top of the quiz
        scores before ranking.  Safe to omit; falls back to pure quiz scoring.
    followup_answers : dict[str, int] | None, optional
        Maps follow-up question id to chosen option index.  Weights are
        accumulated on top of the primary quiz scores before re-ranking.
        An empty dict is treated as no follow-up (scores unchanged).

    Returns
    -------
    DiagnosisResult
    """
    scores: dict[str, float] = {cat: 0.0 for cat in CATEGORIES}

    # Per-question contribution tracking: list of (qid, question_text, category, points)
    # One entry per (question, category) pair that received > 0 weight.
    contributions: list[tuple[str, str, str, float]] = []

    # Score primary quiz answers.
    all_answers: list[tuple[dict[str, int], dict[str, dict]]] = [
        (answers, _QUESTION_MAP),
    ]
    # Append follow-up answers (if any) using their own question map.
    if followup_answers:
        all_answers.append((followup_answers, _FOLLOWUP_QUESTION_MAP))

    for answer_set, question_map in all_answers:
        for qid, option_idx in answer_set.items():
            question = question_map.get(qid)
            if question is None:
                continue  # unknown question id – ignore

            options = question["options"]
            if not isinstance(option_idx, int) or not (0 <= option_idx < len(options)):
                continue  # out-of-range index – ignore

            chosen_weights = options[option_idx]["weights"]
            for category, points in chosen_weights.items():
                if category in scores:
                    scores[category] += points
                    contributions.append((qid, question["text"], category, float(points)))

    # ── Optional context boost ────────────────────────────────────────────────
    context_influence: dict[str, float] = {}
    user_context = (user_context or "").strip()
    if user_context:
        try:
            from llm_client import analyze_context_for_categories
            raw_llm_scores = analyze_context_for_categories(user_context)
        except Exception:  # noqa: BLE001
            raw_llm_scores = None

        if raw_llm_scores is not None:
            for cat, llm_score in raw_llm_scores.items():
                if cat in scores:
                    # Normalise 0-10 LLM score to [0, _CONTEXT_MAX_BOOST] pts.
                    boost = round((llm_score / 10.0) * _CONTEXT_MAX_BOOST, 4)
                    if boost > 0:
                        scores[cat] += boost
                        context_influence[cat] = boost

    return _rank(scores, contributions, context_influence)


def _confidence_from_scores(scores: dict[str, float]) -> tuple[float, str]:
    """
    Compute a normalised Shannon entropy (0-1) from raw category scores
    and return (confidence_score, confidence_label).

    0.0 = all weight in one category (maximum confidence).
    1.0 = perfectly even across all categories (minimum confidence / mixed signals).
    """
    total = sum(scores.values())
    if total == 0:
        # No signal at all — treat as maximum uncertainty.
        return 1.0, "mixed signals"

    # Probability distribution over categories.
    probs = [s / total for s in scores.values() if s > 0]

    # Shannon entropy H = -Σ p·log(p).
    entropy = -sum(p * math.log(p) for p in probs)

    # Normalise to [0, 1] relative to the maximum possible entropy.
    # abs() eliminates -0.0 from floating-point arithmetic on single-category inputs.
    normalised = abs(entropy / _MAX_ENTROPY)

    if normalised <= _HIGH_CONF_THRESHOLD:
        label = "high confidence"
    elif normalised <= _MODERATE_CONF_THRESHOLD:
        label = "moderate confidence"
    else:
        label = "mixed signals"

    return round(normalised, 4), label


def _top_contributors(
    primary: str,
    contributions: list[tuple[str, str, str, float]],
) -> list[dict]:
    """
    From all per-question weight contributions, return the top
    _TOP_N_CONTRIBUTORS entries that fed into *primary*, as a list of
    {qid, question_text, weight} dicts.

    Ties are broken by qid (alphabetical) for determinism.
    """
    # Filter to primary category only, then aggregate per question.
    agg: dict[str, dict] = {}
    for qid, qtext, category, points in contributions:
        if category != primary:
            continue
        if qid not in agg:
            agg[qid] = {"qid": qid, "question_text": qtext, "weight": 0.0}
        agg[qid]["weight"] += points

    # Sort by weight descending, then qid ascending for tie-breaking.
    ranked = sorted(agg.values(), key=lambda d: (-d["weight"], d["qid"]))
    return ranked[:_TOP_N_CONTRIBUTORS]


def _rank(
    scores: dict[str, float],
    contributions: list[tuple[str, str, str, float]],
    context_influence: dict[str, float] | None = None,
) -> DiagnosisResult:
    """
    Given raw category scores and per-question contributions, determine
    primary, secondary, confidence, and contributing_answers.

    Rules
    -----
    - Primary   : category with the highest score.
    - Secondary : the next highest category, but ONLY if its score is at least
                  `_SECONDARY_THRESHOLD` × primary_score (i.e. within 25 %).
    - Ties       : broken alphabetically (deterministic ordering).
    - All-zero  : falls back to "possibility" as a safe default so callers
                  never receive an empty primary.
    """
    if context_influence is None:
        context_influence = {}

    # Sort descending by score, then ascending by name to break ties.
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))

    primary_name, primary_score = ranked[0]

    # All-zero edge case: every answer was skipped or no answers provided.
    if primary_score == 0:
        return DiagnosisResult(
            primary="possibility",
            secondary=None,
            scores=scores,
            confidence="mixed signals",
            confidence_score=1.0,
            contributing_answers=[],
            context_influence={},
        )

    secondary_name: Optional[str] = None
    if len(ranked) > 1:
        second_name, second_score = ranked[1]
        if second_score >= _SECONDARY_THRESHOLD * primary_score:
            secondary_name = second_name

    confidence_score, confidence_label = _confidence_from_scores(scores)
    top_contributors = _top_contributors(primary_name, contributions)

    return DiagnosisResult(
        primary=primary_name,
        secondary=secondary_name,
        scores=scores,
        confidence=confidence_label,
        confidence_score=confidence_score,
        contributing_answers=top_contributors,
        context_influence=context_influence,
    )
