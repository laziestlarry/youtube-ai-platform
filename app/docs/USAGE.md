# Usage Guide for YouTube AI App v2.5

## Main App

### CLI Pipeline
- Run the full pipeline (advanced mode):
  ```bash
  python -m app.cli autoproduce --advanced
  ```
- Run the full pipeline (basic mode):
  ```bash
  python -m app.cli autoproduce
  ```

### API (if backend is running)
- Start backend API:
  ```bash
  uvicorn app.backend.main:app --reload
  ```
- Access endpoints (see app/backend/api/ for available routes):
  - `/api/videos/`
  - `/api/analytics/`
  - `/api/agents/`
  - `/api/channels/`
  - `/api/users/`

## Mini App
- Run the mini app pipeline:
  ```bash
  python mini_app/app/main.py
  ```
- See mini_app/scripts/ for additional scripts.

## Frontend
- Start the frontend UI:
  ```bash
  cd frontend
  npm start
  ```
- Access the workflow dashboard and video management tools.

## Automation
- GitHub Actions workflows are in `.github/workflows/`.
- Scheduled and CI/CD runs are automated on push and on schedule.

---

For more details, see the main `README.md` or contact the project owner. 