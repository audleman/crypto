"""
Methods/utilities for processing Transactions

"""

from btcexplore.models import Transaction, Block, Wallet, Utxo
from btcexplore.utils.address_conversion import address_from_public_key



def process_vin(transaction: Transaction):
    """
    Process transactions in the `vin` of a transaction. 

    Finds the associated UTXOs, deletes them, and records that they're spend
    on their transaction
    """
    print(f'    vins: {len(transaction.vin)}')
    for i, vin in enumerate(transaction.vin):
        if 'coinbase' in vin.keys():
            print(f'        vin {i} coinbase')
        else:
            import ipdb; ipdb.set_trace()


def process_vout(transaction: Transaction):
    print(f'    vouts: {len(transaction.vout)}')
    for vout in transaction.vout:
        if vout['scriptPubKey']['type'] == 'pubkey':
            import ipdb; ipdb.set_trace()
            address = address_from_public_key(vout['scriptPubKey']['asm'].split(' ')[0])
            print(f'    value: {vout["value"]} to address: {address}')