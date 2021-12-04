FROM python:3.10.0

ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install ffmpeg -y
RUN mkdir /files
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "uvicorn", "server.main:app", "--reload", "--host", "0.0.0.0" ]
