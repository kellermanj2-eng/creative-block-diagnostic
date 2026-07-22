# Creative Block Diagnostic

A small Flask web app that helps you figure out *why* you're creatively stuck and gives you one specific exercise to get unstuck.

Answer five questions, receive a scored diagnosis across five block categories, and get a targeted exercise to break through — with optional AI-powered personalisation via IBM watsonx.

---

## Block categories

| Key | Name | What it is |
|---|---|---|
| `possibility` | Possibility Paralysis | Too many options; nothing feels justified |
| `purpose` | Purpose Void | The work feels hollow before it's finished |
| `skill_gap` | Execution Gap | Clear vision, but the skills aren't there yet |
| `fatigue` | Creative Depletion | Genuine low energy — pushing harder makes it worse |
| `judgment` | Judgment Block | Editing before creating; the inner critic blocks output |

---

## Features

- **Scored quiz** — five weighted questions map answers to block categories
- **Primary + secondary diagnosis** — secondary is surfaced if it scores within 25 % of primary
- **Concrete exercises** — one specific, actionable exercise per block type (no vague advice)
- **Optional personalisation** — if you describe your specific situation, IBM watsonx Granite generates a 1–2 sentence note connecting your context to the exercise
- **Offline-first** — runs completely without credentials; watsonx is opt-in

---

## Quick start

```bash
# 1. Clone and create a virtual environment
git clone https://github.com/<your-username>/creative-block-diagnostic.git
cd creative-block-diagnostic
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment (optional — needed only for watsonx)
cp .env.example .env
# Edit .env and set WATSONX_ENABLED=true + your credentials

# 4. Run the app
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Environment variables

Copy `.env.example` to `.env`. All variables are optional — the app runs fully offline without any of them.

| Variable | Default | Description |
|---|---|---|
| `WATSONX_ENABLED` | `false` | Set to `true` to enable LLM personalisation |
| `WATSONX_URL` | — | Your watsonx endpoint, e.g. `https://us-south.ml.cloud.ibm.com` |
| `WATSONX_API_KEY` | — | IBM Cloud API key |
| `WATSONX_PROJECT_ID` | — | watsonx project ID |
| `WATSONX_MODEL_ID` | `ibm/granite-3-3-8b-instruct` | Model to use for personalisation |
| `FLASK_DEBUG` | `false` | Enable Flask debug mode |

---

## API

### `GET /`
Serves the quiz UI.

### `POST /diagnose`
Accepts a JSON body and returns the diagnosis.

**Request**
```json
{
  "answers": {
    "q1": 4,
    "q2": 4,
    "q3": 4,
    "q4": 4,
    "q5": 4
  },
  "context": "Optional free-text about your specific situation"
}
```

**Response**
```json
{
  "primary": "judgment",
  "primary_name": "Judgment Block",
  "primary_description": "...",
  "exercise": "...",
  "personalization": "...",
  "secondary": "possibility",
  "secondary_name": "Possibility Paralysis",
  "scores": { "possibility": 5, "purpose": 0, "skill_gap": 0, "fatigue": 0, "judgment": 20 }
}
```

`personalization` is an empty string when watsonx is disabled or no context was provided.  
`secondary` and `secondary_name` are `null` when no second block scores within 25 % of the primary.

---

## Running the tests

```bash
python _run_tests.py
```

Runs unit tests (scoring logic, interventions completeness, offline LLM path) and Flask integration tests.

---

## License

MIT — see [LICENSE](LICENSE).
