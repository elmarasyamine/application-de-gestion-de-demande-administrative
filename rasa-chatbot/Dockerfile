FROM rasa/rasa:3.6.20-full

USER root
WORKDIR /app

# Copy project files
COPY --chown=1001:1001 config.yml .
COPY --chown=1001:1001 domain.yml .
COPY --chown=1001:1001 credentials.yml .
COPY --chown=1001:1001 endpoints.yml .
COPY --chown=1001:1001 data/ ./data/
COPY --chown=1001:1001 models/ ./models/

USER 1001

# Expose Rasa port
EXPOSE 5005

# Run Rasa server
CMD ["run", "--enable-api", "--cors", "*", "--port", "5005", "--endpoints", "endpoints.yml"]
