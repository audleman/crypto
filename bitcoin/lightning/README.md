# Installation

### Copy lnd.config to data volume

We use `lnd.conf` to avoid having to pass in a bunch of arguments on the command line. This repo has a conf file in this directory called `sample.lnd.conf` that needs to be copied to your data volume as `lnd.conf` before starting your container. 

1. Configure a volume for lightning data. Example: /media/lightning (see docker-compose.yml)
1. Copy `sample.lnd.conf` from this directory to your volume's root.
1. Replace all dummy values (rpc creds)

Note that we have to copy RPC username/password from bitcoin.conf. It's annoying, it would be better
if lnd could just read bitcoin.conf. It has some capability to do that but it doesn't appear to play
well with docker hostnames. See notes in lnd.conf. 

## Create a wallet

1. Run `git submodule update` to ensure the lnd repo is checked out into the appropriate place
1. Start container with `docker-compose up lightning`
1. Execution will pause, asking you to manually create a wallet
```
    $ lncli create
```
1. Choose a password, generate recovery seed. Save these someplace safe as once gone you will lose access forever! 

## Set wallet to auto-open

By default lnd makes you shell into your container and run `lnd unlock` with your password every time it restarts. Luckily they provide a config flag to load the password from a file.

The filename can be configured in `lnd.conf` and defaults to `wallet_pw.txt`

```
[Application Options]
  wallet-unlock-password-file=/root/.lnd/wallet_pw.txt
``` 

Create this file in the same place you put lnd.config.

More information at https://github.com/lightningnetwork/lnd/blob/master/docs/wallet.md

