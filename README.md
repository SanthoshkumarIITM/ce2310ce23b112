# AskMe Bot

Minimal AI-powered chatbot for Plivo internship assignment.

## Tech
- Frontend: Vite + React
- Backend: FastAPI (Python), OpenAI API

## Local Development

Backend:
```bash
cd askme-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env # set OPENAI_API_KEY
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd ../askme-frontend
npm install
cp .env.example .env # set VITE_API_BASE if needed
npm run dev
```

Open the frontend dev server and ask questions. Without `OPENAI_API_KEY`, backend returns a placeholder response.

## Deploy
- Backend: Render/railway/fly.io (free tier) or any container host
- Frontend: Vercel/Netlify (set `VITE_API_BASE` to backend URL)

## Notes
- Stores last 3 questions in `localStorage`
- Session-limited to 5 queries with an IP-based server limit as well
- Prompt prefix applied server-side to ensure consistency