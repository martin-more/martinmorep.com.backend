# pull official base image
FROM python:3.10.7-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

# install system dependencies
RUN apt-get update && apt-get install netcat curl make -y

# install dependencies
RUN pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock ./
COPY pyproject.toml ./

RUN poetry install --no-root

# copy project
COPY . /

RUN chmod +x /migrate.sh /entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
