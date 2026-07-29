"""
llm_client.py – Optional watsonx-powered exercise personalization and
                context-based category scoring.

Controlled by env var:
  WATSONX_ENABLED=true  (any other value disables it, default: disabled)

Required when enabled:
  WATSONX_URL          e.g. https://us-south.ml.cloud.ibm.com
  WATSONX_API_KEY
  WATSONX_PROJECT_ID
  WATSONX_MODEL_ID     default: ibm/granite-3-3-8b-instruct

Public API
----------
personalize_exercise(exercise: str, context: str, block_name: str) -> str

  exercise   : the canonical exercise text from interventions.py
  context    : free-text from the user about their specific situation
  block_name : display name of the diagnosed block (for prompt framing)

  Returns a 1-2 sentence addition that references the user's context while
  keeping the core technique identical.  On any failure (watsonx disabled,
  missing creds, SDK error) returns the offline fallback string instead —
  never raises.

analyze_context_for_categories(user_context: str) -> dict[str, float] | None

  user_context : free-text description of the user's creative situation.

  Returns a dict mapping each of the 5 category keys to a 0-10 float
  indicating how strongly the described situation suggests that block.
  Returns None when watsonx is disabled, credentials are missing, the
  response cannot be parsed, or any other error occurs — never raises.
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

# ── Environment ──────────────────────────────────────────────────────────────

_ENABLED: bool = os.getenv("WATSONX_ENABLED", "false").strip().lower() == "true"
_URL: str = os.getenv("WATSONX_URL", "")
_API_KEY: str = os.getenv("WATSONX_API_KEY", "")
_PROJECT_ID: str = os.getenv("WATSONX_PROJECT_ID", "")
_MODEL_ID: str = os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-3-8b-instruct")

# ── Prompt templates ──────────────────────────────────────────────────────────

# ---- exercise personalisation -----------------------------------------------

_SYSTEM_PROMPT = (
    "You are a direct, practical creative-coaching assistant. "
    "You are given a diagnosed creative block type, a specific exercise, and a "
    "user's description of their personal situation. "
    "Your job is to write 2-3 sentences that make the exercise feel immediately "
    "and concretely applicable to what the user described. "
    "Rules: (1) Reference at least one specific detail from the user's situation "
    "by name — a project type, medium, deadline, person, or feeling they mentioned. "
    "(2) Do not restate or summarise the exercise — assume the user just read it. "
    "(3) Do not give generic creative advice. "
    "(4) Do not use motivational language or toxic positivity. "
    "(5) If the block type is fatigue, do not tell the user to push through — "
    "acknowledge the depletion and make the exercise feel low-cost. "
    "(6) Output only the 2-3 sentences — no preamble, no sign-off, no label."
)

_USER_TEMPLATE = """\
Block type: {block_name}

Core exercise:
{exercise}

User's situation (their own words):
{context}

Write 2-3 sentences that make the exercise feel specifically tailored to what this \
person described. Name something concrete from their situation. Make it feel like \
the exercise was written for them, not for a generic creative person.\
"""

# ---- context-category scoring -----------------------------------------------

_CATEGORIES = ("possibility", "purpose", "skill_gap", "fatigue", "judgment",
               "comparison", "imposter_syndrome", "perfectionism")

_CONTEXT_SYSTEM_PROMPT = (
    "You are a conservative scoring assistant for a creative-block diagnostic tool. "
    "You will receive a free-text description of a creative person's situation. "
    "Your job is to score how much their description suggests each of five creative-block "
    "categories on a scale of 0 to 10 (0 = no evidence, 10 = very strong evidence). "
    "Rules: "
    "(1) Be conservative — the quiz answers carry most of the diagnostic weight; "
    "this is a small secondary signal only. "
    "(2) Only raise a score above 5 if the user explicitly describes that pattern. "
    "(3) Most scores should be 0-3 unless the user's words clearly match a category. "
    "(4) Return ONLY a JSON object with exactly these keys: "
    "possibility, purpose, skill_gap, fatigue, judgment, "
    "comparison, imposter_syndrome, perfectionism. "
    "No explanation, no preamble, no markdown code fences — raw JSON only."
)

_CONTEXT_USER_TEMPLATE = """\
User's description of their creative situation (their own words):
{user_context}

Return a JSON object scoring 0-10 for each category: \
possibility, purpose, skill_gap, fatigue, judgment, \
comparison, imposter_syndrome, perfectionism.\
"""

# ── Offline fallback ──────────────────────────────────────────────────────────

_FALLBACK_TEMPLATE = (
    "Given what you've described — {context_snippet} — this exercise is "
    "a good starting point. Adapt the constraints to fit your specific situation."
)

_MAX_CONTEXT_SNIPPET = 80  # chars shown in fallback


def _offline_fallback(context: str) -> str:
    snippet = context.strip()
    if len(snippet) > _MAX_CONTEXT_SNIPPET:
        snippet = snippet[:_MAX_CONTEXT_SNIPPET].rstrip() + "…"
    return _FALLBACK_TEMPLATE.format(context_snippet=snippet)


# ── watsonx helpers ───────────────────────────────────────────────────────────

def _watsonx_model():
    """Construct and return a ModelInference instance; raises on any error."""
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference

    credentials = Credentials(url=_URL, api_key=_API_KEY)
    return ModelInference(
        model_id=_MODEL_ID,
        credentials=credentials,
        project_id=_PROJECT_ID,
    )


def _call_watsonx(exercise: str, context: str, block_name: str) -> str:
    """Call IBM watsonx for exercise personalisation; raises on any error."""
    model = _watsonx_model()

    messages = [
        {"role": "system", "content": _SYSTEM_PROMPT},
        {
            "role": "user",
            "content": _USER_TEMPLATE.format(
                block_name=block_name,
                exercise=exercise,
                context=context,
            ),
        },
    ]

    response = model.chat(messages=messages)

    # SDK response shape: {"choices": [{"message": {"content": "..."}}], ...}
    content: str = response["choices"][0]["message"]["content"]
    return content.strip()


def _call_watsonx_context_scores(user_context: str) -> dict[str, float]:
    """
    Call IBM watsonx for context-based category scores; raises on any error.
    Returns a dict with exactly the 5 category keys, values clamped to [0, 10].
    """
    import json as _json

    model = _watsonx_model()

    messages = [
        {"role": "system", "content": _CONTEXT_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": _CONTEXT_USER_TEMPLATE.format(user_context=user_context),
        },
    ]

    response = model.chat(messages=messages)
    raw: str = response["choices"][0]["message"]["content"].strip()

    # Strip markdown code fences the model may emit despite instructions.
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    parsed = _json.loads(raw)  # raises ValueError/JSONDecodeError on bad output

    # Validate and clamp each expected key.
    result: dict[str, float] = {}
    for cat in _CATEGORIES:
        val = parsed.get(cat)
        if val is None:
            raise ValueError(f"Missing category key in watsonx response: {cat!r}")
        result[cat] = float(max(0.0, min(10.0, val)))

    return result


# ── Public API ────────────────────────────────────────────────────────────────

def _watsonx_available() -> bool:
    """Return True when watsonx is enabled and all required credentials exist."""
    return _ENABLED and bool(_URL and _API_KEY and _PROJECT_ID)


def analyze_context_for_categories(user_context: str) -> dict[str, float] | None:
    """
    Send *user_context* to watsonx and return a dict mapping each of the 5
    category keys to a 0-10 float representing how strongly the described
    situation suggests that block type.

    Conservative by design — see the system prompt.  Returns ``None`` when:
    - watsonx is disabled (WATSONX_ENABLED != "true")
    - one or more required credentials are missing
    - the model response cannot be parsed as valid JSON with the expected keys
    - any SDK or network error occurs

    Never raises.
    """
    user_context = (user_context or "").strip()
    if not user_context:
        return None

    if not _watsonx_available():
        if _ENABLED:
            logger.warning(
                "WATSONX_ENABLED=true but one or more of WATSONX_URL / "
                "WATSONX_API_KEY / WATSONX_PROJECT_ID is missing. "
                "Skipping context analysis."
            )
        return None

    try:
        return _call_watsonx_context_scores(user_context)
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "watsonx context scoring failed (%s: %s); skipping.",
            type(exc).__name__,
            exc,
        )
        return None


def personalize_exercise(exercise: str, context: str, block_name: str) -> str:
    """
    Return a 1-2 sentence personalisation of *exercise* given the user's
    free-text *context*.  Always returns a string, never raises.

    If watsonx is disabled or context is blank, returns empty string so the
    caller can decide whether to append it.
    """
    context = (context or "").strip()
    if not context:
        return ""

    if not _ENABLED:
        return _offline_fallback(context)

    if not _watsonx_available():
        logger.warning(
            "WATSONX_ENABLED=true but one or more of WATSONX_URL / "
            "WATSONX_API_KEY / WATSONX_PROJECT_ID is missing. "
            "Falling back to offline template."
        )
        return _offline_fallback(context)

    try:
        return _call_watsonx(exercise, context, block_name)
    except Exception as exc:  # noqa: BLE001
        logger.warning("watsonx call failed (%s: %s); using offline fallback.", type(exc).__name__, exc)
        return _offline_fallback(context)
