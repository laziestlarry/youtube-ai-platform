# YouTube Channel Network Platform

[![CI/CD Pipeline](https://github.com/laziestlarry/youtubing_ai/actions/workflows/ci.yml/badge.svg)](https://github.com/laziestlarry/youtubing_ai/actions/workflows/ci.yml)
[![Deploy to Cloud Run](https://github.com/laziestlarry/youtubing_ai/actions/workflows/deploy.yml/badge.svg)](https://github.com/laziestlarry/youtubing_ai/actions/workflows/deploy.yml)

A quantum-inspired, event-driven platform for orchestrating YouTube content creation, collaboration, and automation at scale.

## Key Features
- **Channel-centric business network**: Channels are the atomic business unit, supporting collaboration, cross-promotion, and resource sharing.
- **Unified user/agent model**: Humans and AI agents are both users with dynamic, channel-specific roles.
- **Event-driven orchestration**: All business logic and workflows are triggered by events, enabling modularity, scalability, and resilience.
- **Marketplace-ready**: Channels can hire human or AI agents for any task, and talent can be dynamically assigned across the network.
- **Analytics-driven**: Every action is logged and used to optimize workflows, assignments, and business outcomes.

## Folder Structure
- `app/backend/` — FastAPI, SQLAlchemy, event bus, modular services, analytics
- `frontend/` — React/TypeScript, channel dashboard, workflow, user/agent management, analytics
- `app/scripts/` — DB init, seed, event simulation
- `app/docs/` — Architecture, API, business network, lessons learned
- `app/tests/` — Backend and frontend tests

## Quickstart

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (for deployment)

### Backend
```bash
python -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
uvicorn app.backend.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Environment Setup
- Copy `.env.example` to `.env` and fill in required variables (see `app/docs/ENVIRONMENT_VARIABLES.md`).
- Set up Google Cloud credentials for deployment (see below).

## Deployment

### GitHub Actions (Cloud Run)
- On push to `main`, GitHub Actions will build and deploy API, Worker, and Mini-App to Google Cloud Run.
- Configure secrets in your GitHub repo:
  - `GCP_PROJECT_ID`, `GCP_WIF_PROVIDER`, `GCP_SERVICE_ACCOUNT`, `API_SERVICE_ACCOUNT_EMAIL`, `WORKER_SERVICE_ACCOUNT_EMAIL`, etc.
- See `.github/workflows/deploy.yml` for details.

### Manual
```bash
gcloud builds submit --tag us-central1-docker.pkg.dev/<PROJECT_ID>/youtube-ai-platform/api:latest -f Dockerfile.api .
gcloud run deploy youtube-ai-platform --image us-central1-docker.pkg.dev/<PROJECT_ID>/youtube-ai-platform/api:latest --region us-central1
```

## Contribution Guidelines
- Fork the repo and create a feature branch.
- Write clear, concise commits and PRs.
- Run lint and tests before submitting.
- See `/app/docs/USAGE.md` and `/app/docs/SETUP.md` for more info.

## Documentation & Links
- [Architecture](app/docs/ARCHITECTURE.md) *(coming soon)*
- [Business Network](app/docs/BUSINESS_NETWORK.md) *(coming soon)*
- [Environment Variables](app/docs/ENVIRONMENT_VARIABLES.md)
- [Setup Guide](app/docs/SETUP.md)
- [Usage Guide](app/docs/USAGE.md)
- [Deployment](DEPLOYMENT.md)
- [Launch Guide](LAUNCH_GUIDE.md)
- [Open Issues](https://github.com/laziestlarry/youtubing_ai/issues)
- [Discussions](https://github.com/laziestlarry/youtubing_ai/discussions)

## Vision
This platform is engineered for business velocity, technical excellence, and future-proof growth in the YouTube content ecosystem. 