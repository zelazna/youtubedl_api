FROM python:3.10.0

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN mkdir /static
RUN --mount=type=cache,target=/root/.cache/pip pip install -e .
ENTRYPOINT [ "uvicorn", "server.main:app", "--reload" ]
