import { Bot, GitBranch, LayoutDashboard, Workflow } from 'lucide-react'
import Link from 'next/link'

export function Shell({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <div className="shell">
      <aside className="sidebar">
        <p className="brand">Lite Dify</p>
        <nav className="nav">
          <Link href="/">
            <LayoutDashboard size={18} />
            Apps
          </Link>
          <Link href="/chat">
            <Bot size={18} />
            Chat
          </Link>
          <Link href="/workflow">
            <Workflow size={18} />
            Workflow
          </Link>
          <Link href="/agent">
            <GitBranch size={18} />
            Agent
          </Link>
        </nav>
      </aside>
      <main className="main">{children}</main>
    </div>
  )
}

