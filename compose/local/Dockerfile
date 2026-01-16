FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y gettext && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/local.txt .
RUN pip install -r local.txt
COPY . .

RUN sed -i 's/\r$//' wait-for-it.sh \
    && chmod +x wait-for-it.sh

EXPOSE 8000
