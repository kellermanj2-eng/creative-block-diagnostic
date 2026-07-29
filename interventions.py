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
    "comparison": Intervention(
        name="Comparison Trap",
        description=(
            "The block isn't your work — it's the gap between your work and the best work "
            "you've been consuming. You've calibrated your taste against polished, finished "
            "output from people who've been doing this longer, and your drafts look bad by "
            "that standard. The more you consume, the worse your own output looks in "
            "comparison. The creative energy drains not from internal judgement but from "
            "an external reference point that was never a fair comparison."
        ),
        exercise=(
            "Input Fast + Audience of One: For the next 48 hours, stop consuming work in "
            "your medium entirely — no feeds, no portfolios, no 'inspiration.' Then identify "
            "one specific person — not a demographic, not 'people who like this kind of thing' "
            "— who would benefit from your version of this work. Write one sentence about what "
            "only you can bring to this project that the work you've been comparing yourself "
            "to doesn't have: a specific experience, a specific perspective, a specific "
            "constraint. Work only toward that person and that sentence for your next session. "
            "Don't look at anyone else's work until the session ends."
        ),
    ),
    "imposter_syndrome": Intervention(
        name="Imposter Syndrome",
        description=(
            "The block isn't a skill gap — you have functional ability. The block is the "
            "persistent feeling that you're fraudulently occupying a space you haven't earned, "
            "that your past successes were luck, and that continuing to make work risks "
            "exposing you. Unlike Judgment Block, which fears the work being bad, Imposter "
            "Syndrome fears the person being illegitimate. The distinction matters: improving "
            "your skills doesn't resolve it, because legitimacy isn't the real question."
        ),
        exercise=(
            "Evidence Inventory: Get a blank page. In ten minutes, list every piece of "
            "evidence that you have done this before — finished projects, things you've "
            "shipped, moments where your contribution mattered, skills you've demonstrably "
            "developed. Don't filter for significance. Then write one sentence that separates "
            "credential from contribution: 'I don't need permission to make this because...' "
            "and complete it with something that is true about your experience or perspective, "
            "not your title or qualifications. Keep that sentence somewhere visible. The goal "
            "isn't to feel confident — it's to notice that the evidence for legitimacy already "
            "exists and you've been discounting it."
        ),
    ),
    "perfectionism": Intervention(
        name="Perfectionism Block",
        description=(
            "The block is an internal standard that moves. You can execute the work — "
            "the problem is that your bar for 'good enough to proceed' or 'good enough to "
            "finish' keeps rising as you approach it. Unlike Judgment Block, the fear isn't "
            "primarily about how others will receive the work; it's about not being able to "
            "tolerate output that falls short of an ideal. The unfinished or un-started state "
            "feels safer because it protects the ideal from being tested."
        ),
        exercise=(
            "Time-Box + Pre-Set Criteria: Before your next session, write down exactly three "
            "criteria that would make this piece of work 'done' — specific, observable things, "
            "not feelings. Set a timer for 45 minutes. Work only toward those three criteria. "
            "When the timer ends, evaluate only against those three criteria — not against how "
            "the work compares to your ideal or to other work. If all three are met, the work "
            "is done for this session. If not, identify which one remains and set a new 20-minute "
            "block for that specific criterion only. The goal is to replace 'good enough' — "
            "which is a feeling — with a concrete, pre-committed definition that can actually "
            "be reached."
        ),
    ),
}
