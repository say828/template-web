FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY api ./api
COPY contexts ./contexts
COPY shared ./shared
COPY data ./data
COPY config.py ./config.py
COPY main.py ./main.py
COPY tests ./tests
COPY .env.example ./.env.example

RUN pip install --no-cache-dir -e ".[dev]"

EXPOSE 8000

CMD ["uvicorn", "api.http.app:app", "--host", "0.0.0.0", "--port", "8000"]
