![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Built with IBM watsonx](https://img.shields.io/badge/built%20with-IBM%20watsonx-054ADA?logo=ibm&logoColor=white)

# Creative Block Diagnostic

A small Flask web app that helps you figure out *why* you're creatively stuck and gives you one specific exercise to get unstuck.

Answer ten questions, receive a scored diagnosis across five block categories, and get a targeted exercise to break through — with AI-powered personalisation via IBM watsonx Granite, verified working end-to-end (and gracefully offline when credentials aren't provided).

---

## Quick Start for Testers

**No IBM Cloud account required.** The app runs fully offline out of the box.

### Option A — Docker (fastest, zero Python/pip setup)

```bash
git clone https://github.com/kellermanj2-eng/creative-block-diagnostic.git
cd creative-block-diagnostic
docker build -t creative-block-diagnostic .
docker run -p 5000:5000 creative-block-diagnostic
```

Open [http://localhost:5000](http://localhost:5000). Done.

> To enable watsonx AI personalisation, pass credentials at run time:
> ```bash
> docker run -p 5000:5000 \
>   -e WATSONX_ENABLED=true \
>   -e WATSONX_URL=https://us-south.ml.cloud.ibm.com \
>   -e WATSONX_API_KEY=your_key \
>   -e WATSONX_PROJECT_ID=your_project_id \
>   creative-block-diagnostic
> ```

### Option B — Setup script (no Docker)

**Mac / Linux**
```bash
git clone https://github.com/kellermanj2-eng/creative-block-diagnostic.git
cd creative-block-diagnostic
bash setup.sh
source .venv/bin/activate
python app.py
```

**Windows**
```bat
git clone https://github.com/kellermanj2-eng/creative-block-diagnostic.git
cd creative-block-diagnostic
setup.bat
.venv\Scripts\activate
python app.py
```

The setup script creates a virtual environment, installs all dependencies, and copies `.env.example` to `.env`.

---

## Built with IBM Bob

This project was scaffolded and built end-to-end with **[IBM Bob](https://www.ibm.com/products/bob)**, an AI software engineer. Specifically, Bob:

- **Scaffolded the Flask application** — created [`app.py`](app.py) with the `GET /` and `POST /diagnose` routes, request parsing, and response shaping
- **Wrote the scoring engine** — designed and implemented [`diagnostic.py`](diagnostic.py), including the weighted category scoring, primary/secondary ranking logic, tie-breaking, and the all-zero fallback
- **Authored the question bank** — wrote all five quiz questions and their weighted answer options in [`questions.py`](questions.py), calibrated so each block category is reliably identifiable from a five-question sweep
- **Defined the intervention library** — wrote all five block descriptions and concrete exercises in [`interventions.py`](interventions.py), including the no-toxic-positivity framing for the fatigue entry
- **Wired up the watsonx integration** — built [`llm_client.py`](llm_client.py) with the Granite prompt templates, credential handling, offline fallback logic, and graceful error recovery so the app never raises on LLM failure
- **Built the quiz UI** — created the single-page HTML/CSS/JS front end in [`templates/index.html`](templates/index.html), including the question renderer, fetch-based form submission, and results display
- **Wrote the test suite** — authored [`_run_tests.py`](_run_tests.py) covering unit tests for scoring, interventions completeness, and the offline LLM path, plus Flask integration tests for all route behaviours
- **Added project documentation** — wrote this README and the MIT [LICENSE](LICENSE)

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

- **Scored quiz** — ten weighted questions map answers to block categories
- **Primary + secondary diagnosis** — secondary is surfaced if it scores within 25 % of primary
- **Concrete exercises** — one specific, actionable exercise per block type (no vague advice)
- **AI personalisation via IBM watsonx Granite** — if you describe your specific situation, `ibm/granite-3-3-8b-instruct` generates a 1–2 sentence note connecting your context to the exercise. This integration has been verified end-to-end with real credentials.
- **Offline-first** — runs completely without credentials; watsonx personalisation gracefully falls back to a template-based note when disabled or unavailable

---

## Screenshots

| Quiz | Diagnosis |
|---|---|
| ![Quiz screenshot](screenshots/quiz.png) | ![Result screenshot](screenshots/result.png) |

---

## Manual setup (step by step)

```bash
# 1. Clone and create a virtual environment
git clone https://github.com/kellermanj2-eng/creative-block-diagnostic.git
cd creative-block-diagnostic
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment (optional — needed only for AI personalisation)
cp .env.example .env
# Edit .env: set WATSONX_ENABLED=true and fill in your IBM Cloud credentials
# The app runs fully offline without this step

# 4. Run the app
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Environment variables

Copy `.env.example` to `.env`. All variables are optional — the app runs fully offline without any of them. The watsonx integration has been tested end-to-end and works with `ibm/granite-3-3-8b-instruct` on IBM Cloud.

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
