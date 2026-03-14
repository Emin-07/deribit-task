FROM python:3.13-trixie

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install uv && \
    uv --version

WORKDIR /app

COPY pyproject.toml .

RUN uv sync

COPY . .

EXPOSE 8000

RUN useradd -m appuser

USER appuser

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]