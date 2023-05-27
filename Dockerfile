# using py310 image because cchardet does not work with py311
FROM ghcr.io/divkix/docker-python-base:py310 AS build
WORKDIR /app
COPY . .
RUN apt-get update \
    && apt-get install --no-install-suggests --no-install-recommends --yes \
    poppler-utils \
    && apt-get clean \
    && apt-get autoremove --purge --yes \
    && rm -rf /var/lib/apt/lists/* /root/* /tmp/* /var/cache/apt/archives/*.deb /tmp
RUN poetry install --no-dev --no-interaction --no-ansi \
    && rm -rf /root/.cache/pip /root/.cache/pypoetry
ENTRYPOINT ["poetry", "run"]
CMD ["python", "-m", "bots"]

LABEL org.opencontainers.image.authors="Divanshu Chauhan <divkix@divkix.me>"
LABEL org.opencontainers.image.url="https://divkix.me"
LABEL org.opencontainers.image.source="https://github.com/Divkix/UtilitiesRoBot"
LABEL org.opencontainers.image.title="Utilities Robot"
LABEL org.opencontainers.image.description="Utilities Robot Docker Image for Divkix"
LABEL org.opencontainers.image.vendor="Divkix"
