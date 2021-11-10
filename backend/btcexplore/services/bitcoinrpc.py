"""
Methods for reaching through the RPC client class and retrieving data from our
running bitcoin node
"""
import configparser

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from retry import retry
from backend.settings import ENVIRONMENT


BITCOIN_CONF_LOCATION = '/root/.bitcoin/bitcoin.conf'
RPC_NODE_IP = 'bitcoind'
RPC_PORT = '8332'

def build_rpc_client():
    # Read RPC credentials from bitcoin.config. Note: configparser needs a section
    # header, so we add a dummy one
    with open(BITCOIN_CONF_LOCATION) as f:
        file_content = '[s]\n' + f.read()
    config = configparser.RawConfigParser()
    config.read_string(file_content)
    rpcuser = config['s']['rpcuser']
    rpcpassword = config['s']['rpcpassword']
    # Instantiate client
    return AuthServiceProxy(f'http://{rpcuser}:{rpcpassword}@{RPC_NODE_IP}:{RPC_PORT}')
if ENVIRONMENT == 'production':
    client = build_rpc_client()

@retry(tries=3)
def get_block_hash(block_height):
    return client.getblockhash(block_height)


@retry(tries=3)
def get_block(block_hash, verbosity=1):
    block = client.getblock(block_hash, verbosity)
    # Cleaning
    block['difficulty'] = float(block['difficulty'])
    return block


@retry(tries=3)
def get_transaction(txid, block_hash):
    trans = client.getrawtransaction(txid, True, block_hash)
    # No cleaning necessary?
    return trans