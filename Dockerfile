# using py310 image because cchardet does not work with py311
FROM ghcr.io/divkix/docker-python-base:py310 AS build
WORKDIR /app
COPY . .
RUN poetry install --no-dev --no-interaction --no-ansi \
    && rm -rf /root/.cache/pip /root/.cache/pypoetry
ENTRYPOINT ["poetry", "run"]
CMD ["python", "-m", "bots"]

LABEL org.opencontainers.image.authors="Divanshu Chauhan <me@divkix.me>"
LABEL org.opencontainers.image.url="https://divkix.me"
LABEL org.opencontainers.image.source="https://github.com/Divkix/UtilitiesRoBot"
LABEL org.opencontainers.image.title="Utilities Robot"
LABEL org.opencontainers.image.description="Utilities Robot Docker Image for Divkix"
LABEL org.opencontainers.image.vendor="Divkix"
