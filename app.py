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

from diagnostic import diagnose
from interventions import INTERVENTIONS
from llm_client import personalize_exercise

app = Flask(__name__)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def index():
    """Serve the quiz single-page UI."""
    from questions import QUESTIONS
    return render_template("index.html", questions=QUESTIONS)


@app.post("/diagnose")
def diagnose_route():
    """Score answers and return diagnosis + exercise."""
    body = request.get_json(silent=True) or {}

    raw_answers: dict = body.get("answers", {})
    context: str = str(body.get("context", "") or "").strip()

    # Coerce answer values to int (JSON numbers arrive as int already, but
    # be defensive in case they arrive as strings from some clients).
    answers: dict[str, int] = {}
    for qid, val in raw_answers.items():
        try:
            answers[str(qid)] = int(val)
        except (TypeError, ValueError):
            pass  # skip malformed values

    result = diagnose(answers, user_context=context)

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
