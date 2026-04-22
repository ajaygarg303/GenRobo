# Business Chatbot (OpenAI API, Docker, AWS-friendly)

Multi-tenant demo: each **business** has a **slug** (URL), **theme** (colors, welcome text), **FAQ text**, and **transcript email**. The API can call the **OpenAI API**; if `OPENAI_API_KEY` is omitted, replies are **mock** (for cheap testing).

## What you get

- **FastAPI** backend: `/api/tenants/by-slug/{slug}`, `/api/sessions`, chat turns, end session.
- **React (Vite)** UI: open `/b/demo` (seeded tenant).
- **SQLite** by default; optional **PostgreSQL** (e.g. Amazon RDS) via `DATABASE_URL`.
- **Docker** image: builds the web app and serves API + static files on port **8000**.

## Quick start (local)

### 1. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Use a **dedicated venv** so this app’s dependencies do not clash with other global Python packages on your machine.

Copy `..\.env.example` to `backend\.env` and adjust if needed (optional OpenAI).

```powershell
mkdir data 2>$null
$env:DATABASE_URL="sqlite+aiosqlite:///./data/app.db"
```

**Prefer the helper script** (correct reload scope on Windows):

```powershell
.\run-dev.ps1
```

Or manually:

```powershell
python -m uvicorn app.main:app --reload --reload-dir app --reload-exclude ".venv" --reload-exclude "data/**" --host 127.0.0.1 --port 8000
```

In Cursor: **Terminal → Run Task…** → **API: Uvicorn (reload app only)**.

`--reload-dir app` stops Uvicorn from watching **`.venv`**. If you run plain `--reload` from the `backend` folder, WatchFiles will see thousands of changes under `.venv` and you get endless reloads and `CancelledError` spam.

Open `http://127.0.0.1:8000/docs` for OpenAPI.

### 2. Frontend (development)

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Vite proxies `/api` to `http://127.0.0.1:8000`. Open the URL Vite prints (e.g. `http://127.0.0.1:5173/b/demo`).

### 3. Single origin (API serves the built UI)

After `npm run build` in `frontend` (requires **Node.js** installed), copy the build into the API static folder:

```powershell
Copy-Item -Recurse -Force frontend\dist\* backend\app\static\
```

If you do not have Node locally, run **`docker compose build`** once; the image build step runs `npm run build` inside Docker. You can copy `static` out of the image, or rely on Docker for end-to-end testing.

Run `python -m uvicorn` from `backend` as above, then open `http://127.0.0.1:8000/b/demo`.

## Docker (local)

From the repo root:

```powershell
docker compose up --build
```

Browse `http://localhost:8000/b/demo`. Data persists in the `sqlite_data` volume.

Set OpenAI in a `.env` file next to `docker-compose.yml` (see `.env.example`) or export variables before `docker compose up`.

## OpenAI API

1. Create an API key in the [OpenAI dashboard](https://platform.openai.com/api-keys).
2. Set:

- `OPENAI_API_KEY` — required for real replies
- `OPENAI_MODEL` — defaults to `gpt-4o-mini` if unset
- `OPENAI_BASE_URL` — optional; only if you use an OpenAI-compatible proxy or hosted gateway

Without `OPENAI_API_KEY`, the bot returns a short **mock** reply so you can test without spend.

## Deploy on AWS with ECS (outline)

Typical path for this **single container**:

1. **Amazon ECR** — push an image built from the repo root `Dockerfile` (`docker build -t ... .`).
2. **Amazon ECS on Fargate** — task definition: one container, port **8000**, CPU/memory for your traffic; environment variables from **Secrets Manager** or **SSM Parameter Store** (especially `OPENAI_API_KEY`, `DATABASE_URL`).
3. **Application Load Balancer** — target group → ECS service on port 8000; health check on **`/api/health`** (or `/docs` if you enable docs).
4. **RDS PostgreSQL** (recommended for production):  
   `DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:5432/DBNAME?ssl=require`  
   SQLite on Fargate without persistent storage will reset on redeploy.
5. **CORS**: if the browser origin differs from the API, set `CORS_ORIGINS` to that origin (comma-separated).
6. **Outbound internet**: tasks in private subnets need **NAT** (or public subnet + public IP) so the app can reach `api.openai.com`.

Wire **GitHub Actions** (or CodePipeline) to build, push to ECR, and **`ecs:UpdateService`** after each merge to `main`, using **OIDC** for AWS credentials instead of long-lived keys.

## Transcripts

On session end (user **End chat**, idle **timeout**, or timeout on next message), the server **logs** the full transcript. If you set **SMTP** (`SMTP_HOST`, `SMTP_PORT`, etc.), it also emails `transcript_email` on the tenant (see seeded `demo` tenant in `app/seed.py`).

## Seeded tenant

Slug **`demo`** — adjust in `backend/app/seed.py` or add rows via SQL/admin later.

## Troubleshooting

### `npm` is not recognized (frontend)

Install **Node.js LTS** from [https://nodejs.org](https://nodejs.org), then **close and reopen** the terminal (or Cursor) so `npm` is on your `PATH`. Alternatively use **Docker** to build the UI (`docker compose build`) without installing Node locally.

### Uvicorn reload loop / `CancelledError` / `WatchFiles detected changes in '.venv\...'`

1. **Stop** the old server (Ctrl+C in that terminal).
2. Start with **`.\run-dev.ps1`** from the `backend` folder, or the **Run Task** above — do **not** use bare `python -m uvicorn ... --reload` without `--reload-dir app`.
3. If it still misbehaves, your repo may be under **OneDrive** (constant file sync). Exclude the `backend\.venv` folder from sync, or move the project to a non-synced folder (e.g. `C:\dev\...`).
4. Last resort: no reload — `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`.
