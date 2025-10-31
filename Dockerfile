FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements-dev.txt pyproject.toml setup.cfg README.md Makefile ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY demos ./demos
COPY docs ./docs
COPY data ./data

EXPOSE 7860

CMD ["python", "-m", "demos.gradio_interface"]
