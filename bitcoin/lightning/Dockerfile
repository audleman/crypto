FROM lightninglabs/lnd:v0.14.1-beta

# Build/runtime env setup
ARG checkout
ARG TMP_DIR=/tmp

# Pass args into env
ENV TMP_DIR=$TMP_DIR

# Injection
COPY lnd.conf $TMP_DIR/lnd.conf
COPY init     /usr/local/bin/init

# Override base template's entrypoint
ENTRYPOINT []