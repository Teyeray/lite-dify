# Startup

This guide starts Lite Dify from a clean code-server machine.

## Prerequisites

- Python 3.12
- Node.js and pnpm
- Redis installed and running
- `uv`

## 1. Install Runtime Tools

```bash
conda create -n lite-dify python=3.12 -c conda-forge
conda activate lite-dify
conda install -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge redis-server -y
```

## 2. Start Redis

Lite Dify uses Redis as its only persistence store in the first version.

```bash
mkdir -p ~/data/lite-dify-redis
redis-server --dir ~/data/lite-dify-redis --appendonly yes --port 16379
```

Or from the project directory:

```bash
make redis-start
```

## 3. Install Dependencies

```bash
make install
```

## 4. Create Environment

For normal local development:

```bash
make local-env
```

For code-server:

```bash
make codeserver-env
```

`make codeserver-env` reads `$VSCODE_PROXY_URI` and writes the correct public API and web URLs.

You can also use:

```bash
make env
```

`make env` uses code-server settings when `$VSCODE_PROXY_URI` exists and local settings otherwise.

## 5. Start

```bash
make redis-start
make dev
```

Open the URL printed by `make codeserver-env` when running in code-server.

Default ports are intentionally separated from the original Dify project:

- Web: `13080`
- API: `18080`
- Redis: `16379`
