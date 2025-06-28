# --- Builder Stage ---
# This stage installs dependencies into a virtual environment.
FROM python:3.10-slim as builder

# Set the working directory in the container
WORKDIR /usr/src/app

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# --- Production Stage ---
# This stage creates the final, smaller image.
FROM python:3.10-slim
WORKDIR /usr/src/app

# Install system dependencies: ffmpeg for moviepy, redis for the broker, supervisor for process management
RUN apt-get update && apt-get install -y ffmpeg redis-server supervisor && rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the application
RUN useradd --create-home appuser

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY entrypoint.sh /usr/src/app/entrypoint.sh

# Set environment and permissions
ENV PATH="/opt/venv/bin:$PATH"
RUN chmod +x /usr/src/app/entrypoint.sh
RUN chown -R appuser:appuser /usr/src/app
USER appuser

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run the application
CMD ["/usr/src/app/entrypoint.sh"]