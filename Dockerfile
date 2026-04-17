# Multi-stage build for smaller image
FROM python:3.11-slim as builder

WORKDIR /app

# Copy dependencies first for better caching
COPY requirements.txt .

# Install dependencies with pip
RUN pip install --user --no-cache-dir -r requirements.txt


# ============== FINAL STAGE ==============
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Set PATH to use local pip packages
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy entire project
COPY . .

# Verify model file exists (fail fast)
RUN test -f models/xgb_model.pkl || (echo "ERROR: models/xgb_model.pkl not found!" && exit 1)

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5)" || exit 1

# Expose port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]