# dingkwang-site

Personal homepage with an embedded AI chatbot powered by Claude Agent SDK.

## Architecture

```
Frontend (Next.js)          Backend (FastAPI)
Vercel                      Railway
     │                           │
     │   POST /api/chat (SSE)    │
     │ ─────────────────────────>│
     │ <─────────────────────────│  Claude Agent SDK
     │   data: {type, content}   │  + MCP Tools
```

- **Frontend**: Next.js + Tailwind CSS — personal homepage with floating chatbot panel
- **Backend**: FastAPI + `claude-agent-sdk` — streams responses via SSE, uses in-process MCP tools for project/resume data
- **Communication**: Server-Sent Events (SSE)

## Project Structure

```
dingkwang-site/
├── frontend/                 # Next.js app
│   ├── app/                  # Pages (App Router)
│   ├── components/           # ChatBot, Hero, Projects, TechStack, etc.
│   └── .env.local            # NEXT_PUBLIC_API_URL
├── backend/                  # FastAPI app
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── routers/chat.py   # SSE streaming endpoint
│   │   ├── agent/            # Claude SDK client, tools, system prompt
│   │   └── middleware/       # Rate limiting
│   ├── data/resume.md        # Resume data
│   ├── Dockerfile
│   └── .env                  # ANTHROPIC_API_KEY
└── docker-compose.yml
```

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (recommended)
- Anthropic API key

### Option 1: Docker (recommended)

```bash
# 1. Set up backend env
cp backend/.env.example backend/.env
# Edit backend/.env and add your ANTHROPIC_API_KEY

# 2. Build and run backend
cd backend
docker build -t dingkwang-backend .
docker run -d --name dingkwang-backend -p 8000:8000 --env-file .env dingkwang-backend

# 3. Run frontend
cd ../frontend
npm install
npm run dev
```

Open http://localhost:3000

### Option 2: Docker Compose

```bash
cp backend/.env.example backend/.env
# Edit backend/.env and add your ANTHROPIC_API_KEY

docker compose up
```

Open http://localhost:3000

## Deployment

### Backend → Railway

1. Go to [railway.com](https://railway.app) and sign in with GitHub
2. **New Project** → **Deploy from GitHub Repo** → select `dingkwang/dingkwang-site`
3. In **Settings**:
   - Set **Root Directory** to `backend/`
   - Railway will auto-detect the Dockerfile
4. In **Variables**, add:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```
5. Deploy. Note the generated URL (e.g. `https://dingkwang-site-xxx.up.railway.app`)

### Frontend → Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. **Import Project** → select `dingkwang/dingkwang-site`
3. In **Settings**:
   - Set **Root Directory** to `frontend/`
   - Framework Preset: Next.js (auto-detected)
4. In **Environment Variables**, add:
   ```
   NEXT_PUBLIC_API_URL=https://dingkwang-site-xxx.up.railway.app
   ```
5. Deploy

### Post-deployment

Update Railway's `ALLOWED_ORIGINS` to match your Vercel URL:
```
ALLOWED_ORIGINS=https://dingkwang-site.vercel.app
```

### Custom Domain (optional)

1. Purchase a domain from Cloudflare or Namecheap (~$10/year)
2. In Vercel: **Settings** → **Domains** → add your domain
3. Update DNS records as instructed by Vercel

## Environment Variables

| Variable | Location | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Backend | Anthropic API key |
| `ALLOWED_ORIGINS` | Backend | Comma-separated CORS origins |
| `RATE_LIMIT_PER_MINUTE` | Backend | Rate limit per IP (default: 10) |
| `NEXT_PUBLIC_API_URL` | Frontend | Backend API URL |

## Tech Stack

- **Frontend**: Next.js, React, Tailwind CSS, react-markdown, lucide-react
- **Backend**: FastAPI, claude-agent-sdk, uvicorn
- **AI**: Claude Agent SDK with in-process MCP tools
