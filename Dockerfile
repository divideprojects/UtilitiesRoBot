FROM debian:11-slim AS build
RUN apt-get update \
    && apt-get upgrade --yes \
    && apt-get install --no-install-suggests --no-install-recommends --yes \
    python3-venv \
    gcc \
    libpython3-dev \
    g++ \
    && python3 -m venv /venv \
    && /venv/bin/pip install --upgrade pip setuptools wheel poetry==1.1.11

# Install external packages in base image
FROM build as deb-extractor
RUN cd /tmp \
    && apt-get download $(apt-cache depends --recurse --no-recommends --no-suggests \
    --no-conflicts --no-breaks --no-replaces --no-enhances \
    --no-pre-depends poppler-utils | grep "^\w") \
    && mkdir /dpkg \
    && for deb in *.deb; do dpkg --extract $deb /dpkg || exit 10; done

# Build virtualenv as separate step: Only re-execute this step when pyproject.toml or poetry.lock changes
FROM build AS build-venv
COPY pyproject.toml poetry.lock /
RUN /venv/bin/poetry export -f requirements.txt --output requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Copy the virtualenv into a distroless image
FROM gcr.io/distroless/python3-debian11
WORKDIR /app
COPY --from=deb-extractor /dpkg /
COPY --from=build-venv /venv /venv
COPY . .
ENTRYPOINT ["/venv/bin/python3", "-m", "bots"]
