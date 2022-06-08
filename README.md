Fun with crypto! My personal development around Bitcoin and Ethereum

# Bitcoin
A docker swarm of the following microservices:

- Bitcoind - the bitcoin daemon
- Lnd - official lightning daemon
- RTL - a web dashboard for lightning
- Backend - my personal sandbox, used for querying bitcoin blockchain and doing
            interesting things with the results

These run as docker containers and are orchestrated via docker-compose

## Setup

1. Base machine needs docker
1. Source bash extensions in your .bash_profile
1. Create `crypto/bitcoin/.secrets`
    * Copy `crypto/bitcoin/.secrets.tmpl` and populate reasonable values
3. Operate containers from `crypto/bitcoin/docker-compose.yaml`

