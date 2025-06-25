# Setup Guide for YouTube AI App v2.5

## 1. Prerequisites
- Python 3.10+
- Node.js (for frontend)
- ffmpeg (for video/audio processing)

## 2. Environment Setup
- Clone or unzip the repository.
- (Recommended) Create and activate a Python virtual environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

## 3. Install Dependencies
- Main app:
  ```bash
  pip install -r app/requirements.txt
  ```
- Mini app:
  ```bash
  pip install -r mini_app/requirements.txt
  ```
- Frontend:
  ```bash
  cd frontend
  npm install
  ```

## 4. Environment Variables
- Copy `env.template` to `.env` and fill in required API keys and settings.
- For GitHub Actions, add secrets in the repo settings.

## 5. First Run
- Main app pipeline:
  ```bash
  python -m app.cli autoproduce --advanced
  ```
- Mini app pipeline:
  ```bash
  python mini_app/app/main.py
  ```
- Frontend:
  ```bash
  cd frontend
  npm start
  ```

## 6. Testing
- (If tests are present) Run tests:
  ```bash
  pytest app/tests/
  ```

## 7. Deployment
- See `gcloud/README.md` for Google Cloud deployment.

---

For more details, see the main `README.md` or contact the project owner. 