FROM ubuntu:20.04

# Update this env variable to set version of bitcoin
ENV BITCOIN_VERSION=22.0

# Bitcoin dependencies
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
        curl
        
# Optional Software
# RUN apt install -y git 

# Clean up after apt
RUN apt clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Checkout bitcoin master branch (TODO: peg to version)
# RUN GIT_SSL_NO_VERIFY=1 git clone https://github.com/bitcoin/bitcoin.git bitcoin

# Set environment
WORKDIR /bitcoin
ENV HOME /bitcoin

# Build bitcoin from source
COPY ./build .
RUN chmod +x build && ./build

# Let 'er rip
# COPY ./go .
# RUN chmod +x go
CMD ["bitcoind"]