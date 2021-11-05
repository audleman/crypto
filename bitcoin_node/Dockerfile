FROM ubuntu:20.04

# Update this env variable to set version of bitcoin
ENV BITCOIN_VERSION=22.0

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

WORKDIR /bitcoin
ENV HOME /bitcoin

# Run build script to download and compile bitcoind from source
COPY ./build .
RUN chmod +x build && ./build

EXPOSE 8332 8333
VOLUME ["/bitcoin/.bitcoin"]

# Let 'er rip
CMD ["bitcoind"]