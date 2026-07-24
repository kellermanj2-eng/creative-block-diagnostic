"""
questions.py – Quiz questions and their weighted answer options.

Each question has 5 answer options (index 0–4).
Each option carries a `weights` dict mapping category keys to point values.
Categories: possibility | purpose | skill_gap | fatigue | judgment

Weights are non-negative integers; an option can weight multiple categories
(blocks overlap), but one category usually dominates.
"""

from typing import TypedDict


class Option(TypedDict):
    text: str
    weights: dict[str, int]  # category -> points


class Question(TypedDict):
    id: str
    text: str
    options: list[Option]


CATEGORIES: tuple[str, ...] = (
    "possibility",
    "purpose",
    "skill_gap",
    "fatigue",
    "judgment",
)

QUESTIONS: list[Question] = [
    {
        "id": "q1",
        "text": "When you sit down to work on your project, what happens first?",
        "options": [
            {
                "text": "I open a blank document and stare at it — I have no idea where to start.",
                "weights": {"possibility": 3, "purpose": 2},
            },
            {
                "text": "I start something but quickly wonder if anyone will actually care about it.",
                "weights": {"purpose": 4, "judgment": 1},
            },
            {
                "text": "I have a clear vision but the moment I try to execute it, I fall short.",
                "weights": {"skill_gap": 4},
            },
            {
                "text": "I stare at the screen but I'm mostly just tired — my brain won't cooperate.",
                "weights": {"fatigue": 4},
            },
            {
                "text": "I start, then delete everything because it's not good enough yet.",
                "weights": {"judgment": 4, "possibility": 1},
            },
        ],
    },
    {
        "id": "q2",
        "text": "How would you describe the ideas you currently have?",
        "options": [
            {
                "text": "Too many — I can't choose between them and none feel right.",
                "weights": {"possibility": 4},
            },
            {
                "text": "Almost none — everything feels pointless before I've even started.",
                "weights": {"purpose": 3, "fatigue": 2},
            },
            {
                "text": "One solid idea, but I genuinely lack the skills to bring it to life.",
                "weights": {"skill_gap": 4},
            },
            {
                "text": "Ideas exist but I can't muster the energy to develop them.",
                "weights": {"fatigue": 4},
            },
            {
                "text": "I have ideas but they all seem embarrassing or not original enough.",
                "weights": {"judgment": 4, "purpose": 1},
            },
        ],
    },
    {
        "id": "q3",
        "text": "When you imagine finishing this project, what feeling dominates?",
        "options": [
            {
                "text": "Uncertainty — I'm not sure which direction I even want to finish in.",
                "weights": {"possibility": 4, "purpose": 1},
            },
            {
                "text": "Emptiness — I can't picture who would want it or why it matters.",
                "weights": {"purpose": 4},
            },
            {
                "text": "Frustration — I can see the finished thing clearly but don't know how to get there.",
                "weights": {"skill_gap": 4},
            },
            {
                "text": "Dread — the effort required feels like more than I can give right now.",
                "weights": {"fatigue": 4},
            },
            {
                "text": "Anxiety — I worry that once it's done, people will judge it (and me).",
                "weights": {"judgment": 4, "purpose": 1},
            },
        ],
    },
    {
        "id": "q4",
        "text": "What does your inner critic most often say?",
        "options": [
            {
                "text": "'You're spreading yourself too thin — commit to something already.'",
                "weights": {"possibility": 4},
            },
            {
                "text": "'This won't matter to anyone. Why bother?'",
                "weights": {"purpose": 4},
            },
            {
                "text": "'You're not skilled enough to pull this off.'",
                "weights": {"skill_gap": 4},
            },
            {
                "text": "'You're running on empty — you don't have what it takes right now.'",
                "weights": {"fatigue": 3, "judgment": 1},
            },
            {
                "text": "'Even if you finish it, everyone will see how mediocre it is.'",
                "weights": {"judgment": 4},
            },
        ],
    },
    {
        "id": "q5",
        "text": "What has your creative work looked like over the past few weeks?",
        "options": [
            {
                "text": "Starting lots of things, finishing none — I keep pivoting to something new.",
                "weights": {"possibility": 4, "judgment": 1},
            },
            {
                "text": "Sparse. I struggle to justify the time when I'm not sure the work has a point.",
                "weights": {"purpose": 4},
            },
            {
                "text": "Frustrating attempts that fall short of what I imagined — I keep hitting walls.",
                "weights": {"skill_gap": 4},
            },
            {
                "text": "Very little — I've been going through the motions when I do anything at all.",
                "weights": {"fatigue": 4, "purpose": 1},
            },
            {
                "text": "Stop-start. I produce things privately but hesitate to show or commit to them.",
                "weights": {"judgment": 4, "possibility": 1},
            },
        ],
    },
    {
        "id": "q6",
        "text": "When you get feedback or look at someone else's finished work, how do you feel?",
        "options": [
            {
                "text": "Envious of their focus — I wish I could just pick one thing and stick with it.",
                "weights": {"possibility": 4},
            },
            {
                "text": "Hollow. Their work matters; mine doesn't seem to.",
                "weights": {"purpose": 4},
            },
            {
                "text": "Inspired but intimidated — I can see the technique I'm missing.",
                "weights": {"skill_gap": 4},
            },
            {
                "text": "Numb. I can barely engage with other people's work right now.",
                "weights": {"fatigue": 4},
            },
            {
                "text": "Defensive or deflated — I compare and always come up short.",
                "weights": {"judgment": 4, "purpose": 1},
            },
        ],
    },
    {
        "id": "q7",
        "text": "If you had a completely free afternoon with no obligations, what would happen with your project?",
        "options": [
            {
                "text": "I'd probably spend it researching new directions instead of actually making anything.",
                "weights": {"possibility": 4},
            },
            {
                "text": "I'd avoid it. The free time would just remind me I don't know why I'm doing this.",
                "weights": {"purpose": 4, "fatigue": 1},
            },
            {
                "text": "I'd work on it, hit a wall quickly, and spend the rest of the time frustrated.",
                "weights": {"skill_gap": 4},
            },
            {
                "text": "I'd intend to work, then rest instead — and feel guilty about it.",
                "weights": {"fatigue": 4},
            },
            {
                "text": "I'd tinker but not commit anything. It wouldn't feel ready to be seen — even by me.",
                "weights": {"judgment": 4, "possibility": 1},
            },
        ],
    },
    {
        "id": "q8",
        "text": "How do you feel about the last creative thing you actually completed?",
        "options": [
            {
                "text": "Like it was the wrong choice — I should have gone in a different direction.",
                "weights": {"possibility": 4, "judgment": 1},
            },
            {
                "text": "Indifferent. I finished it but can't remember why it seemed worth doing.",
                "weights": {"purpose": 4},
            },
            {
                "text": "Disappointed — it doesn't match what I had in my head.",
                "weights": {"skill_gap": 4},
            },
            {
                "text": "Relieved it's over more than proud of it. The process drained me.",
                "weights": {"fatigue": 4, "purpose": 1},
            },
            {
                "text": "I'm already embarrassed by it. I notice everything that's wrong with it.",
                "weights": {"judgment": 4},
            },
        ],
    },
    {
        "id": "q9",
        "text": "What usually breaks your focus mid-session?",
        "options": [
            {
                "text": "A better idea — I get distracted by a new direction that seems more promising.",
                "weights": {"possibility": 4},
            },
            {
                "text": "A creeping sense that this isn't going anywhere meaningful.",
                "weights": {"purpose": 4, "judgment": 1},
            },
            {
                "text": "Hitting a specific technical obstacle I don't know how to get past.",
                "weights": {"skill_gap": 4},
            },
            {
                "text": "Physical tiredness or mental fog — I can feel my capacity running out.",
                "weights": {"fatigue": 4},
            },
            {
                "text": "Rereading or reviewing what I've done and deciding it's not good enough.",
                "weights": {"judgment": 4, "possibility": 1},
            },
        ],
    },
    {
        "id": "q10",
        "text": "What would it mean to you if this project were never finished?",
        "options": [
            {
                "text": "Fine, honestly — I'd probably just start something else. I always do.",
                "weights": {"possibility": 4},
            },
            {
                "text": "Nothing. I already suspect it wouldn't have mattered.",
                "weights": {"purpose": 4},
            },
            {
                "text": "Frustrating — I know it could be good, I just can't get it there.",
                "weights": {"skill_gap": 4, "judgment": 1},
            },
            {
                "text": "Honestly, a relief. I don't have the reserves for it right now.",
                "weights": {"fatigue": 4},
            },
            {
                "text": "Secretly relieved — it can't be judged if it's never done.",
                "weights": {"judgment": 4, "purpose": 1},
            },
        ],
    },
]
