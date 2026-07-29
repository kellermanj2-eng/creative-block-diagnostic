"""
test_personas.py – Synthetic persona evaluation suite.

Runs 25 persona profiles through the full diagnose() pipeline to verify
that the scoring logic produces sensible, consistent results across a
range of real-world creative-block patterns.

Profiles
--------
 3+ clear-cut profiles per category (one-category dominant answers)
 5  ambiguous / mixed profiles (two-way ties or noisy real-world patterns)
 2  edge-case profiles (partial submission, all-same answer)

Usage
-----
    python test_personas.py            # full output
    python test_personas.py --quiet    # only failures + final summary

Exit code: 0 if all assertions pass, 1 otherwise.
"""

from __future__ import annotations

import sys
import math
from dataclasses import dataclass, field
from typing import Optional

# ── Import the app's scoring engine ──────────────────────────────────────────
sys.path.insert(0, ".")
from diagnostic import diagnose, DiagnosisResult
import questions as qmod

QUIET = "--quiet" in sys.argv

# ── Helpers ───────────────────────────────────────────────────────────────────

def best_option(q: dict, category: str) -> int:
    """Return the option index with the highest weight for *category*."""
    return max(
        range(len(q["options"])),
        key=lambda i: q["options"][i]["weights"].get(category, 0),
    )


def build_sweep(category: str) -> dict[str, int]:
    """Answer every question with the option that most strongly signals *category*."""
    return {q["id"]: best_option(q, category) for q in qmod.QUESTIONS}


def build_partial_sweep(category: str, question_indices: list[int]) -> dict[str, int]:
    """Answer only the listed question indices (0-based) with the best option for *category*."""
    answers = {}
    for i in question_indices:
        q = qmod.QUESTIONS[i]
        answers[q["id"]] = best_option(q, category)
    return answers


def build_mixed(
    cat_a: str, weight_a: int, cat_b: str, weight_b: int
) -> dict[str, int]:
    """
    Answer *weight_a* questions with cat_a's best option and *weight_b*
    questions with cat_b's best option (always totalling ≤ 10).
    """
    assert weight_a + weight_b <= len(qmod.QUESTIONS)
    answers = {}
    qs = qmod.QUESTIONS
    for i in range(weight_a):
        q = qs[i]
        answers[q["id"]] = best_option(q, cat_a)
    for i in range(weight_a, weight_a + weight_b):
        q = qs[i]
        answers[q["id"]] = best_option(q, cat_b)
    return answers


# ── Persona definitions ───────────────────────────────────────────────────────

@dataclass
class Persona:
    name: str
    answers: dict[str, int]
    expected_primary: str
    # If None, any secondary (including None) is accepted.
    expected_secondary: Optional[str] = None
    check_secondary: bool = False
    # Expected confidence bucket: "high" | "moderate" | "mixed" | None (any)
    expected_confidence_bucket: Optional[str] = None
    description: str = ""


def conf_bucket(label: str) -> str:
    if label.startswith("high"):
        return "high"
    if label.startswith("moderate"):
        return "moderate"
    return "mixed"


PERSONAS: list[Persona] = [

    # ── Clear-cut possibility ─────────────────────────────────────────────────
    Persona(
        name="Possibility – full sweep",
        answers=build_sweep("possibility"),
        expected_primary="possibility",
        expected_confidence_bucket="high",
        description="All 10 answers point to possibility block.",
    ),
    Persona(
        name="Possibility – 8/10 strong",
        answers={**build_sweep("possibility"),
                 **{qmod.QUESTIONS[8]["id"]: best_option(qmod.QUESTIONS[8], "judgment"),
                    qmod.QUESTIONS[9]["id"]: best_option(qmod.QUESTIONS[9], "judgment")}},
        expected_primary="possibility",
        expected_confidence_bucket=None,
        description="8 possibility answers, 2 mild judgment noise.",
    ),
    Persona(
        name="Possibility – overwhelmed ideator",
        # Q1 opt0 (possibility:3/purpose:2), Q2 opt0 (possibility:4),
        # Q4 opt0 (possibility:4), Q5 opt0 (possibility:4/judgment:1),
        # Q7 opt0 (possibility:4), Q9 opt0 (possibility:4),
        # Q10 opt0 (possibility:4)
        answers={
            "q1": 0, "q2": 0, "q3": 0, "q4": 0, "q5": 0,
            "q6": 0, "q7": 0, "q9": 0, "q10": 0,
        },
        expected_primary="possibility",
        description="Real-world pattern: spreads thin, can't commit.",
    ),

    # ── Clear-cut purpose ─────────────────────────────────────────────────────
    Persona(
        name="Purpose – full sweep",
        answers=build_sweep("purpose"),
        expected_primary="purpose",
        expected_confidence_bucket="high",
        description="All 10 answers point to purpose block.",
    ),
    Persona(
        name="Purpose – 8/10 strong",
        answers={**build_sweep("purpose"),
                 **{qmod.QUESTIONS[0]["id"]: best_option(qmod.QUESTIONS[0], "possibility"),
                    qmod.QUESTIONS[1]["id"]: best_option(qmod.QUESTIONS[1], "possibility")}},
        expected_primary="purpose",
        description="8 purpose answers, 2 possibility noise.",
    ),
    Persona(
        name="Purpose – meaning vacuum",
        answers={
            "q2": 1,   # purpose:3, fatigue:2 — everything feels pointless
            "q3": 1,   # purpose:4 — emptiness when imagining completion
            "q4": 1,   # purpose:4 — 'this won't matter to anyone'
            "q6": 1,   # purpose:4 — hollow when seeing others' work
            "q8": 1,   # purpose:4 — indifferent to last completed work
            "q10": 1,  # purpose:4 — nothing if project never finished
        },
        expected_primary="purpose",
        description="Textbook purpose block: 'why bother?' at every turn.",
    ),

    # ── Clear-cut skill_gap ───────────────────────────────────────────────────
    Persona(
        name="Skill gap – full sweep",
        answers=build_sweep("skill_gap"),
        expected_primary="skill_gap",
        expected_confidence_bucket="high",
        description="All 10 answers point to skill_gap block.",
    ),
    Persona(
        name="Skill gap – 8/10 strong",
        answers={**build_sweep("skill_gap"),
                 **{qmod.QUESTIONS[6]["id"]: best_option(qmod.QUESTIONS[6], "fatigue"),
                    qmod.QUESTIONS[7]["id"]: best_option(qmod.QUESTIONS[7], "fatigue")}},
        expected_primary="skill_gap",
        description="8 skill_gap answers, 2 fatigue noise.",
    ),
    Persona(
        name="Skill gap – craft frustration",
        answers={
            "q1": 2,   # skill_gap:4 — clear vision, can't execute
            "q3": 2,   # skill_gap:4 — can see finish but can't get there
            "q5": 2,   # skill_gap:4 — frustrating attempts hit walls
            "q6": 2,   # skill_gap:4 — inspired but intimidated by technique
            "q9": 2,   # skill_gap:4 — breaks focus on specific technical wall
        },
        expected_primary="skill_gap",
        description="The craft/execution gap persona: sees ideal, can't reach it.",
    ),

    # ── Clear-cut fatigue ─────────────────────────────────────────────────────
    Persona(
        name="Fatigue – full sweep",
        answers=build_sweep("fatigue"),
        expected_primary="fatigue",
        expected_confidence_bucket="high",
        description="All 10 answers point to fatigue block.",
    ),
    Persona(
        name="Fatigue – 8/10 strong",
        answers={**build_sweep("fatigue"),
                 **{qmod.QUESTIONS[2]["id"]: best_option(qmod.QUESTIONS[2], "purpose"),
                    qmod.QUESTIONS[3]["id"]: best_option(qmod.QUESTIONS[3], "purpose")}},
        expected_primary="fatigue",
        description="8 fatigue answers, 2 purpose noise.",
    ),
    Persona(
        name="Fatigue – going through motions",
        answers={
            "q1": 3,   # fatigue:4 — brain won't cooperate
            "q2": 3,   # fatigue:4 — can't muster energy
            "q4": 3,   # fatigue:3, judgment:1 — running on empty
            "q7": 3,   # fatigue:4 — intends to work, rests instead
            "q9": 3,   # fatigue:4 — physical tiredness breaks focus
            "q10": 3,  # fatigue:4 — honestly, a relief to stop
        },
        expected_primary="fatigue",
        description="Depleted creator: rest > guilt loop at every question.",
    ),

    # ── Clear-cut judgment ────────────────────────────────────────────────────
    Persona(
        name="Judgment – full sweep",
        answers=build_sweep("judgment"),
        expected_primary="judgment",
        expected_confidence_bucket="high",
        description="All 10 answers point to judgment block.",
    ),
    Persona(
        name="Judgment – 8/10 strong",
        answers={**build_sweep("judgment"),
                 **{qmod.QUESTIONS[4]["id"]: best_option(qmod.QUESTIONS[4], "possibility"),
                    qmod.QUESTIONS[5]["id"]: best_option(qmod.QUESTIONS[5], "possibility")}},
        expected_primary="judgment",
        description="8 judgment answers, 2 possibility noise.",
    ),
    Persona(
        name="Judgment – perfectionist hider",
        answers={
            "q1": 4,   # judgment:4 — starts, deletes, not good enough
            "q3": 4,   # judgment:4 — anxiety about being judged
            "q5": 4,   # judgment:4 — produces privately, won't commit
            "q8": 4,   # judgment:4 — embarrassed by last completed work
            "q9": 4,   # judgment:4 — rereads, decides not good enough
            "q10": 4,  # judgment:4 — secretly relieved unfinished
        },
        expected_primary="judgment",
        description="Classic perfectionist: makes things, hides them, deletes them.",
    ),

    # ── Ambiguous / mixed profiles ────────────────────────────────────────────
    Persona(
        name="Mixed – purpose/fatigue 5-5 split",
        answers=build_mixed("purpose", 5, "fatigue", 5),
        expected_primary=None,  # accept either
        expected_confidence_bucket=None,
        description="Even split between purpose and fatigue; top-2 should be those two.",
    ),
    Persona(
        name="Mixed – possibility/judgment 5-5 split",
        answers=build_mixed("possibility", 5, "judgment", 5),
        expected_primary=None,
        expected_confidence_bucket=None,
        description="Even split between possibility and judgment.",
    ),
    Persona(
        name="Mixed – skill_gap/judgment 6-4 split",
        answers=build_mixed("skill_gap", 6, "judgment", 4),
        expected_primary="skill_gap",
        expected_confidence_bucket=None,
        description="Slight skill_gap lean; judgment close behind.",
    ),
    Persona(
        name="Mixed – burnout blend (fatigue + purpose noise)",
        answers={
            "q1": 3,   # fatigue:4
            "q2": 1,   # purpose:3, fatigue:2
            "q4": 3,   # fatigue:3, judgment:1
            "q5": 3,   # fatigue:4, purpose:1
            "q7": 3,   # fatigue:4
            "q8": 3,   # fatigue:4, purpose:1
            "q10": 3,  # fatigue:4
        },
        expected_primary="fatigue",
        description="Real-world burnout: fatigue dominates with purpose undertone.",
    ),
    Persona(
        name="Mixed – scattered creative (possibility noise)",
        answers={
            "q1": 0,   # possibility:3, purpose:2
            "q2": 0,   # possibility:4
            "q4": 0,   # possibility:4
            "q5": 4,   # judgment:4, possibility:1
            "q7": 4,   # judgment:4, possibility:1
            "q9": 0,   # possibility:4
        },
        expected_primary=None,
        description="Half possibility, half judgment — common ambiguous case.",
    ),

    # ── Edge cases ────────────────────────────────────────────────────────────
    Persona(
        name="Edge – partial submission (3 questions only)",
        answers=build_partial_sweep("judgment", [0, 3, 8]),
        expected_primary="judgment",
        description="Only 3 questions answered; primary should still be judgment.",
    ),
    Persona(
        name="Edge – all answers the same index (option 2 = skill_gap)",
        answers={q["id"]: 2 for q in qmod.QUESTIONS},
        expected_primary="skill_gap",
        description="Every question answered with option index 2 (skill_gap-weighted).",
    ),
    Persona(
        name="Edge – single question answered",
        answers={"q4": 4},  # judgment:4
        expected_primary="judgment",
        description="Minimal valid submission: one question, strong judgment signal.",
    ),
    Persona(
        name="Edge – 3-way tie (possibility + judgment + fatigue)",
        answers={
            **build_partial_sweep("possibility", [0, 1, 2]),
            **build_partial_sweep("judgment", [3, 4, 5]),
            **build_partial_sweep("fatigue", [6, 7, 8]),
        },
        expected_primary=None,
        description="3-way close race; entropy will be high; should not crash.",
    ),
]


# ── Run evaluations ───────────────────────────────────────────────────────────

passed = 0
failed = 0
failures: list[str] = []

sep = "-" * 64
print(sep)
print("Creative Block Diagnostic — Persona Evaluation Suite")
print(f"{len(PERSONAS)} personas across 5 categories")
print(sep)

for i, p in enumerate(PERSONAS, 1):
    result = diagnose(p.answers)

    ok = True
    reasons: list[str] = []

    # Check primary (None = accept any non-empty)
    if p.expected_primary is not None:
        if result.primary != p.expected_primary:
            ok = False
            reasons.append(
                f"primary={result.primary!r} (expected {p.expected_primary!r})"
            )
    else:
        if not result.primary:
            ok = False
            reasons.append("primary is empty")

    # Check secondary if explicitly required
    if p.check_secondary and p.expected_secondary is not None:
        if result.secondary != p.expected_secondary:
            ok = False
            reasons.append(
                f"secondary={result.secondary!r} (expected {p.expected_secondary!r})"
            )

    # Check confidence bucket
    if p.expected_confidence_bucket is not None:
        bucket = conf_bucket(result.confidence)
        if bucket != p.expected_confidence_bucket:
            ok = False
            reasons.append(
                f"confidence={result.confidence!r} (expected bucket "
                f"{p.expected_confidence_bucket!r})"
            )

    # Invariants: scores dict completeness + confidence_score range
    cats = set(qmod.CATEGORIES)
    if set(result.scores.keys()) != cats:
        ok = False
        reasons.append(f"scores keys mismatch: {set(result.scores.keys())}")

    if not (0.0 <= result.confidence_score <= 1.0):
        ok = False
        reasons.append(
            f"confidence_score out of range: {result.confidence_score}"
        )

    status = "PASS" if ok else "FAIL"
    if ok:
        passed += 1
    else:
        failed += 1
        failures.append(f"[{i:02d}] {p.name}")

    if not QUIET or not ok:
        top2 = sorted(result.scores.items(), key=lambda kv: -kv[1])[:2]
        top2_str = ", ".join(f"{k}={v:.1f}" for k, v in top2)
        print(
            f"  [{status}] #{i:02d} {p.name}\n"
            f"         primary={result.primary!r}  "
            f"secondary={result.secondary!r}  "
            f"confidence={result.confidence!r} ({result.confidence_score:.3f})\n"
            f"         top-2 scores: {top2_str}"
        )
        if reasons:
            for r in reasons:
                print(f"         !! {r}")

print()
print(sep)
print(f"Results: {passed} passed, {failed} failed out of {len(PERSONAS)}")
if failures:
    print("Failing personas:")
    for f in failures:
        print(f"  {f}")
    print(sep)
    sys.exit(1)
else:
    print("All personas passed.")
    print(sep)
    sys.exit(0)
