# -------- Stage 1: Build Image --------
FROM python:3.10-slim AS builder

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt


# -------- Stage 2: Runtime Image --------
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl


# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy the entire app folder into the container
COPY app /app/app

# Copy .env file
COPY .env /app/.env

EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1
