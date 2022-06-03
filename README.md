My personal development around Bitcoin and Ethereum

# Bitcoin

A container-orchestrated setup for running bitcoin + lightning

- A full Bitcoin node, built from source
- Backend, written in Django 
- Lightning node
- Ride the Lightning (RTL) admin interface for Lightning


These run as docker containers and are orchestrated via docker-compose

## Setup

1. Install docker
2. Install docker-compose


## Run
Starts the bitcoin daemon, backend
```
$ cd crypto/bitcoin
$ docker-compose up
```

# Ethereum

Runs a light node, validator TBD
