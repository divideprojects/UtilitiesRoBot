FROM ghcr.io/divideprojects/docker-python-base:latest AS build
WORKDIR /app
RUN apt-get install -y apt-utils build-essential
RUN apt-get install libpq-dev python3-dev -y
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry export -f requirements.txt --without-hashes --output requirements.txt \
    && pip install --disable-pip-version-check -r requirements.txt
COPY . .
ENTRYPOINT ["python3"]
CMD ["-m", "bots"]
