FROM ubuntu:20.04 as builder

# Passed in by docker-compose.yaml
ARG VERSION

# Install build dependencies, cleanup
RUN apt update \
    && apt install -y --no-install-recommends \
        build-essential \
        libtool \
        autotools-dev \
        automake \
        pkg-config \
        bsdmainutils \
        python3 \
        ca-certificates \
        curl \
        libevent-dev \
        libboost-dev \
        libboost-system-dev \
        libboost-filesystem-dev \
        libboost-test-dev \
        libzmq3-dev \
    && apt clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Build
WORKDIR "/bitcoin"
COPY build.sh build
RUN chmod +x build && ./build

# --- 
# Keep image size down by starting from ubuntu base again, only copying
# over binaries from the builder stage
from ubuntu:20.04

# Install runtime dependencies, cleanup
RUN apt update \
    && apt install -y --no-install-recommends \
        libevent-dev \
        libboost-dev \
        libboost-system-dev \
        libboost-filesystem-dev \
        libboost-test-dev \
        ca-certificates \
        libsqlite3-dev \
        libzmq3-dev \
    && apt clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=builder /usr/local/bin/ /usr/local/bin/

ARG TMP_DIR=/tmp

# Pass args into env
ENV TMP_DIR=$TMP_DIR

# Injection
COPY bitcoin.conf $TMP_DIR/bitcoin.conf
COPY init /usr/local/bin/init