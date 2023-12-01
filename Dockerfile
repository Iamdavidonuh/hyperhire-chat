FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.7.0
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry config virtualenvs.create false


WORKDIR /hyperhire

COPY poetry.lock /hyperhire/
COPY pypoetry.toml /hyperhire/
RUN poetry install --no-root

COPY . /hyperhire/