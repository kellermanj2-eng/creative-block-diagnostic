"""
questions.py – Quiz questions and their weighted answer options.

Each question has 5 answer options (index 0–7).
Each option carries a `weights` dict mapping category keys to point values.
Categories: possibility | purpose | skill_gap | fatigue | judgment
           | comparison | imposter_syndrome | perfectionism

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
    "comparison",
    "imposter_syndrome",
    "perfectionism",
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
            {
                "text": "I open it, glance at what others are making online, and close the tab feeling behind.",
                "weights": {"comparison": 4, "judgment": 1},
            },
            {
                "text": "I start, but a quiet voice asks who I think I am to be making this.",
                "weights": {"imposter_syndrome": 4, "purpose": 1},
            },
            {
                "text": "I plan extensively — outlining, researching — but never actually begin.",
                "weights": {"perfectionism": 4, "possibility": 1},
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
            {
                "text": "I have ideas but they all feel derivative — someone else has already done it better.",
                "weights": {"comparison": 4, "judgment": 1},
            },
            {
                "text": "I have ideas but I'm not qualified to execute them — someone more experienced should.",
                "weights": {"imposter_syndrome": 4, "skill_gap": 1},
            },
            {
                "text": "I have one idea but I'm not ready to start — it needs to be fully formed first.",
                "weights": {"perfectionism": 4, "possibility": 1},
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
            {
                "text": "Deflation — I can already picture better versions of it that others have made.",
                "weights": {"comparison": 4, "judgment": 1},
            },
            {
                "text": "Dread — finishing means being seen, and being seen means being found out.",
                "weights": {"imposter_syndrome": 4, "judgment": 1},
            },
            {
                "text": "Dissatisfaction in advance — I know it won't meet the standard I'm aiming for.",
                "weights": {"perfectionism": 4, "skill_gap": 1},
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
            {
                "text": "'Why bother — someone with real talent has already made something better.'",
                "weights": {"comparison": 4, "purpose": 1},
            },
            {
                "text": "'You're not the kind of person who gets to do this — you don't have the credentials.'",
                "weights": {"imposter_syndrome": 4},
            },
            {
                "text": "'It's not ready yet. Keep refining until it's right before you start.'",
                "weights": {"perfectionism": 4, "possibility": 1},
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
            {
                "text": "Absent. Seeing everyone else's polished output has made starting feel pointless.",
                "weights": {"comparison": 4, "purpose": 1},
            },
            {
                "text": "Sporadic and secretive — I work in bursts but share nothing; I don't feel legitimate.",
                "weights": {"imposter_syndrome": 4, "judgment": 1},
            },
            {
                "text": "Very slow — I redo and refine the same small section rather than moving forward.",
                "weights": {"perfectionism": 4, "skill_gap": 1},
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
            {
                "text": "Paralysed. Their finished, polished work makes mine feel pointless before it exists.",
                "weights": {"comparison": 4, "judgment": 1},
            },
            {
                "text": "Like a fraud. They clearly belong here; I'm not sure I do.",
                "weights": {"imposter_syndrome": 4, "purpose": 1},
            },
            {
                "text": "Critical — I notice every flaw in their work and worry mine will have the same ones.",
                "weights": {"perfectionism": 4, "judgment": 1},
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
            {
                "text": "I'd start something, then spiral into looking at what everyone else is doing instead.",
                "weights": {"comparison": 4, "fatigue": 1},
            },
            {
                "text": "I'd probably find an excuse not to — I don't feel like I've earned the right to make freely.",
                "weights": {"imposter_syndrome": 4, "purpose": 1},
            },
            {
                "text": "I'd spend most of it planning and preparing — I need conditions to be right before I begin.",
                "weights": {"perfectionism": 4, "possibility": 1},
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
            {
                "text": "Hollow. It exists, but better versions of it exist, made by better people.",
                "weights": {"comparison": 4, "purpose": 1},
            },
            {
                "text": "Suspicious of myself — like I got lucky and won't be able to repeat it.",
                "weights": {"imposter_syndrome": 4, "judgment": 1},
            },
            {
                "text": "Already focused on what I should have done differently — I see every flaw first.",
                "weights": {"perfectionism": 4, "judgment": 1},
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
            {
                "text": "Opening a browser and looking at what others are making — and losing momentum entirely.",
                "weights": {"comparison": 4, "fatigue": 1},
            },
            {
                "text": "A thought like 'who am I to be doing this?' that drains the energy from the session.",
                "weights": {"imposter_syndrome": 4, "purpose": 1},
            },
            {
                "text": "Getting stuck trying to perfect an earlier section before I can move on.",
                "weights": {"perfectionism": 4, "skill_gap": 1},
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
            {
                "text": "Like a reason to stop — why finish something that won't measure up to what's already out there?",
                "weights": {"comparison": 4, "purpose": 1},
            },
            {
                "text": "Quietly relieved — if it's unfinished, no one can confirm I wasn't capable of it.",
                "weights": {"imposter_syndrome": 4, "judgment": 1},
            },
            {
                "text": "Like a failure — but also like I can keep improving it indefinitely without the risk of it being judged as final.",
                "weights": {"perfectionism": 4, "judgment": 1},
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

    # ── New category pairs ────────────────────────────────────────────────────

    frozenset({"comparison", "judgment"}): [
        {
            "id": "fq_comparison_judgment_1",
            "text": "When you hesitate to share or commit to your work, the main thought is:",
            "options": [
                {
                    "text": "Someone else has already done this better — what's the point of adding mine?",
                    "weights": {"comparison": 4, "judgment": 0, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "People will look at this and see how mediocre I am.",
                    "weights": {"judgment": 4, "comparison": 0, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "My work can't compete with what's already out there.",
                    "weights": {"comparison": 3, "judgment": 1, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I'll be exposed as less talented than I've led people to believe.",
                    "weights": {"judgment": 3, "comparison": 1, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I measure it against the best work in the field and it doesn't hold up.",
                    "weights": {"comparison": 4, "judgment": 1, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
            ],
        },
    ],

    frozenset({"comparison", "purpose"}): [
        {
            "id": "fq_comparison_purpose_1",
            "text": "When your motivation disappears, what's driving it?",
            "options": [
                {
                    "text": "The work feels redundant — others are doing this and doing it better.",
                    "weights": {"comparison": 4, "purpose": 0, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I can't find a reason the work needs to exist at all.",
                    "weights": {"purpose": 4, "comparison": 0, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "Both — the space feels saturated AND I don't know why I'd add to it.",
                    "weights": {"comparison": 2, "purpose": 2, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I struggle to see the value in my contribution specifically.",
                    "weights": {"comparison": 3, "purpose": 1, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "The work matters in general — I just can't connect to why I'm doing it.",
                    "weights": {"purpose": 4, "comparison": 0, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
            ],
        },
    ],

    frozenset({"imposter_syndrome", "judgment"}): [
        {
            "id": "fq_imposter_judgment_1",
            "text": "When you imagine people seeing your finished work, the fear is:",
            "options": [
                {
                    "text": "They'll realise I don't actually belong in this space.",
                    "weights": {"imposter_syndrome": 4, "judgment": 0, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "They'll see how bad the work is.",
                    "weights": {"judgment": 4, "imposter_syndrome": 0, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "They'll think I'm overreaching — trying to do something I'm not credentialed to do.",
                    "weights": {"imposter_syndrome": 4, "judgment": 1, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "They'll see how far it falls short of what I should be capable of.",
                    "weights": {"judgment": 3, "imposter_syndrome": 1, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "Both — that I'm a fraud AND that the work proves it.",
                    "weights": {"imposter_syndrome": 2, "judgment": 2, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
            ],
        },
    ],

    frozenset({"imposter_syndrome", "purpose"}): [
        {
            "id": "fq_imposter_purpose_1",
            "text": "When you ask yourself 'why am I making this?', the answer that surfaces is:",
            "options": [
                {
                    "text": "I don't know who it's for or why it should exist.",
                    "weights": {"purpose": 4, "imposter_syndrome": 0, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I want to make it, but I'm not sure I'm the right person to.",
                    "weights": {"imposter_syndrome": 4, "purpose": 0, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I question both why and whether I have standing to do it.",
                    "weights": {"imposter_syndrome": 2, "purpose": 2, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "The subject matters — I'm just not sure my voice adds anything to it.",
                    "weights": {"imposter_syndrome": 3, "purpose": 1, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "Even if I knew the purpose, I'd feel unqualified to execute it.",
                    "weights": {"imposter_syndrome": 4, "purpose": 1, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
            ],
        },
    ],

    frozenset({"perfectionism", "judgment"}): [
        {
            "id": "fq_perfectionism_judgment_1",
            "text": "What most often prevents you from calling a piece of work done?",
            "options": [
                {
                    "text": "It hasn't reached the internal standard I've set for it yet.",
                    "weights": {"perfectionism": 4, "judgment": 0, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I'm afraid of how it'll be received once it's out in the world.",
                    "weights": {"judgment": 4, "perfectionism": 0, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "There's always one more improvement to make — it's never quite there.",
                    "weights": {"perfectionism": 4, "judgment": 1, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "Finishing means publishing, and publishing means judgement.",
                    "weights": {"judgment": 3, "perfectionism": 1, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "I keep the bar moving — as soon as I reach one standard, I raise it.",
                    "weights": {"perfectionism": 4, "judgment": 0, "possibility": 0, "skill_gap": 0, "fatigue": 0},
                },
            ],
        },
    ],

    frozenset({"perfectionism", "skill_gap"}): [
        {
            "id": "fq_perfectionism_skill_gap_1",
            "text": "When your work falls short of what you imagined, your immediate interpretation is:",
            "options": [
                {
                    "text": "I don't have the technical ability to execute it yet — I need to improve.",
                    "weights": {"skill_gap": 4, "perfectionism": 0, "judgment": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "The standard I'm holding it to is the problem — not the execution.",
                    "weights": {"perfectionism": 4, "skill_gap": 0, "judgment": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "I need more skill AND I refuse to ship anything below my standard.",
                    "weights": {"skill_gap": 2, "perfectionism": 2, "judgment": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "Specific techniques are missing — if I learn them, the quality will meet my standard.",
                    "weights": {"skill_gap": 3, "perfectionism": 1, "judgment": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "I could produce something acceptable but I won't release it at that quality.",
                    "weights": {"perfectionism": 4, "skill_gap": 1, "judgment": 0, "purpose": 0, "fatigue": 0},
                },
            ],
        },
    ],

    frozenset({"comparison", "imposter_syndrome"}): [
        {
            "id": "fq_comparison_imposter_1",
            "text": "When you look at others in your creative field, the thought that most holds you back is:",
            "options": [
                {
                    "text": "Their work is so much better — mine doesn't add anything.",
                    "weights": {"comparison": 4, "imposter_syndrome": 0, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "They actually belong here — I don't.",
                    "weights": {"imposter_syndrome": 4, "comparison": 0, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "The field is full of people who are more legitimate than I am.",
                    "weights": {"imposter_syndrome": 3, "comparison": 1, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "Why would anyone look at mine when theirs exists?",
                    "weights": {"comparison": 3, "imposter_syndrome": 1, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "They've earned the right to make; I haven't yet.",
                    "weights": {"imposter_syndrome": 4, "comparison": 1, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
            ],
        },
    ],

    frozenset({"comparison", "perfectionism"}): [
        {
            "id": "fq_comparison_perfectionism_1",
            "text": "The standard you're holding your work to comes from:",
            "options": [
                {
                    "text": "The best work I've seen others produce in this space.",
                    "weights": {"comparison": 4, "perfectionism": 0, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "An internal ideal I've set for myself, independent of anyone else's work.",
                    "weights": {"perfectionism": 4, "comparison": 0, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "Both — others' best work has shaped what I think my standard should be.",
                    "weights": {"comparison": 2, "perfectionism": 2, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "The most successful examples in the field — I benchmark against those.",
                    "weights": {"comparison": 4, "perfectionism": 1, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
                {
                    "text": "My own previous best — each new work has to exceed the last.",
                    "weights": {"perfectionism": 4, "comparison": 1, "judgment": 0, "skill_gap": 0, "fatigue": 0},
                },
            ],
        },
    ],

    frozenset({"imposter_syndrome", "skill_gap"}): [
        {
            "id": "fq_imposter_skill_gap_1",
            "text": "When you feel unqualified to make your project, the main reason is:",
            "options": [
                {
                    "text": "I genuinely lack specific skills I need — it's a real gap, not a feeling.",
                    "weights": {"skill_gap": 4, "imposter_syndrome": 0, "judgment": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "I have the skills but I don't feel like a legitimate practitioner.",
                    "weights": {"imposter_syndrome": 4, "skill_gap": 0, "judgment": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "Even when I improve my skills, I still feel like I'm pretending.",
                    "weights": {"imposter_syndrome": 4, "skill_gap": 1, "judgment": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "The gap between my vision and execution makes me feel like a fraud.",
                    "weights": {"skill_gap": 2, "imposter_syndrome": 2, "judgment": 0, "purpose": 0, "fatigue": 0},
                },
                {
                    "text": "Once I close the skill gap, I'll feel more legitimate.",
                    "weights": {"skill_gap": 3, "imposter_syndrome": 1, "judgment": 0, "purpose": 0, "fatigue": 0},
                },
            ],
        },
    ],
}
