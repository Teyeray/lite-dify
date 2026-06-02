'use client'

import { Send } from 'lucide-react'
import { FormEvent, useEffect, useState } from 'react'

import { Shell } from '../components/shell'
import { AppDefinition, listApps, sendChat } from '../lib/api'

type LocalMessage = {
  role: 'user' | 'assistant'
  content: string
}

export default function ChatPage() {
  const [apps, setApps] = useState<AppDefinition[]>([])
  const [appId, setAppId] = useState('')
  const [conversationId, setConversationId] = useState<string | undefined>()
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState<LocalMessage[]>([])
  const [isSending, setIsSending] = useState(false)

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    listApps().then(items => {
      setApps(items)
      setAppId(params.get('app') || items[0]?.id || '')
    })
  }, [])

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!appId || !query.trim())
      return

    const nextQuery = query.trim()
    setQuery('')
    setIsSending(true)
    setMessages(current => [...current, { role: 'user', content: nextQuery }])
    const result = await sendChat(appId, nextQuery, conversationId)
    setConversationId(result.conversation.id)
    setMessages(current => [...current, { role: 'assistant', content: result.answer.content }])
    setIsSending(false)
  }

  return (
    <Shell>
      <div className="toolbar">
        <h1>Chat</h1>
        <select value={appId} onChange={event => setAppId(event.target.value)}>
          <option value="">Select app</option>
          {apps.map(app => (
            <option key={app.id} value={app.id}>{app.name}</option>
          ))}
        </select>
      </div>
      <div className="chat">
        <div className="messages">
          {messages.map((message, index) => (
            <div className="message" key={`${message.role}-${index}`}>
              <div className="role">{message.role}</div>
              {message.content}
            </div>
          ))}
          {messages.length === 0 && <p className="muted">Choose an app and send a message.</p>}
        </div>
        <form className="composer" onSubmit={onSubmit}>
          <input value={query} onChange={event => setQuery(event.target.value)} placeholder="Message" />
          <button className="button" disabled={isSending || !appId} type="submit">
            <Send size={18} />
            Send
          </button>
        </form>
      </div>
    </Shell>
  )
}

