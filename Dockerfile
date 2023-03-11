FROM python:3.9.1-slim

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONUNBUFFERED 1
RUN apt-get -qq update && apt install --no-install-recommends -y curl libmagickwand-dev wget make wait-for-it && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.create false && \
    poetry self update && \
    mkdir app
WORKDIR /app
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install --no-root
COPY . .
CMD ["python", "bot.py"]