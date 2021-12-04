This folder contains a dockerfile for running a full bitcoin core node. It 
downloads the source code from Github and builds from source.

Data persistence is handled with an external volume. You must ensure it has
enough space to hold the entire block history. Thanks to this, the container 
can be torn down/recreated at will and will simply pick up where it left off. 

Wallet support is enabled and a wallet named `wallet` is created if it doesn't 
already exist on the data volume. 

The RPC api is enabled with a random password generated on initialization. See
docker-compose.yaml for security considerations. 

### Updating to a newer version of bitcoin core

Update the environment variable BITCOIN_VERSION to the release you want
in docker-compose.yaml

Find the new release number on the github releases page:
https://github.com/bitcoin/bitcoin/releases

Run `docker-compose build` to build a new container version. 
