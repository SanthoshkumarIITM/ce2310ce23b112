from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import time
from collections import deque, defaultdict
import httpx
from dotenv import load_dotenv

load_dotenv()

PROMPT_PREFIX = "Answer like you're a helpful assistant."

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")

# Simple in-memory rate limit: 5 requests per 10 minutes per IP
RATE_LIMIT_MAX = int(os.getenv("RATE_LIMIT_MAX", "5"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", str(10 * 60)))
_ip_to_timestamps: dict[str, deque] = defaultdict(deque)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


def _is_rate_limited(ip: str) -> bool:
    now = time.time()
    timestamps = _ip_to_timestamps[ip]
    # Drop timestamps outside the window
    while timestamps and now - timestamps[0] > RATE_LIMIT_WINDOW_SECONDS:
        timestamps.popleft()
    if len(timestamps) >= RATE_LIMIT_MAX:
        return True
    timestamps.append(now)
    return False


async def call_openai_chat_completion(question: str) -> str:
    if not OPENAI_API_KEY:
        return "Demo mode: Set OPENAI_API_KEY to get real AI answers. Here's a placeholder response to your question: " + question

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": PROMPT_PREFIX},
            {"role": "user", "content": question},
        ],
        "temperature": 0.7,
    }
    timeout = httpx.Timeout(30.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(OPENAI_API_URL, headers=headers, json=payload)
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Upstream AI error: {resp.text}")
        data = resp.json()
        try:
            content = data["choices"][0]["message"]["content"].strip()
            return content
        except Exception:
            raise HTTPException(status_code=502, detail="Unexpected AI response format")


app = FastAPI(title="AskMe API", version="0.1.0")

# CORS - allow all for simplicity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "ok", "service": "askme-backend"}


@app.post("/api/ask", response_model=AskResponse)
async def ask(request: Request, body: AskRequest):
    client_host = request.client.host if request.client else "unknown"
    if _is_rate_limited(client_host):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")

    question = (body.question or "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    answer = await call_openai_chat_completion(question)
    return AskResponse(answer=answer)


# For local run: uvicorn askme-backend.app:app --reload --host 0.0.0.0 --port 8000