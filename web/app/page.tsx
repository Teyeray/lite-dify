import { Plus } from 'lucide-react'
import Link from 'next/link'

import { Shell } from './components/shell'
import { listApps } from './lib/api'

export default async function AppsPage() {
  const apps = await listApps().catch(() => [])

  return (
    <Shell>
      <div className="toolbar">
        <h1>Apps</h1>
        <Link className="button" href="/new">
          <Plus size={18} />
          New app
        </Link>
      </div>
      <div className="grid">
        {apps.map(app => (
          <Link className="card" href={`/chat?app=${app.id}`} key={app.id}>
            <h2>{app.name}</h2>
            <p className="muted">{app.mode}</p>
            <p>{app.description || 'No description'}</p>
          </Link>
        ))}
        {apps.length === 0 && (
          <div className="card">
            <h2>No apps yet</h2>
            <p className="muted">Create a chatbot, chatflow, workflow, or agent to start.</p>
          </div>
        )}
      </div>
    </Shell>
  )
}

