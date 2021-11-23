FROM ghcr.io/divideprojects/telegram-bot-docker:latest

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install --no-dev --no-interaction --no-ansi && rm -rf /root/.cache

COPY . .

CMD ["make", "run"]
