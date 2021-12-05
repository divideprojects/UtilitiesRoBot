##
## Utilities Robot - All in one Utilities Bot of Telegram
## Copyright (C) 2021 Divide Projects <https://github.com/DivideProjects>
##
## This file is part of Utilities Robot.
##
## Utilities Robot is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published
## by the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Utilities Robot is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with Utilities Robot.  If not, see <http://www.gnu.org/licenses/>.
##
FROM ghcr.io/divideprojects/docker-python-base:latest AS build

# Install external packages in base image
FROM build as deb-extractor
RUN cd /tmp \
    && apt-get update \
    && apt-get download $(apt-cache depends --recurse --no-recommends --no-suggests \
    --no-conflicts --no-breaks --no-replaces --no-enhances \
    --no-pre-depends poppler-utils | grep "^\w") \
    && mkdir /dpkg \
    && for deb in *.deb; do dpkg --extract $deb /dpkg || exit 10; done

# Build virtualenv as separate step: Only re-execute this step when pyproject.toml or poetry.lock changes
FROM build AS build-venv
COPY pyproject.toml poetry.lock /
RUN /venv/bin/poetry export -f requirements.txt --without-hashes --output requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Copy the virtualenv into a distroless image
FROM gcr.io/distroless/python3-debian11
WORKDIR /app
COPY --from=deb-extractor /dpkg /
COPY --from=build-venv /venv /venv
COPY . .
ENTRYPOINT ["/venv/bin/python3"]
CMD ["-m", "bots"]
