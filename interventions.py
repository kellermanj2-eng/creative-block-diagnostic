"""
interventions.py – One concrete, specific exercise per creative-block category.

Each entry maps a category key to an Intervention with:
  name        : display name of the block type
  description : what this block actually is (diagnostic framing)
  exercise    : ONE specific, concrete exercise — no vague advice

FATIGUE NOTE: The fatigue intervention deliberately avoids toxic positivity,
"push through it," and motivational language. It treats tiredness as a
normal, valid state and offers a minimal-effort way to stay connected to
the work without demanding output.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Intervention:
    name: str
    description: str
    exercise: str


INTERVENTIONS: dict[str, Intervention] = {
    "possibility": Intervention(
        name="Possibility Paralysis",
        description=(
            "You're not stuck because you have no ideas — you're stuck because "
            "you have too many, or because the space of options feels so open that "
            "no single direction feels justified. The project hasn't failed yet, so "
            "every choice feels reversible and therefore optional. The block is the "
            "openness itself."
        ),
        exercise=(
            "Forced-Constraints Sprint: Set a timer for 20 minutes. Before it starts, "
            "write down three arbitrary restrictions for this session — e.g. 'only use "
            "two colors,' 'the piece must reference something from my kitchen,' 'every "
            "sentence must be under eight words.' The constraints must be specific enough "
            "to rule out options. Then work only within those rules until the timer ends. "
            "Don't evaluate the output afterward — the goal is to discover what emerges "
            "when the possibility space is artificially narrowed, not to produce something "
            "you'll keep."
        ),
    ),
    "purpose": Intervention(
        name="Purpose Void",
        description=(
            "The work feels hollow before it's finished — you can't picture who it's for, "
            "why it should exist, or what it would add. This isn't imposter syndrome about "
            "your skill; it's a missing answer to 'so what?' The creative energy drains "
            "because you can't find a reason to direct it."
        ),
        exercise=(
            "One Real Person Letter: Identify one specific, real person — not a demographic, "
            "not 'my audience,' but an actual human being you know or have met — who would "
            "genuinely benefit from encountering this work. Write a single paragraph (not to "
            "publish, just for yourself) addressed to them: what you're making, why you think "
            "they specifically would care, and one concrete thing you want them to feel or know "
            "afterward. Pin that paragraph somewhere visible while you work. If you can't name "
            "anyone, that's the real constraint to solve first — make it for yourself, and write "
            "the paragraph to a past version of you."
        ),
    ),
    "skill_gap": Intervention(
        name="Execution Gap",
        description=(
            "The idea is clear — maybe vivid — but the moment you try to render it, the gap "
            "between what you imagine and what your hands produce is discouraging. This isn't "
            "a problem with vision; it's a mismatch between the skill level the idea demands "
            "and the skill level you currently have. The block is the distance, not the direction."
        ),
        exercise=(
            "Steal One Technique: Find one finished work — in any medium — that solves the "
            "specific execution problem you're stuck on. Study it for ten minutes: how exactly "
            "did they do the thing you can't do yet? Then spend 30 minutes doing nothing but "
            "reverse-engineering that one technique in isolation, completely detached from your "
            "own project. Don't try to apply it to your work yet. Practice the technique on "
            "throwaway material until you can produce even a rough version of it on demand. "
            "Then return to your project with that one tool available."
        ),
    ),
    "fatigue": Intervention(
        name="Creative Depletion",
        description=(
            "Your creative energy is genuinely low right now — not as a metaphor, but as a "
            "real, physical and mental state. The work isn't the problem; output just costs "
            "more than you have available at the moment. This kind of block doesn't respond "
            "to motivation or discipline. Trying harder tends to make it worse."
        ),
        exercise=(
            "Minimum Footprint Session: Give yourself explicit permission to produce nothing "
            "today. Instead, spend 15 minutes doing only passive contact with your project: "
            "read through existing notes or drafts without editing, look at reference images "
            "you've collected, or re-read a few sentences of something that originally inspired "
            "the work. No output required. When the 15 minutes end, stop — even if something "
            "starts to feel interesting. The goal is to stay loosely connected to the work "
            "without spending anything you don't have."
        ),
    ),
    "judgment": Intervention(
        name="Judgment Block",
        description=(
            "The obstacle isn't the work itself — it's the imagined audience watching you make "
            "it. You're editing before you've created, or abandoning things before they're "
            "finished because they'll reveal something unflattering. Perfectionism here is "
            "usually fear in disguise: the unfinished thing can't be judged yet."
        ),
        exercise=(
            "Make It Bad on Purpose: Set a timer for 15 minutes. Your only goal is to produce "
            "the worst possible version of whatever you're working on — the most clichéd, "
            "embarrassing, overwrought, or technically sloppy version you can manage. Commit "
            "to it. Don't accidentally make it good. When the timer ends, look at what you "
            "made: notice that you still made something, that the world didn't end, and that "
            "some of it is probably less bad than you aimed for. You're not keeping this — "
            "the point is to practice completing a thing while the inner critic is aimed at "
            "a target it can't hurt."
        ),
    ),
}
