My personal development around Bitcoin and Ethereum

# Bitcoin

A container-orchestrated setup for running bitcoin + lightning

- A full Bitcoin node, built from source
- Backend, written in Django 
- Lightning node
- Ride the Lightning (RTL) admin interface for Lightning


These run as docker containers and are orchestrated via docker-compose

## Setup

1. Base machine needs docker
1. Source bash extensions in your .bash_profile
1. Create `crypto/bitcoin/.secrets`
    * Copy `crypto/bitcoin/.secrets.tmpl` and populate reasonable values
3. Operate containers from `crypto/bitcoin/docker-compose.yaml`

