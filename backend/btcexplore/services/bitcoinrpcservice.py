"""
Methods for reaching through the RPC client class and retrieving data from our
running bitcoin node
"""
import configparser

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

BITCOIN_CONF_LOCATION = '/media/btcdisk/bitcoin.conf'
RPC_NODE_IP = '127.0.0.1'
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


client = build_rpc_client()


def get_block(block_hash):

    block = client.getblock(block_hash)

    # Cleaning
    block['difficulty'] = float(block['difficulty'])

    return block