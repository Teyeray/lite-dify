import { Shell } from '../components/shell'

export default function WorkflowPage() {
  return (
    <Shell>
      <div className="toolbar">
        <h1>Workflow</h1>
      </div>
      <div className="card">
        <h2>Runtime included</h2>
        <p className="muted">
          The first scaffold supports Start, LLM, and Answer nodes. The visual editor can be expanded here with React Flow.
        </p>
      </div>
    </Shell>
  )
}

