# Stage 1: Build the frontend assets
FROM node:18-alpine AS builder

# Set the working directory for the frontend app
WORKDIR /app/frontend/dev_dashboard

# Copy package.json and yarn.lock to leverage Docker layer caching
COPY frontend/dev_dashboard/package.json frontend/dev_dashboard/yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile

# Copy the rest of the frontend source code
COPY frontend/dev_dashboard/ ./

# Build the React app for production
RUN yarn build

# ---

# Stage 2: Build the final application image
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required by the application
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY app/requirements.txt ./app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r app/requirements.txt

# Copy the entire application source code into the image
COPY . .

# Copy the built frontend assets from the 'builder' stage
COPY --from=builder /app/frontend/dev_dashboard/build /app/app/static

# Expose the port the app runs on and define the startup command
EXPOSE 8000
CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]