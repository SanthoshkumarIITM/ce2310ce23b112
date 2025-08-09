# AskMe Backend

FastAPI backend providing `/api/ask` that proxies to OpenAI Chat Completions with a simple prompt prefix.

- In-memory IP-based rate limit (5 per 10 minutes by default)
- Prompt prefix: "Answer like you're a helpful assistant."

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env # set OPENAI_API_KEY to enable real answers
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

```http
POST /api/ask
{ "question": "What is Plivo?" }
```
