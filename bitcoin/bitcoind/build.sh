#!/bin/bash
set -ex

# Download
# ------------------------------------------------------------------------------

echo "Fetching bitcoin version: $VERSION"
curl -L https://github.com/bitcoin/bitcoin/archive/refs/tags/v$VERSION.tar.gz | tar -zx --strip-components=1



# Build
# ------------------------------------------------------------------------------

echo "Building bitcoin source..."

# Berkley database for wallet support
./contrib/install_db4.sh `pwd`

./autogen.sh
export BDB_PREFIX='/bitcoin/db4'
./configure --without-gui BDB_LIBS="-L${BDB_PREFIX}/lib -ldb_cxx-4.8" BDB_CFLAGS="-I${BDB_PREFIX}/include"
make -j 4  # use "-j N" for N parallel jobs
make install

# ---- Run the tests
echo "Running test suite..."
test_bitcoin


# Cleanup - important to keep intermediate image size down
# ------------------------------------------------------------------------------

echo "Cleaning up..."
# Remove some unused but large binaries
rm /usr/local/bin/test_bitcoin   # 500mb
rm /usr/local/bin/bench_bitcoin  # 300mb

# Remove source folder to cleanum ~5GB 
cd /
rm -rf /bitcoin

echo "Build complete. Happy bitcoining!"