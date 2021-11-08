FROM ubuntu:20.04 as builder

# Passed in by docker-compose.yaml
ARG BITCOIN_VERSION

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
    && apt clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Build
WORKDIR "/bitcoin"
COPY ./scripts/build .
RUN chmod +x build && ./build

# --- 
# Keep image size down by starting from ubuntu base again, only copying
# over build artifacts from the builder stage
# ---
from ubuntu:20.04

COPY --from=builder /usr/local/bin/ /usr/local/bin/

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
    && apt clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Expose bitcoin ports
EXPOSE 8332 8333

# Set up init script - performs env setup and launches bitcoind
WORKDIR "/root"
COPY ./scripts/init .
RUN chmod +x init
CMD ["./init"]
