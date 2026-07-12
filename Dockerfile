FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies for OpenCV and Tesseract OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements first to leverage Docker cache
COPY backend/requirements.txt /app/backend/requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy configuration, source modules, and backend code
COPY config.py /app/config.py
COPY src/ /app/src/
COPY backend/ /app/backend/

# Create data directories for uploads, results, and temp files
RUN mkdir -p /app/data/uploads /app/data/results /app/data/temp

# Expose FastAPI default port
EXPOSE 8000

# Set environment variables for database (render will override this)
ENV DATABASE_URL=sqlite:////app/data/invoiscope.db

# Command to run the application
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
