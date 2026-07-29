"""
test_diagnosis.py – Minimal pytest suite for the diagnostic engine.

Covers the core contract so that `pytest` reports green PASSED out of the box.
The full 25-persona evaluation suite can be run separately with:
    python eval_personas.py
"""

import sys
sys.path.insert(0, ".")

import pytest
from diagnostic import diagnose, _confidence_from_scores
from interventions import INTERVENTIONS
from questions import CATEGORIES


def test_single_category_sweeps():
    """Highest-weight sweep for each category should produce that category as primary."""
    import questions as qmod
    for cat in CATEGORIES:
        answers = {
            q["id"]: max(
                range(len(q["options"])),
                key=lambda i, c=cat: q["options"][i]["weights"].get(c, 0),
            )
            for q in qmod.QUESTIONS
        }
        r = diagnose(answers)
        assert r.primary == cat, f"sweep {cat}: got {r.primary}, scores={r.scores}"


def test_empty_input_fallback():
    """Empty answers should not raise and should return a valid result."""
    r = diagnose({})
    assert r.primary  # non-empty string
    assert r.confidence == "mixed signals"
    assert r.contributing_answers == []


def test_interventions_completeness():
    """Every category must have a name, description, and exercise."""
    for cat in CATEGORIES:
        iv = INTERVENTIONS[cat]
        assert iv.name, f"missing name: {cat}"
        assert iv.description, f"missing description: {cat}"
        assert iv.exercise, f"missing exercise: {cat}"


def test_high_confidence_single_category():
    cs, label = _confidence_from_scores(
        {"possibility": 20, "purpose": 0, "skill_gap": 0, "fatigue": 0, "judgment": 0}
    )
    assert cs == 0.0
    assert label == "high confidence"


def test_mixed_signals_even_split():
    # Even split across all 8 categories → maximum entropy → mixed signals
    from questions import CATEGORIES
    cs, label = _confidence_from_scores({cat: 4 for cat in CATEGORIES})
    assert abs(cs - 1.0) < 1e-6
    assert label == "mixed signals"
