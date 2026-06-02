import { Shell } from '../components/shell'

export default function AgentPage() {
  return (
    <Shell>
      <div className="toolbar">
        <h1>Agent</h1>
      </div>
      <div className="card">
        <h2>Agent loop placeholder</h2>
        <p className="muted">
          The backend has an agent runtime boundary. Tool calling can be added without introducing a plugin daemon.
        </p>
      </div>
    </Shell>
  )
}

