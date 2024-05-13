FROM python:3.10-slim-bullseye

RUN pip install poetry

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ADD pyproject.toml /app/
ADD poetry.lock /app/


RUN poetry install --without dev

EXPOSE 8000

ADD ./src /app/src
ADD ./settings.toml /app/settings.toml

ENV PYTHONPATH=src

ENTRYPOINT ["poetry", "run", "python", "-m", "uvicorn", "api_service.__main__:app", "--host", "0.0.0.0", "--port", "8000"]
