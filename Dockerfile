FROM python:3.12 AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN python -m venv /venv
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

### Production image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /venv/ /venv/
COPY ./src/ /app/

EXPOSE 5000

CMD ["/venv/bin/hypercorn", "-w", "5", "-b", "0.0.0.0:5000", "server:app"]
