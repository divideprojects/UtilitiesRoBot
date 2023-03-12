# using py310 image because cchardet does not work with py311
FROM ghcr.io/divkix/docker-python-base:py310 AS build
WORKDIR /app
COPY . .
RUN poetry export -f requirements.txt --without-hashes --output requirements.txt \
    && pip install --disable-pip-version-check -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["-m", "bots"]
