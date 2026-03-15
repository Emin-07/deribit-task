FROM python:3.13-slim-bookworm

ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Сначала копируем файлы зависимостей (для кэширования слоев)
COPY pyproject.toml uv.lock ./

# Синхронизируем зависимости без копирования всего кода
RUN uv sync --frozen --no-install-project

COPY . .

EXPOSE 8000

RUN useradd -m appuser

RUN chmod +x entrypoint.sh && chown -R appuser:appuser /app

USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]