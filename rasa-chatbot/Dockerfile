FROM rasa/rasa:3.6.20-full

USER root
WORKDIR /app

# Copy project files
COPY --chown=1001:1001 config.yml .
COPY --chown=1001:1001 domain.yml .
COPY --chown=1001:1001 credentials.yml .
COPY --chown=1001:1001 endpoints.yml .
COPY --chown=1001:1001 data/ ./data/

USER 1001

# Train the model inside the container (ensures compatibility with Rasa 3.6.20)
RUN rasa train --config config.yml --domain domain.yml --data data/ --out models/

# Expose Rasa port
EXPOSE 5005

# Run Rasa server with explicit model path
CMD ["run", "--enable-api", "--cors", "*", "--port", "5005", "--model", "/app/models", "--endpoints", "/app/endpoints.yml"]
