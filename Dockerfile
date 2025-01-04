# Get latest Python3
FROM python:latest

# Set the work directory inside the container
WORKDIR /usr/app/src

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Python Modules
COPY ./src/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Default command
CMD ["python3", "main.py"]
