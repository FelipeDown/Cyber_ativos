FROM python:3.11-slim
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app/
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
