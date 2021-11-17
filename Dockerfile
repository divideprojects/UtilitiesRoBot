FROM python:3.10-slim-buster
ENV FASTAPI_ENV=production

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install and setup poetry
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    cmake \
    curl \
    debian-archive-keyring \
    debian-keyring \
    ffmpeg \
    gcc \
    git \
    gnupg \
    jq \
    libatlas-base-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavformat-dev \
    libavutil-dev \
    libboost-python-dev \
    libcurl4-openssl-dev \
    libffi-dev \
    libgconf-2-4 \
    libgtk-3-dev \
    libjpeg-dev \
    libjpeg62-turbo-dev \
    libopus-dev \
    libopus0 \
    libpq-dev \
    libreadline-dev \
    libswresample-dev \
    libswscale-dev \
    libssl-dev \
    libwebp-dev \
    libx11-dev \
    libxi6 \
    libxml2-dev \
    libxslt1-dev \
    libyaml-dev \
    linux-headers-amd64 \
    make \
    mediainfo \
    megatools \
    meson \
    musl \
    musl-dev \
    neofetch \
    netcat \
    ninja-build \
    openssh-client \
    openssh-server \
    openssl \
    p7zip-full \
    pdftk \
    pkg-config \
    procps \
    python3-dev \
    texinfo \
    unzip \
    util-linux \
    wget \
    wkhtmltopdf \
    xvfb \
    yasm \
    zip \
    zlib1g \
    zlib1g-dev \
    && apt-get autoremove --purge \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install --no-dev --no-interaction --no-ansi && rm -rf /root/.cache

COPY . .

CMD ["make", "run"]
