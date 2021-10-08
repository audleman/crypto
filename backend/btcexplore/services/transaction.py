"""
Methods/utilities for processing Transactions

"""

from btcexplore.models import Transaction, Block, Wallet, Utxo
from btcexplore.utils.address_conversion import address_from_public_key
from btcexplore.utils.vin import get_vin_type, VinType, UnknownVinSchema
from btcexplore.utils.vout import get_vout_type, VoutType, UnknownVoutSchema



# Two duplicate txids made it in before the code was patched to make that not 
# possible. We will skip both, as the behavior was for the second to replace the first
# See:
# https://bitcoin.stackexchange.com/questions/40444/what-happens-when-two-txids-collide
# https://github.com/bitcoin/bitcoin/commit/ab91bf39b7c11e9c86bb2043c24f0f377f1cf514
INVALID_TRANSACTIONS = {
    'd5d27987d2a3dfc724e359870c6644b40e497bdc0589a033220fe15429d88599': 91812,
    'e3bf3d07d4b0375638d5f1db5255fe07ba2c4cb067cd81b84ee974b6585fb468': 91722
}
# Here are the hex versions from the PR. Would love to figure out how to translate
# these and verify they match the txids above
INVALID_TRANSACTION_HEX = [
    '0x00000000000a4d0a398161ffc163c503763b1f4360639393e0e4c8e300e0caec',
    '0x00000000000743f190a18c5577a3c2d2a1f610ae9601ac046a38084ccb7cd721'
]

# Keeping track of transactions with type 'nonstandard'. For now manually flagging
# them
KNOWN_NONSTANDARD_TX = [
    'e411dbebd2f7d64dafeef9b14b5c59ec60c36779d43f850e5e347abee1e1a455',
    '2a0597e665ac3d1cabeede95cedf907934db7f639e477b3c77b242140d8cf728',
    'a288fec5559c3f73fd3d93db8e8460562ebfe2fcf04a5114e8d0f2920a6270dc'
]

def is_invalid_transaction(txid: str, block_height: int):
    return txid in INVALID_TRANSACTIONS and INVALID_TRANSACTIONS[txid] == block_height
         

def process_vin(transaction: Transaction, vin_set: dict):
    """
    Process transactions in the `vin` of a transaction. 

    Finds the associated UTXOs, deletes them, and records that they're spend
    on their transaction
    """
    for i, vin in enumerate(vin_set):
        vin_type = get_vin_type(vin)
        if vin_type == VinType.COINBASE:
            print(f'        vin {i} (coinbase)')
        elif vin_type == VinType.TXOUT:
            utxo = Utxo.objects.get(id=f'{vin["txid"]}-{vin["vout"]}')
            utxo.spent = transaction.block.time
            utxo.tx_out = transaction
            utxo.save()
            print(f'        vin {i} {utxo}')
        else:
            raise UnknownVinSchema(vin_type)


def process_vout(transaction: Transaction, vout_set: dict):
    print('        ---')
    for i, vout in enumerate(vout_set):
        vout_type = get_vout_type(vout)
        if  vout_type in [VoutType.PUBKEY, VoutType.PUBKEYHASH]:
            if vout_type == VoutType.PUBKEY:
                address = address_from_public_key(vout['scriptPubKey']['asm'].split(' ')[0])
            else:
                address = vout['scriptPubKey']['addresses'][0]    
            
            wallet, created = Wallet.objects.get_or_create(address=address)
            utxo = Utxo.objects.create(
                id=f'{transaction.txid}-{vout["n"]}',
                tx_in=transaction,
                wallet=wallet,
                type=vout_type,
                value=vout['value'],
                created=transaction.block.time)
            print(f'        vout {i} {wallet} {utxo}')
        elif vout_type == VoutType.NONSTANDARD:
            if transaction.txid in KNOWN_NONSTANDARD_TX:
                print(f'        vout {i} NONSTANDARD!')
            else:
                # import ipdb; ipdb.set_trace()
                raise Exception('Unhandled nonstandard transaction')
        else:
            import ipdb; ipdb.set_trace()
            raise UnknownVoutSchema(vout_type)
        
