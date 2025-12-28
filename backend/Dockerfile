# Use Python 3.11
FROM python:3.11-slim

# Install FFmpeg and system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set the port (Railway uses $PORT)
ENV PORT=8080

# Start the app
# We use sh -c to force the shell to process the $PORT variable
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT} --timeout 180 --workers 1"]