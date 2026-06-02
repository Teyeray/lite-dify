'use client'

import { useRouter } from 'next/navigation'
import { FormEvent, useState } from 'react'

import { Shell } from '../components/shell'
import { AppMode, createApp } from '../lib/api'

const defaultWorkflow = {
  nodes: [
    { id: 'start', type: 'start' as const, title: 'Start', config: {} },
    { id: 'llm', type: 'llm' as const, title: 'LLM', config: {} },
    { id: 'answer', type: 'answer' as const, title: 'Answer', config: {} },
  ],
  edges: [
    { source: 'start', target: 'llm' },
    { source: 'llm', target: 'answer' },
  ],
}

export default function NewAppPage() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [mode, setMode] = useState<AppMode>('chatbot')
  const [description, setDescription] = useState('')
  const [systemPrompt, setSystemPrompt] = useState('')
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsSaving(true)
    setError('')
    try {
      const app = await createApp({
        name,
        mode,
        description,
        system_prompt: systemPrompt,
        workflow: mode === 'chatflow' || mode === 'workflow' ? defaultWorkflow : undefined,
      })
      router.push(`/chat?app=${app.id}`)
    }
    catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create app')
      setIsSaving(false)
    }
  }

  return (
    <Shell>
      <div className="toolbar">
        <h1>New app</h1>
      </div>
      <form className="form" onSubmit={onSubmit}>
        <div className="field">
          <label htmlFor="name">Name</label>
          <input id="name" value={name} onChange={event => setName(event.target.value)} required />
        </div>
        <div className="field">
          <label htmlFor="mode">Mode</label>
          <select id="mode" value={mode} onChange={event => setMode(event.target.value as AppMode)}>
            <option value="chatbot">Chatbot</option>
            <option value="chatflow">Chatflow</option>
            <option value="workflow">Workflow</option>
            <option value="agent">Agent</option>
          </select>
        </div>
        <div className="field">
          <label htmlFor="description">Description</label>
          <input id="description" value={description} onChange={event => setDescription(event.target.value)} />
        </div>
        <div className="field">
          <label htmlFor="prompt">System prompt</label>
          <textarea id="prompt" rows={6} value={systemPrompt} onChange={event => setSystemPrompt(event.target.value)} />
        </div>
        <button className="button" disabled={isSaving} type="submit">
          {isSaving ? 'Creating' : 'Create'}
        </button>
        {error && <p className="muted" role="alert">{error}</p>}
      </form>
    </Shell>
  )
}
