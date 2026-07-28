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


# ── Follow-up question bank ───────────────────────────────────────────────────
#
# Keys are frozensets of two category names (order-independent lookup).
# Values: 1–2 question dicts, same schema as QUESTIONS.
# Weights strongly favour one or the other of the paired categories;
# the remaining three receive minimal weight.
# Weight scale: 0–4 (same as QUESTIONS).

FOLLOWUP_QUESTIONS: dict[frozenset, list[Question]] = {
    frozenset({"possibility", "judgment"}): [
        {
            "id": "fq_possibility_judgment_1",
            "text": "When you abandon a creative direction, what is the main reason?",
            "options": [
                {
                    "text": "A genuinely better idea came along and I had to follow it.",
                    "weights": {"possibility": 4, "judgment": 0, "purpose": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "The idea felt too risky — I worried it would look foolish or amateurish.",
                    "weights": {"judgment": 4, "possibility": 0, "purpose": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I never really commit — keeping options open feels safer than finishing.",
                    "weights": {"possibility": 3, "judgment": 1, "purpose": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I commit but then delete it — the output never meets my standard.",
                    "weights": {"judgment": 3, "possibility": 1, "purpose": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I lose interest quickly — no single idea grips me long enough.",
                    "weights": {"possibility": 4, "judgment": 0, "purpose": 1, "skill_gap": 0, "fatigue": 0},
                },
            ],
        },
        {
            "id": "fq_possibility_judgment_2",
            "text": "You've committed to one idea and started. What happens next?",
            "options": [
                {
                    "text": "I immediately second-guess whether it was the right choice.",
                    "weights": {"possibility": 4, "judgment": 1, "purpose": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I make progress, but keep re-editing because nothing feels good enough.",
                    "weights": {"judgment": 4, "possibility": 0, "purpose": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I make steady progress without major doubt.",
                    "weights": {"possibility": 0, "judgment": 0, "purpose": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I finish a draft but hide it — too embarrassed to share or commit.",
                    "weights": {"judgment": 4, "possibility": 0, "purpose": 0, "skill_gap": 0, "fatigue": 1},
                },
                {
                    "text": "Another idea grabs me and I abandon the original one.",
                    "weights": {"possibility": 4, "judgment": 0, "purpose": 0, "skill_gap": 0, "fatigue": 0},
                },
            ],
        },
    ],
    frozenset({"possibility", "purpose"}): [
        {
            "id": "fq_possibility_purpose_1",
            "text": "When you can't start your creative work, the feeling is closest to:",
            "options": [
                {
                    "text": "Paralysis from too many directions — I don't know which way to go.",
                    "weights": {"possibility": 4, "purpose": 0, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "Emptiness — I don't know why I'd go any direction at all.",
                    "weights": {"purpose": 4, "possibility": 0, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "Restlessness — I want to make something, just nothing I land on feels right.",
                    "weights": {"possibility": 3, "purpose": 1, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "Meaninglessness — even a great idea wouldn't feel worth pursuing right now.",
                    "weights": {"purpose": 4, "possibility": 0, "judgment": 0, "skill_gap": 0, "fatigue": 1},
                },
                {
                    "text": "Indecision — I have options but none of them feel personally meaningful.",
                    "weights": {"possibility": 2, "purpose": 2, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
            ],
        },
    ],
    frozenset({"purpose", "fatigue"}): [
        {
            "id": "fq_purpose_fatigue_1",
            "text": "If you had two full weeks off to do nothing but creative projects, you would most likely:",
            "options": [
                {
                    "text": "Still not make much — time off wouldn't fix the feeling that it doesn't matter.",
                    "weights": {"purpose": 4, "fatigue": 0, "possibility": 0, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "Recharge and come back energised — I just need rest.",
                    "weights": {"fatigue": 4, "purpose": 0, "possibility": 0, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "Start several things with excitement, then quietly abandon them all.",
                    "weights": {"purpose": 2, "fatigue": 1, "possibility": 1, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "Make progress, but it still wouldn't feel meaningful or satisfying.",
                    "weights": {"purpose": 3, "fatigue": 1, "possibility": 0, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "Spend the first week sleeping, then tentatively start again.",
                    "weights": {"fatigue": 4, "purpose": 1, "possibility": 0, "skill_gap": 0, "judgment": 0},
                },
            ],
        },
        {
            "id": "fq_purpose_fatigue_2",
            "text": "The last time you tried to work creatively, what stopped you?",
            "options": [
                {
                    "text": "Exhaustion — my body and mind were too depleted to produce anything.",
                    "weights": {"fatigue": 4, "purpose": 0, "possibility": 0, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "A feeling the project wasn't worth the energy, even when I had it.",
                    "weights": {"purpose": 4, "fatigue": 0, "possibility": 0, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "Both — I was tired AND the work felt pointless.",
                    "weights": {"purpose": 2, "fatigue": 2, "possibility": 0, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "I actually did work — it's been going okay lately.",
                    "weights": {"purpose": 0, "fatigue": 0, "possibility": 0, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "Low-grade exhaustion that made even small decisions feel overwhelming.",
                    "weights": {"fatigue": 3, "purpose": 1, "possibility": 0, "skill_gap": 0, "judgment": 0},
                },
            ],
        },
    ],
    frozenset({"fatigue", "judgment"}): [
        {
            "id": "fq_fatigue_judgment_1",
            "text": "After a creative session, how do you usually feel?",
            "options": [
                {
                    "text": "Drained and flat — the session used up more than it gave back.",
                    "weights": {"fatigue": 4, "judgment": 0, "possibility": 0, "skill_gap": 0, "purpose": 0},
                },
                {
                    "text": "Critical of everything I made — it never reaches the standard I want.",
                    "weights": {"judgment": 4, "fatigue": 0, "possibility": 0, "skill_gap": 0, "purpose": 0},
                },
                {
                    "text": "Tired AND disappointed in the output.",
                    "weights": {"fatigue": 2, "judgment": 2, "possibility": 0, "skill_gap": 0, "purpose": 0},
                },
                {
                    "text": "Relieved it's over, regardless of how it went.",
                    "weights": {"fatigue": 3, "judgment": 1, "possibility": 0, "skill_gap": 0, "purpose": 0},
                },
                {
                    "text": "Deflated — I can see clearly how far it falls short of what I imagined.",
                    "weights": {"judgment": 3, "fatigue": 1, "possibility": 0, "skill_gap": 0, "purpose": 0},
                },
            ],
        },
    ],
    frozenset({"purpose", "judgment"}): [
        {
            "id": "fq_purpose_judgment_1",
            "text": "When you think about sharing your creative work, the main fear is:",
            "options": [
                {
                    "text": "That people will think less of me — I dread being judged.",
                    "weights": {"judgment": 4, "purpose": 0, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "That no one will care — the work just won't matter to anyone.",
                    "weights": {"purpose": 4, "judgment": 0, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "Both — afraid it'll be criticised AND that the criticism will be right.",
                    "weights": {"judgment": 2, "purpose": 2, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "That I'm wasting time on something irrelevant.",
                    "weights": {"purpose": 3, "judgment": 1, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "That I'll be exposed as someone not as good as people expect.",
                    "weights": {"judgment": 4, "purpose": 1, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
            ],
        },
    ],
    frozenset({"skill_gap", "judgment"}): [
        {
            "id": "fq_skill_gap_judgment_1",
            "text": "When your work doesn't turn out as you imagined, you think:",
            "options": [
                {
                    "text": "'I don't have the technical skill to execute this yet.'",
                    "weights": {"skill_gap": 4, "judgment": 0, "possibility": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "'This is embarrassing — I should be better than this.'",
                    "weights": {"judgment": 4, "skill_gap": 0, "possibility": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "'I need to practise specific techniques to close the gap.'",
                    "weights": {"skill_gap": 4, "judgment": 0, "possibility": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "'I'll never be able to produce what I see in my head.'",
                    "weights": {"judgment": 3, "skill_gap": 1, "possibility": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "'The gap between my taste and my ability feels unbridgeable right now.'",
                    "weights": {"skill_gap": 2, "judgment": 2, "possibility": 0, "purpose": 0, "fatigue": 0},
                },
            ],
        },
        {
            "id": "fq_skill_gap_judgment_2",
            "text": "What describes your relationship to learning new creative techniques?",
            "options": [
                {
                    "text": "Eager — I know what I need to learn and I'm actively seeking it.",
                    "weights": {"skill_gap": 4, "judgment": 0, "possibility": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "Avoidant — practising feels humiliating because I see how bad my attempts are.",
                    "weights": {"judgment": 4, "skill_gap": 0, "possibility": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "Frustrated — I understand the technique but can't make it work in practice.",
                    "weights": {"skill_gap": 3, "judgment": 1, "possibility": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "Paralysed — I don't want anyone to see me at the clumsy learning stage.",
                    "weights": {"judgment": 3, "skill_gap": 1, "possibility": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "Ambivalent — I'm not sure more skill would solve the underlying problem.",
                    "weights": {"skill_gap": 1, "judgment": 1, "possibility": 0, "purpose": 2, "fatigue": 0},
                },
            ],
        },
    ],
    frozenset({"possibility", "fatigue"}): [
        {
            "id": "fq_possibility_fatigue_1",
            "text": "When you find yourself not working on your project, the most accurate description is:",
            "options": [
                {
                    "text": "I'm down a rabbit hole of new ideas and never actually make anything.",
                    "weights": {"possibility": 4, "fatigue": 0, "purpose": 0, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "I'm resting — too exhausted to create anything right now.",
                    "weights": {"fatigue": 4, "possibility": 0, "purpose": 0, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "I'm researching and exploring — which feels productive but produces nothing.",
                    "weights": {"possibility": 3, "fatigue": 1, "purpose": 0, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "I'm procrastinating because I have no energy and no idea what to do next.",
                    "weights": {"fatigue": 2, "possibility": 2, "purpose": 0, "skill_gap": 0, "judgment": 0},
                },
                {
                    "text": "I'm scrolling — too tired to make, not bored enough to stop.",
                    "weights": {"fatigue": 4, "possibility": 0, "purpose": 0, "skill_gap": 0, "judgment": 0},
                },
            ],
        },
    ],
}
