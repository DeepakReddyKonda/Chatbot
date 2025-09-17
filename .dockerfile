# Use an official Python runtime as a parent image. We use a version
# based on Debian as it has a robust package manager (apt).
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system-level dependencies required by pdf2image and pytesseract.
# The --no-install-recommends flag keeps the image size small.
# The -y flag automatically confirms installation without user prompt.
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    libjpeg-dev \
    zlib1g-dev \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python packages
RUN pip install --no-cache-dir -r requirements.txt
