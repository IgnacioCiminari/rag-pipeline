FROM python:3.11-slim

# Install system dependencies required by docling and opencv
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install opendataloader-pdf with hybrid extras
RUN pip install --no-cache-dir -U "opendataloader-pdf[hybrid]"

EXPOSE 5002

CMD ["opendataloader-pdf-hybrid", "--host", "0.0.0.0", "--port", "5002"]
