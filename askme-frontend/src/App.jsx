import { useEffect, useMemo, useRef, useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
const STORAGE_KEY_HISTORY = 'askme:last3'
const STORAGE_KEY_SESSION_COUNT = 'askme:sessionCount'
const SESSION_MAX = 5

function loadLastQuestions() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY_HISTORY)
    if (!raw) return []
    const arr = JSON.parse(raw)
    return Array.isArray(arr) ? arr.slice(-3) : []
  } catch {
    return []
  }
}

function saveLastQuestion(q) {
  const arr = loadLastQuestions()
  arr.push(q)
  localStorage.setItem(STORAGE_KEY_HISTORY, JSON.stringify(arr.slice(-3)))
}

function getSessionCount() {
  const raw = sessionStorage.getItem(STORAGE_KEY_SESSION_COUNT)
  return raw ? parseInt(raw, 10) || 0 : 0
}

function bumpSessionCount() {
  const next = getSessionCount() + 1
  sessionStorage.setItem(STORAGE_KEY_SESSION_COUNT, String(next))
  return next
}

function App() {
  const [messages, setMessages] = useState(() => {
    const last3 = loadLastQuestions()
    const seed = last3.map(q => ({ role: 'user', content: q }))
    return seed.length ? seed : [{ role: 'bot', content: 'Hi! Ask me anything.' }]
  })
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const chatRef = useRef(null)

  useEffect(() => {
    chatRef.current?.scrollTo({ top: chatRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, loading])

  const sessionLeft = useMemo(() => Math.max(0, SESSION_MAX - getSessionCount()), [messages.length])

  async function handleAsk(e) {
    e.preventDefault()
    if (loading) return
    const q = input.trim()
    if (!q) return

    // client-side rate limit in session
    if (getSessionCount() >= SESSION_MAX) {
      setError('Session limit reached (max 5). Please try again later.')
      return
    }

    setError('')
    setLoading(true)
    setMessages(prev => [...prev, { role: 'user', content: q }])
    setInput('')

    try {
      const resp = await fetch(`${API_BASE}/api/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q }),
      })
      const data = await resp.json()
      if (!resp.ok) throw new Error(data?.detail || 'Request failed')
      const answer = data.answer
      setMessages(prev => [...prev, { role: 'bot', content: answer }])
      saveLastQuestion(q)
      bumpSessionCount()
    } catch (err) {
      setMessages(prev => [...prev, { role: 'bot', content: `Error: ${err.message}` }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="header">AskMe Bot</div>
      <div className="chat" ref={chatRef}>
        {messages.map((m, idx) => (
          <div key={idx} className={`bubble ${m.role === 'user' ? 'user' : 'bot'}`}>
            {m.content}
          </div>
        ))}
        {loading && <div className="bubble bot">Thinking…</div>}
      </div>
      <div className="footer">
        <form className="form" onSubmit={handleAsk}>
          <input
            className="input"
            placeholder="Type your question..."
            value={input}
            onChange={e => setInput(e.target.value)}
            disabled={loading}
          />
          <button className="button" disabled={loading || !input.trim()} type="submit">
            Ask
          </button>
        </form>
        <div className="hint">Session remaining: {sessionLeft} / {SESSION_MAX}</div>
      </div>
    </div>
  )
}

export default App
