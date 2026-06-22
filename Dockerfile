FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ /app/
WORKDIR /app

EXPOSE 8000

CMD ["sh", "-c", "uv run python manage.py migrate && uv run python manage.py generate_data && uv run python manage.py runserver 0.0.0.0:8000"]
