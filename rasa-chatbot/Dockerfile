FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Rasa
RUN pip install --no-cache-dir rasa==3.6.20

# Copy project files
COPY config.yml .
COPY domain.yml .
COPY credentials.yml .
COPY data/ ./data/

# Copy pre-trained model
COPY models/ ./models/

# Expose Rasa port
EXPOSE 5005

# Run Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005"]
