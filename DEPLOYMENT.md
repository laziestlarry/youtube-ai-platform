# Deployment Guide for YouTube AI App v2.5

## 1. Local Deployment

### Prerequisites
- Python 3.10+
- Node.js (for frontend)
- ffmpeg (required for video/audio processing)

#### Install ffmpeg
- **macOS (Homebrew):**
  ```bash
  brew install ffmpeg
  ```
- **Ubuntu/Debian:**
  ```bash
  sudo apt-get update && sudo apt-get install ffmpeg
  ```
- **Windows:**
  - Download from https://ffmpeg.org/download.html and add to PATH.

### Run Locally
```bash
chmod +x start.sh
./start.sh
```

---

## 2. Docker Deployment

### Dockerfile Example
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y ffmpeg && \
    pip install --upgrade pip && \
    pip install -r app/requirements.txt && \
    pip install -r mini_app/requirements.txt
CMD ["bash", "start.sh"]
```

### Build and Run
```bash
docker build -t youtube-ai-app-v2.5 .
docker run --env-file .env -it youtube-ai-app-v2.5
```

---

## 3. Google Cloud Deployment

### App Engine (Flexible)
- Use the Dockerfile above and deploy with:
  ```bash
  gcloud app deploy
  ```

### Cloud Run
- Build and push the image:
  ```bash
  gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/youtube-ai-app-v2-5
  gcloud run deploy --image gcr.io/YOUR_PROJECT_ID/youtube-ai-app-v2-5 --platform managed
  ```

---

## 4. GitHub Actions (CI/CD)
- Ensure `.github/workflows/ci.yml` and other workflows are present.
- Add all required secrets (API keys, etc.) in GitHub repo settings.
- Workflows will run on push, PR, and on schedule.

---

For more details, see the main `README.md` or contact the project owner. 