FROM python:3.13-slim AS builder

WORKDIR /app

# Dependency metadata first, so the layer is cached
COPY pyproject.toml ./

# CPU-only torch keeps the image reasonable
RUN pip install --no-cache-dir \
    torch \
    --index-url https://download.pytorch.org/whl/cpu

COPY src ./src

RUN pip install --no-cache-dir -e .


FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Application entry point (uvicorn imports `main:app`)
COPY main.py ./

RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
