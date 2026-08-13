FROM maven:3.9-eclipse-temurin-17 AS java-builder
WORKDIR /build

# Copy the entire repository
COPY . .

# Build the Java project
WORKDIR /build/java
RUN mvn clean package -DskipTests

# Stage 2: Final runtime image
FROM python:3.11-slim

# Install system dependencies required for Java, Docling, OpenCV, PyTorch, and Tesseract
RUN apt-get update && apt-get install -y \
    default-jre-headless \
    git \
    g++ \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-spa \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the repository
COPY . /app

# Copy the built JARs from the builder stage to their expected location
COPY --from=java-builder /build/java/opendataloader-pdf-cli/target/opendataloader-pdf-cli-*.jar /app/java/opendataloader-pdf-cli/target/

# Copy README to the python package directory as expected by hatchling
RUN cp /app/README.md /app/python/opendataloader-pdf/

# Install the python package with hybrid dependencies
WORKDIR /app/python/opendataloader-pdf
RUN pip install --no-cache-dir ".[hybrid]"

# Expose the default port for the hybrid server
EXPOSE 5002

# Set the working directory to the root of the app
WORKDIR /app

# Run the hybrid server by default, binding to all interfaces
CMD ["opendataloader-pdf-hybrid", "--host", "0.0.0.0", "--port", "5002"]
