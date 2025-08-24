FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl tzdata ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:/root/.uv/bin:${PATH}"

WORKDIR /app

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:${PATH}"

COPY src ./src
COPY .env.production .env.development ./
COPY ./ ./

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
    
CMD ["python", "src/main.py"]