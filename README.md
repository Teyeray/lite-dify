# Lite Dify

A lightweight Dify-like application focused on chatbot, chatflow, workflow, and agent apps.

This project is intentionally small:

- FastAPI backend
- Next.js frontend
- Redis as the only persistence store in the first version
- OpenAI-compatible model gateway
- No marketplace, plugin daemon, dataset, or vector store in the first version

## Status

This is an early runnable scaffold. It provides the core architecture and a mock LLM response path when no OpenAI-compatible API key is configured.

Implemented:

- Create apps in `chatbot`, `chatflow`, `workflow`, and `agent` modes
- Chat against an app
- Redis-backed app, conversation, and message repositories
- Basic workflow runtime with Start, LLM, and Answer nodes
- Agent runtime boundary for future tool calling
- code-server URL generation through `$VSCODE_PROXY_URI`

Not implemented yet:

- Authentication
- SQL database
- Visual workflow editor
- Tool calling loop
- Streaming responses
- Production deployment hardening

## Quick Start

```bash
cp .env.example .env
make install
make redis-start
make dev
```

For code-server environments, use:

```bash
make codeserver-env
make dev
```

See `docs/startup.md` for the full from-zero setup.

## Architecture

```text
api/
  app/api/              HTTP routes and request schemas
  app/core/             configuration
  app/domain/           entities and repository interfaces
  app/infrastructure/   Redis persistence
  app/runtime/          LLM, workflow, and agent execution
  app/services/         application use cases

web/
  app/                  Next.js app router pages
  app/lib/api.ts        API client and shared frontend types
```

The backend keeps repository interfaces separate from Redis implementations so another persistence layer can be added later without rewriting the service layer.

## Environment

Minimal `.env`:

```env
REDIS_URL=redis://127.0.0.1:6379/0
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
PUBLIC_API_URL=http://localhost:8000
PUBLIC_WEB_URL=http://localhost:3000
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-mini
```

When `OPENAI_API_KEY` is empty, the API returns mock responses so the app can be tested without a model provider.
