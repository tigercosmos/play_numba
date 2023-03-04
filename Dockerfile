FROM ubuntu:latest
WORKDIR /build
ENV LC_ALL=en_US.UTF-8

RUN apt-get update && \
    apt-get install -y \
    gcc \
    cmake \
    build-essential \
    gdb \
    git \
    curl \
    wget;

WORKDIR /root
# python
RUN apt-get update && \
    apt-get install -y \
        lcov \
        pkg-config \
        libbz2-dev \
        libffi-dev \
        libgdbm-dev \
        libgdbm-compat-dev \
        liblzma-dev \
        libncurses5-dev \
        libreadline6-dev \
        libsqlite3-dev \
        libssl-dev \
        lzma \
        lzma-dev \
        uuid-dev \
        zlib1g-dev
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/pyenv/pyenv.git /root/.pyenv && \
    echo 'export PYENV_ROOT="/root/.pyenv"' >> /root/.bashrc && \
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> /root/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> /root/.bashrc

WORKDIR /workspace
RUN chmod 777 /workspace
RUN rm -rf /build

CMD [ "/bin/bash" ]