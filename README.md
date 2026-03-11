# AI Automation Builder — Backend API

A production-ready FastAPI backend that converts a plain-language idea into a structured AI automation workflow using Google Gemini and a multi-agent pipeline.

---

## Architecture

```
POST /api/generate-automation
        │
        ▼
 ┌─────────────┐
 │ PlannerAgent│  — Extracts intent, domain, trigger hints
 └──────┬──────┘
        │
        ▼
 ┌─────────────┐
 │ BuilderAgent│  — Constructs steps, integrations, ai_tasks
 └──────┬──────┘
        │
        ▼
 ┌──────────────┐
 │ReviewerAgent │  — Validates, improves, assigns confidence_score
 └──────┬───────┘
        │
        ▼
  AutomationResponse (JSON)
```

---

## API Reference

### `POST /api/generate-automation`

**Request**
```json
{
  "idea": "Build automation that analyzes sales Excel reports and generates a summary"
}
```

**Response**
```json
{
  "automation_name": "Sales Report Analysis Automation",
  "trigger": "File Upload",
  "steps": [
    "Receive uploaded Excel file",
    "Parse and validate spreadsheet structure",
    "Extract sales data and key metrics",
    "Analyze trends with AI",
    "Generate executive summary",
    "Send summary via email"
  ],
  "integrations": ["Excel", "Gmail"],
  "ai_tasks": ["data_extraction", "trend_analysis", "report_generation"],
  "confidence_score": 0.92
}
```

**Error Response**
```json
{
  "detail": "Error message",
  "code": "ERROR_CODE"
}
```

### `GET /api/health`
Returns `{"status": "ok", "version": "1.0.0"}`.

### `GET /api/docs`
Swagger UI.

---

## Local Development

### 1. Clone & install

```bash
git clone https://github.com/your-org/ai-automation-builder.git
cd ai-automation-builder
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and set GEMINI_API_KEY
```

### 3. Run locally

```bash
uvicorn api.generate-automation:app --reload --port 8000
```

Open [http://localhost:8000/api/docs](http://localhost:8000/api/docs).

---

## Deploy to Vercel

### Prerequisites
- [Vercel CLI](https://vercel.com/docs/cli): `npm i -g vercel`
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Steps

#### 1. Add the secret to Vercel

```bash
vercel secrets add gemini_api_key "your_actual_api_key_here"
```

#### 2. Deploy

```bash
vercel deploy --prod
```

Vercel will auto-detect `vercel.json`, install Python 3.11, and deploy the function.

#### 3. Test

```bash
curl -X POST https://your-project.vercel.app/api/generate-automation \
  -H "Content-Type: application/json" \
  -d '{"idea": "Send a Slack alert when a new lead is added to HubSpot"}'
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | — | Google Gemini API key |
| `GEMINI_MODEL` | No | `gemini-1.5-flash` | Gemini model name |
| `GEMINI_TEMPERATURE` | No | `0.4` | LLM sampling temperature |
| `APP_ENV` | No | `production` | App environment |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `CORS_ORIGINS` | No | `["*"]` | Allowed CORS origins |

---

## Project Structure

```
ai-automation-builder/
├── api/
│   └── generate-automation.py   # FastAPI app + Vercel entry point
├── app/
│   ├── config.py                # Settings (pydantic-settings)
│   ├── logging_config.py        # Structured JSON logging
│   ├── agents/
│   │   ├── planner_agent.py     # Intent extraction
│   │   ├── builder_agent.py     # Workflow construction
│   │   └── reviewer_agent.py    # Validation + confidence scoring
│   ├── services/
│   │   └── gemini_client.py     # Reusable Gemini API client
│   ├── schemas/
│   │   ├── request_models.py    # AutomationRequest
│   │   └── response_models.py   # AutomationResponse, ErrorResponse
│   └── core/
│       └── workflow_generator.py # Orchestrator
├── requirements.txt
├── vercel.json
├── .env.example
└── README.md
```

---

## License

MIT
