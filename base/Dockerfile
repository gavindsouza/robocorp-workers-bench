# Select the base image
FROM ubuntu:18.04

ARG NAME
ARG LINK_TOKEN

# Set all variables that affect programs to follow the same encoding
ENV LANG=C.UTF-8 LANGUAGE=C.UTF-8 LC_ALL=C.UTF-8

# Install here all the software your process needs in order to execute
RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl bash chromium-browser chromium-chromedriver build-essential && \
    apt-get install -y fonts-indic fonts-noto fonts-noto-cjk && \
    apt-get install -y zip libdbus-glib-1-2 && \
    export PATH=$PATH:/usr/lib/chromium-browser/ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \
    echo "Chromium Version: " && chromium-browser --product-version && chromedriver --version

# Running as non sudo user 'worker'
RUN useradd --no-log-init --system --create-home --shell /bin/bash worker
USER worker
WORKDIR /home/worker

# Create the agent inside the image
RUN mkdir -p /home/worker/bin && \
    mkdir -p /home/worker/.robocorp \
    mkdir -p /home/worker/bin/conda && \
    mkdir -p /home/worker/instance
RUN curl --silent --show-error --fail -o /home/worker/bin/robocorp-workforce-agent-core https://downloads.robocorp.com/workforce-agent-core/releases/latest/linux64/robocorp-workforce-agent-core
RUN chmod +x /home/worker/bin/robocorp-workforce-agent-core

# initialize the Agent Core
RUN /home/worker/bin/robocorp-workforce-agent-core init --log-level TRACE --rcc-exec-path /home/worker/bin/rcc

