# Environment Variables for YouTube AI App v2.5

## Main App
- `TTS_PROVIDER` (e.g., elevenlabs, gtts)
- `TTS_VOICE` (e.g., Adam, default)
- `ADVANCED_VIDEO` (true/false)
- `MOTION_FOOTAGE_DIR` (path to motion footage)
- `MUSIC_PATH` (path to background music)
- `YOUTUBE_API_KEY` (YouTube Data API key)

## Mini App
- See mini_app/README.md for any additional variables.

## GitHub Actions
- Add all secrets (API keys, etc.) in the repo settings under Settings > Secrets and variables > Actions.

## Google Cloud
- Set environment variables in your deployment configuration (see gcloud/README.md).

---

For more details, see the main `README.md` or contact the project owner. 