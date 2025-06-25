# YouTube AI Platform Launch Guide

## 📋 Overview

The YouTube AI Platform is an integrated system for YouTube content creation, analytics, and monetization. It consists of:

- **Main Application**: Core content creation and analytics pipeline
- **Mini App**: Supplementary tools for income projection and rapid content creation
- **Backend API**: Serves data to frontend and manages system operations
- **Frontend UI**: User interface for interacting with the platform

## 🖥️ System Requirements

- **Operating System**: macOS, Linux, or Windows with WSL
- **Python**: 3.8 or higher
- **Node.js**: 14.x or higher
- **npm**: 6.x or higher
- **ffmpeg**: Latest version (required for video/audio processing)
- **Storage**: At least 5GB free space
- **Memory**: Minimum 8GB RAM (16GB+ recommended)
- **API Keys**: Various third-party API keys (see below)

## 🔑 Required API Keys

The platform integrates with several external services that require API keys:

| API Key | Purpose | Where to Get |
|---------|---------|--------------|
| `OPENAI_API_KEY` | AI content generation | [OpenAI Platform](https://platform.openai.com/account/api-keys) |
| `YOUTUBE_CLIENT_ID` & `SECRET` | YouTube API access | [Google Cloud Console](https://console.cloud.google.com/) |
| `GEMINI_API_KEY` | Alternative AI model | [Google AI Studio](https://makersuite.google.com/) |
| `MIDJOURNEY_API_KEY` | Thumbnail generation | Midjourney API Dashboard |
| `STRIPE_API_KEY` | Payment processing | [Stripe Dashboard](https://dashboard.stripe.com/apikeys) |
| `SHOPIFY_API_KEY` | E-commerce integration | [Shopify Partner Dashboard](https://partners.shopify.com/) |
| `PAYONEER_CUSTOMER_ID` | Payment processing | Payoneer Business Account |
| `FREELANCER_ACCESS_TOKEN` | Outsourcing integration | Freelancer Developer Portal |

## ⚙️ First-Time Setup

### 1. Clone the repository (if you haven't already)

```bash
git clone <repository-url>
cd youtube_ai_app_v2.5
```

### 2. Set up environment variables

Create a `.env` file in the project root by copying the template:

```bash
cp env.template .env
```

Then edit the `.env` file to add your API keys:

```
OPENAI_API_KEY=your_openai_key_here
YOUTUBE_CLIENT_ID=your_youtube_client_id_here
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret_here
# ... add all other required API keys
```

### 3. Install dependencies

The launch script will handle most dependency installation, but you need to ensure the following are installed system-wide:

#### macOS:

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install python3 node npm ffmpeg
```

#### Ubuntu/Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nodejs npm ffmpeg
```

## 🚀 Launching the Platform

### Standard Launch (All Components)

To launch the entire platform with all components:

```bash
./start.sh
```

This will:
1. Check prerequisites
2. Set up the Python virtual environment
3. Install all dependencies
4. Initialize the database
5. Start the backend, frontend, and mini-app services
6. Run the main and mini application pipelines
7. Perform health checks

### Component-Specific Launch

If you want to run only specific components, you can use these environment variables:

```bash
# Launch only the backend and frontend (no pipelines)
SKIP_PIPELINES=true ./start.sh

# Launch only the main pipeline (no UI components)
SKIP_UI=true SKIP_MINI=true ./start.sh
```

## 📊 Accessing the Platform

After successful launch, you can access the platform through:

- **Frontend UI**: http://localhost:3001
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Mini App**: http://localhost:5050

## 📁 Directory Structure

```
youtube_ai_app_v2.5/
├── app/                    # Main application
│   ├── cli.py              # Command-line interface
│   ├── full_pipeline.py    # End-to-end pipeline
│   └── ...
├── backend/                # Backend API
├── frontend/               # Frontend UI
├── mini_app/               # Mini application
├── logs/                   # Log files directory
├── outputs/                # Generated content
├── .env                    # Environment variables
└── start.sh                # Launch script
```

## 📋 Log Files

The platform generates several log files to help with monitoring and troubleshooting:

- `logs/startup.log`: Overall startup process logs
- `logs/backend.log`: Backend API server logs
- `logs/frontend.log`: Frontend server logs
- `logs/mini-app.log`: Mini app server logs
- `logs/main_pipeline.log`: Main application pipeline logs
- `logs/mini_app_pipeline.log`: Mini app pipeline logs

## ❓ Troubleshooting

### Common Issues

#### "Missing API key" error
- Ensure all required API keys are properly set in your `.env` file
- Check for typos or extra spaces in your API keys

#### Service fails to start
- Check the corresponding log file in the `logs` directory
- Ensure all dependencies are correctly installed
- Verify that the required ports (8000, 3001, 5050) are not in use by other applications

#### Pipeline errors
- Check the pipeline logs (`logs/main_pipeline.log` or `logs/mini_app_pipeline.log`)
- Ensure ffmpeg is properly installed and in your PATH
- Verify that all required API keys are valid and have sufficient quota/credits

#### Database issues
- Delete the database file (`youtube_ai.db`) and restart to reinitialize
- Check permissions on the database file and directory

### Advanced Troubleshooting

For more complex issues:

1. Enable debug mode:
   ```bash
   DEBUG=true ./start.sh
   ```

2. Check system resources:
   ```bash
   # Check disk space
   df -h
   
   # Check memory usage
   free -m
   ```

3. Restart with clean slate:
   ```bash
   # Remove virtual environment and database
   rm -rf venv youtube_ai.db
   
   # Restart
   ./start.sh
   ```

## 🛑 Stopping the Platform

To stop all running services and pipelines, press `Ctrl+C` in the terminal where you started the platform.

This will:
1. Stop all running services (backend, frontend, mini-app)
2. Terminate all running pipelines
3. Clean up temporary files and processes

## 🔄 Updating the Platform

To update to the latest version:

1. Pull the latest changes:
   ```bash
   git pull
   ```

2. Restart the platform:
   ```bash
   ./start.sh
   ```

## 📧 Support

If you encounter issues not covered by this guide, please contact support at:
- Email: support@youtubeaiplatform.com
- Issue Tracker: [GitHub Issues](https://github.com/youtubeaiplatform/issues)
