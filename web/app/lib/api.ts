const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export type AppMode = 'chatbot' | 'chatflow' | 'workflow' | 'agent'

export type WorkflowNode = {
  id: string
  type: 'start' | 'llm' | 'answer' | 'http' | 'code' | 'tool'
  title: string
  config: Record<string, string>
}

export type WorkflowGraph = {
  nodes: WorkflowNode[]
  edges: Array<{ source: string; target: string }>
}

export type AppDefinition = {
  id: string
  name: string
  mode: AppMode
  description: string
  model?: string | null
  system_prompt: string
  workflow: WorkflowGraph
}

export type RunResult = {
  conversation: { id: string; app_id: string; title: string }
  answer: { id: string; role: string; content: string }
  trace: Array<{ node_id: string; node_type: string; status: string; input: string; output: string }>
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...init,
    headers: {
      'content-type': 'application/json',
      ...init?.headers,
    },
    cache: 'no-store',
  })
  if (!response.ok)
    throw new Error(await response.text())
  return response.json() as Promise<T>
}

export function listApps() {
  return request<AppDefinition[]>('/apps')
}

export function createApp(payload: {
  name: string
  mode: AppMode
  description?: string
  system_prompt?: string
  workflow?: WorkflowGraph
}) {
  return request<AppDefinition>('/apps', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function sendChat(appId: string, query: string, conversationId?: string) {
  return request<RunResult>(`/apps/${appId}/chat`, {
    method: 'POST',
    body: JSON.stringify({ query, conversation_id: conversationId }),
  })
}

