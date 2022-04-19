"""
Methods for reaching through the RPC client class and retrieving data from our
running bitcoin node
"""
import os

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from retry import retry
from backend.settings import ENVIRONMENT


RPC_NODE_IP = 'bitcoind'
RPC_PORT = '8332'

def build_rpc_client():
    rpcuser = os.environ['BTD_RPC_USER']
    rpcpass = os.environ['BTD_RPC_PASSWORD']
    return AuthServiceProxy(f'http://{rpcuser}:{rpcpass}@{RPC_NODE_IP}:{RPC_PORT}')
if ENVIRONMENT == 'production':
    client = build_rpc_client()

@retry(tries=3)
def get_block_hash(block_height):
    client = build_rpc_client()
    return client.getblockhash(block_height)


@retry(tries=6, delay=1, backoff=2)
def get_block(block_hash, verbosity=1):
    client = build_rpc_client()
    block = client.getblock(block_hash, verbosity)
    # Cleaning
    block['difficulty'] = float(block['difficulty'])
    return block


@retry(tries=10)
def get_transaction(txid, block_hash):
    client = build_rpc_client()
    trans = client.getrawtransaction(txid, True, block_hash)
    # No cleaning necessary?
    return trans