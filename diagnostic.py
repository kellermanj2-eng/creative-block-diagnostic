"""
diagnostic.py – Pure scoring logic. No I/O, no network calls.

Public API
----------
diagnose(answers: dict[str, int]) -> DiagnosisResult

  answers  – maps question id (e.g. "q1") to the chosen option index (0-9).
             Missing questions are simply skipped; partial submissions work.

  returns  – DiagnosisResult with:
               primary   : str   – category with highest weighted score
               secondary : str | None  – second category if it scores
                                         within 25 % of the primary
               scores    : dict[str, float]  – raw scores for all categories
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from questions import CATEGORIES, QUESTIONS


@dataclass
class DiagnosisResult:
    primary: str
    secondary: Optional[str]
    scores: dict[str, float] = field(default_factory=dict)


# Index questions by id for O(1) lookup.
_QUESTION_MAP = {q["id"]: q for q in QUESTIONS}

# Threshold: secondary is reported only if it reaches this fraction of primary.
_SECONDARY_THRESHOLD = 0.75  # i.e. within 25 % of primary


def diagnose(answers: dict[str, int]) -> DiagnosisResult:
    """
    Score the submitted answers and return a DiagnosisResult.

    Parameters
    ----------
    answers : dict[str, int]
        Maps question id to chosen option index (0-based).
        Extra keys that don't match any question id are silently ignored.
        Option indices outside the valid range for a question are skipped.

    Returns
    -------
    DiagnosisResult
    """
    scores: dict[str, float] = {cat: 0.0 for cat in CATEGORIES}

    for qid, option_idx in answers.items():
        question = _QUESTION_MAP.get(qid)
        if question is None:
            continue  # unknown question id – ignore

        options = question["options"]
        if not isinstance(option_idx, int) or not (0 <= option_idx < len(options)):
            continue  # out-of-range index – ignore

        chosen_weights = options[option_idx]["weights"]
        for category, points in chosen_weights.items():
            if category in scores:
                scores[category] += points

    return _rank(scores)


def _rank(scores: dict[str, float]) -> DiagnosisResult:
    """
    Given raw category scores, determine primary and optional secondary.

    Rules
    -----
    - Primary   : category with the highest score.
    - Secondary : the next highest category, but ONLY if its score is at least
                  `_SECONDARY_THRESHOLD` × primary_score (i.e. within 25 %).
    - Ties       : broken alphabetically (deterministic ordering).
    - All-zero  : falls back to "possibility" as a safe default so callers
                  never receive an empty primary.
    """
    # Sort descending by score, then ascending by name to break ties.
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))

    primary_name, primary_score = ranked[0]

    # All-zero edge case: every answer was skipped or no answers provided.
    if primary_score == 0:
        return DiagnosisResult(primary="possibility", secondary=None, scores=scores)

    secondary_name: Optional[str] = None
    if len(ranked) > 1:
        second_name, second_score = ranked[1]
        if second_score >= _SECONDARY_THRESHOLD * primary_score:
            secondary_name = second_name

    return DiagnosisResult(
        primary=primary_name,
        secondary=secondary_name,
        scores=scores,
    )
