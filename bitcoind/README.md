# Bitcoin node

Docker image that builds bitcoin core from source. Set to allow RPC connections
on the docker local network. 

## Updating bitcoin core version

To perform an upgrade, find the new release number on the github releases page:

https://github.com/bitcoin/bitcoin/releases

And update the environment variable BITCOIN_VERSION in docker-compose.yaml at
the root of this project
