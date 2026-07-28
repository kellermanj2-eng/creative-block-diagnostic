"""
app.py – Flask application entry point.

Routes
------
GET  /           Serve the quiz page (templates/index.html)
POST /diagnose   Accept JSON body, return diagnosis JSON

POST /diagnose – request body
{
    "answers": {
        "q1": 0,   // option index 0-4 for each question
        "q2": 3,
        ...
    },
    "context": "optional free-text about the user's specific situation"
}

POST /diagnose – response body
{
    "primary": "judgment",
    "primary_name": "Judgment Block",
    "primary_description": "...",
    "exercise": "...",
    "personalization": "...",        // empty string when watsonx disabled/no context
    "secondary": "fatigue",          // null when no secondary qualifies
    "secondary_name": "Creative Depletion",
    "scores": { "possibility": 4, "purpose": 1, ... },
    "context_influence": {           // empty object when no context boost was applied
        "fatigue": 0.32,
        "judgment": 0.16
    }
}
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()  # must run before any module reads env vars

from flask import Flask, jsonify, render_template, request  # noqa: E402

from diagnostic import diagnose, get_followup_questions
from interventions import INTERVENTIONS
from llm_client import personalize_exercise

app = Flask(__name__)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def index():
    """Serve the quiz single-page UI."""
    from questions import QUESTIONS
    return render_template("index.html", questions=QUESTIONS)


def _coerce_answers(raw: dict) -> dict[str, int]:
    """Coerce a raw answers dict to {str: int}, dropping malformed values."""
    out: dict[str, int] = {}
    for qid, val in raw.items():
        try:
            out[str(qid)] = int(val)
        except (TypeError, ValueError):
            pass
    return out


@app.post("/diagnose")
def diagnose_route():
    """Score answers and return diagnosis + exercise.

    Two-round protocol
    ------------------
    Round 1 – body contains ``answers`` (and optional ``context``).
              If confidence is "mixed signals" AND follow-up questions exist,
              returns ``needs_followup: true`` plus the follow-up questions.
              No exercise is returned in this case.

    Round 2 – body additionally contains ``followup_answers``.
              Runs full scoring with both answer sets, returns the final
              result with ``needs_followup: false``.

    If round-1 confidence is already good (not "mixed signals"), returns
    the final result immediately with ``needs_followup: false``.
    """
    body = request.get_json(silent=True) or {}

    answers = _coerce_answers(body.get("answers", {}))
    context: str = str(body.get("context", "") or "").strip()

    raw_followup: dict | None = body.get("followup_answers")
    followup_answers: dict[str, int] | None = None
    if raw_followup is not None:
        # Round 2: followup_answers key present (may be empty dict → treated
        # as no follow-up, scores unchanged — spec requirement).
        followup_answers = _coerce_answers(raw_followup)

    result = diagnose(answers, user_context=context, followup_answers=followup_answers)

    # Round 1 check: only trigger follow-up when the client hasn't already
    # sent followup_answers (i.e. raw_followup is None, not just empty).
    if raw_followup is None and result.confidence == "mixed signals":
        followup_qs = get_followup_questions(result)
        if followup_qs:
            return jsonify(
                {
                    "needs_followup": True,
                    "followup_questions": followup_qs,
                    "primary": result.primary,
                    "scores": result.scores,
                    "confidence": result.confidence,
                    "confidence_score": result.confidence_score,
                }
            )

    # Final result (round 2, or round 1 where confidence is already good).
    primary_intervention = INTERVENTIONS[result.primary]
    exercise_text = primary_intervention.exercise

    personalization = personalize_exercise(
        exercise=exercise_text,
        context=context,
        block_name=primary_intervention.name,
    )

    secondary_name: str | None = None
    if result.secondary:
        secondary_name = INTERVENTIONS[result.secondary].name

    return jsonify(
        {
            "needs_followup": False,
            "primary": result.primary,
            "primary_name": primary_intervention.name,
            "primary_description": primary_intervention.description,
            "exercise": exercise_text,
            "personalization": personalization,
            "secondary": result.secondary,
            "secondary_name": secondary_name,
            "scores": result.scores,
            "confidence": result.confidence,
            "confidence_score": result.confidence_score,
            "contributing_answers": result.contributing_answers,
            "context_influence": result.context_influence,
        }
    )


# ── Dev server ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, port=5000)
