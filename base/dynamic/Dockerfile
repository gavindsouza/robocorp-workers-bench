# Use the latest LTS base
FROM ubuntu:24.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8 LANGUAGE=C.UTF-8 LC_ALL=C.UTF-8

# Install dependencies
# Install Chromium + Chromedriver without snap
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        curl \
        unzip \
        fonts-indic \
        fonts-noto \
        fonts-noto-cjk \
        libdbus-glib-1-2 \
        ca-certificates \
        bash \
        build-essential \
        zip \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Install matching ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1) && \
    DRIVER_VERSION=$(curl -sS "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_VERSION}") && \
    wget -q "https://storage.googleapis.com/chrome-for-testing-public/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip chromedriver-linux64.zip -d /opt/chromedriver && \
    ln -s /opt/chromedriver/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    rm chromedriver-linux64.zip

RUN google-chrome --version && chromedriver --version

RUN useradd --no-log-init --system --create-home --shell /bin/bash worker
USER worker
WORKDIR /home/worker

RUN mkdir -p /home/worker/bin /home/worker/.robocorp /home/worker/bin/conda /home/worker/instance

# Download Robocorp Agent Core
RUN curl -fsSL -o /home/worker/bin/robocorp-workforce-agent-core \
        https://downloads.robocorp.com/workforce-agent-core/releases/latest/linux64/robocorp-workforce-agent-core && \
    chmod +x /home/worker/bin/robocorp-workforce-agent-core

ARG NAME
ENV LINK_TOKEN=${LINK_TOKEN:-}

# Initialize Agent Core
RUN /home/worker/bin/robocorp-workforce-agent-core init \
        --log-level TRACE \
        --rcc-exec-path /home/worker/bin/rcc

# Build conda environment
COPY ./conda.yaml conda.yaml
RUN /home/worker/bin/rcc ht vars ./conda.yaml

COPY ./start.sh start.sh

ENTRYPOINT [ "./start.sh" ]
