ARG DOCKER_IMAGE=docker:23.0
FROM ${DOCKER_IMAGE} as docker
FROM ubuntu:22.04 as base

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    git \
    openssh-client \
    python3 \
    python3-dev \
    python3-pip \
    sshpass \
    sudo \
 && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache poetry==1.3.2

COPY --from=docker /usr/local/bin/docker /usr/local/bin/docker
# docker-compose and docker-buildx (unused)
COPY --from=docker /usr/libexec/docker/cli-plugins/ /usr/libexec/docker/cli-plugins/
