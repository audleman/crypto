FROM ubuntu:20.04

# Passed in by docker-compose.yaml
ARG BITCOIN_VERSION
ARG HOME

# Pass into container runtime
ENV HOME $HOME

# Install apt dependencies, cleanup afterwards
RUN apt update \
    && apt install -y --no-install-recommends \
        build-essential \
        libtool \
        autotools-dev \
        automake \
        pkg-config \
        bsdmainutils \
        libevent-dev \
        libboost-dev \
        libboost-system-dev \
        libboost-filesystem-dev \
        libboost-test-dev \
        python3 \
        ca-certificates \
        curl \
    && apt clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR $HOME

# Run build script - downloads and compiles bitcoin
COPY ./build .
RUN chmod +x build && ./build

# Expose bitcoin ports
EXPOSE 8332 8333

# Let 'er rip
COPY ./run .
RUN chmod +x run
CMD ["./run"]