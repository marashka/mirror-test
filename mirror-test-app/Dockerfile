FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

WORKDIR app

COPY ./poetry.lock ./pyproject.toml ./

RUN pip install poetry

RUN poetry install

COPY . .

RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
