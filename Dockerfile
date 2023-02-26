# using py310 image because cchardet does not work with py311
FROM ghcr.io/divkix/docker-python-base:py310 AS build
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /app
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry export -f requirements.txt --without-hashes --output requirements.txt \
    && pip install --disable-pip-version-check -r requirements.txt
COPY . .
ENTRYPOINT ["python3"]
CMD ["-m", "bots"]
