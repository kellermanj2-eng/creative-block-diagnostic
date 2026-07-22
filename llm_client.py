"""
llm_client.py – Optional watsonx-powered exercise personalization.

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

# ── Prompt template ───────────────────────────────────────────────────────────

_SYSTEM_PROMPT = (
    "You are a concise creative-coaching assistant. "
    "Your task is to add a short, personalised note (1-2 sentences only) to a "
    "specific creative exercise. The note must reference the user's situation "
    "without changing, replacing, or diluting the core technique. "
    "Output only the 1-2 sentence note — no preamble, no sign-off."
)

_USER_TEMPLATE = """\
Block type: {block_name}

Core exercise:
{exercise}

User's situation:
{context}

Write 1-2 sentences that connect the user's specific situation to the exercise above, \
making it feel immediately applicable to what they described. \
Do not restate the full exercise. Do not give generic advice.\
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


# ── watsonx call ──────────────────────────────────────────────────────────────

def _call_watsonx(exercise: str, context: str, block_name: str) -> str:
    """Call IBM watsonx ModelInference.chat; raises on any error."""
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference

    credentials = Credentials(url=_URL, api_key=_API_KEY)
    model = ModelInference(
        model_id=_MODEL_ID,
        credentials=credentials,
        project_id=_PROJECT_ID,
    )

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


# ── Public API ────────────────────────────────────────────────────────────────

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

    if not all([_URL, _API_KEY, _PROJECT_ID]):
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
