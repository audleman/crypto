import factory
import hashlib
from btcexplore.models import Block, Transaction, Wallet, Utxo
from django.utils import timezone
from datetime import timedelta
from factory.fuzzy import FuzzyText, FuzzyInteger, FuzzyDecimal
import string
import random

random.seed()
alpha_num = string.digits + string.ascii_lowercase
# Start block timestamps a month ago, just so they're in the past
START_TIME = timezone.now() - timedelta(days=30)


class BlockFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Block

    height = factory.Sequence(lambda n: n)

    # Deterministic SHA-256 hash based on height
    hash = factory.LazyAttribute(lambda a: hashlib.sha256(str(a.height).encode()).hexdigest())

    time = factory.LazyAttribute(lambda a: START_TIME + timedelta(minutes=a.height * 10))


class VinCoinbaseFactory(factory.DictFactory):
    """
    Vin that comes from a coinbase, new coins issued to the block miner
    {
        'coinbase': '04ffff001d02f400', 
        'sequence': 4294967295
    }
    """
    coinbase = FuzzyText(length=6, prefix='04ffff001d', chars=alpha_num)
    sequence = 4294967295  # FuzzyInteger(low=4000000000, high=4999999999)


class VinTxOutFactory(factory.DictFactory):
    """
    A vin that points to the vout from a previous transaction. 
    {
        'scriptSig': {
            'asm': '304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d09[ALL]',
            'hex': '47304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901'
        },
        'sequence': 4294967295,
        'txid': '0437cd7f8525ceed2324359c2d0ba26006d92d856a9c20fa0241106ee5a597c9',
        'vout': 0
    }
    """
    scriptSig = factory.LazyFunction(lambda: factory.DictFactory(
        asm=FuzzyText(length=140, suffix='[ALL]', chars=alpha_num),
        hex=FuzzyText(length=145, chars=alpha_num)))
    sequence = FuzzyInteger(low=42000000000, high=42999999999)
    txid = factory.LazyAttribute(lambda a: hashlib.sha256(str(random.random()).encode()).hexdigest())
    vout = 0


class VoutPubkeyFactory(factory.DictFactory):
    """
    {
        'value': Decimal('50.00000000'),
        'n': 0,
        'scriptPubKey': {
            'asm': '04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f '
                   'OP_CHECKSIG',
            'hex': '4104678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac',
            'type': 'pubkey'}
    }
    """
    n = 0
    value = FuzzyDecimal(low=0.00000001, high=50.00000000, precision=8)
    scriptPubKey = factory.LazyFunction(lambda: factory.DictFactory(
        asm=FuzzyText(length=100, suffix=' OP_CHECKSIG'),
        hex=FuzzyText(length=100),
        type='pubkey'))


class VoutPubkeyhashFactory(factory.DictFactory):
    """
    {
        'value': Decimal('100.00000000')
        'n': 0,
        'scriptPubKey': {
            'addresses': ['12higDjoCCNXSA95xZMWUdPvXNmkAduhWv'],
            'asm': 'OP_DUP OP_HASH160 '
                   '12ab8dc588ca9d5787dde7eb29569da63c3a238c '
                   'OP_EQUALVERIFY OP_CHECKSIG',
            'hex': '76a91412ab8dc588ca9d5787dde7eb29569da63c3a238c88ac',
            'reqSigs': 1,
            'type': 'pubkeyhash'},
        
    }
    """
    n = 0
    value = FuzzyDecimal(low=0.00000001, high=50.00000000, precision=8)
    scriptPubKey = factory.LazyFunction(lambda: factory.DictFactory(
        addresses=factory.LazyFunction(lambda: factory.ListFactory(only_one_address=FuzzyText(length=34))),
        asm=FuzzyText(
            length=100, 
            prefix='OP_DUP OP_HASH160 ',
            suffix=' OP_EQUALVERIFY OP_CHECKSIG'),
        reqSigs=1,
        hex=FuzzyText(length=100),
        type='pubkeyhash'))


class VoutMultisigFactory(factory.DictFactory):
    """
    {
        'n': 0,
        'value': Decimal('0.01000000'),
        'scriptPubKey': {
            'addresses': [
                '1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F',
                '1A8JiWcwvpY7tAopUkSnGuEYHmzGYfZPiq'
            ],
            'asm': '1 '
                   '04cc71eb30d653c0c3163990c47b976f3fb3f37cccdcbedb169a1dfef58bbfbfaff7d8a473e7e2e6d317b87bafe8bde97e3cf8f065dec022b51d11fcdd0d348ac4 '
                   '0461cbdcc5409fb4b4d42b51d33381354d80e550078cb532a34bfa2fcfdeb7d76519aecc62770f5b0e4ef8551946d8a540911abe3e7854a26f39f58b25c15342af '
                   '2 OP_CHECKMULTISIG',
            'hex': '514104cc71eb30d653c0c3163990c47b976f3fb3f37cccdcbedb169a1dfef58bbfbfaff7d8a473e7e2e6d317b87bafe8bde97e3cf8f065dec022b51d11fcdd0d348ac4410461cbdcc5409fb4b4d42b51d33381354d80e550078cb532a34bfa2fcfdeb7d76519aecc62770f5b0e4ef8551946d8a540911abe3e7854a26f39f58b25c15342af52ae',
            'reqSigs': 1,
            'type': 'multisig'
        }
    }
    """
    n = 0
    value = FuzzyDecimal(low=0.00000001, high=50.00000000, precision=8)
    scriptPubKey = factory.LazyFunction(lambda: factory.DictFactory(
        addresses=factory.LazyFunction(lambda: factory.ListFactory(
            address1=FuzzyText(length=34),
            address2=FuzzyText(length=34))),
        asm=FuzzyText(
            length=200, 
            prefix='1 ',
            suffix=' 2 OP_CHECKMULTISIG'),
        reqSigs=1,
        hex=FuzzyText(length=100),
        type='multisig'))


class VoutScriptHashFactory(factory.DictFactory):
    """
    {
        'n': 1,
        'value': Decimal('0.00400000'),
        'scriptPubKey': {
            'addresses': ['342ftSRCvFHfCeFFBuz4xwbeqnDw6BGUey'],
            'asm': 'OP_HASH160 19a7d869032368fd1f1e26e5e73a4ad0e474960e '
                   'OP_EQUAL',
            'hex': 'a91419a7d869032368fd1f1e26e5e73a4ad0e474960e87',
            'reqSigs': 1,
            'type': 'scripthash'
        }
    }
    """
    n = 0
    value = FuzzyDecimal(low=0.00000001, high=50.00000000, precision=8)
    scriptPubKey = factory.LazyFunction(lambda: factory.DictFactory(
        addresses=factory.LazyFunction(lambda: factory.ListFactory(only_one_address=FuzzyText(length=34))),
        asm=FuzzyText(
            length=100, 
            prefix='OP_DUP OP_HASH160 ',
            suffix=' OP_EQUALVERIFY OP_CHECKSIG'),
        reqSigs=1,
        hex=FuzzyText(length=100),
        type='scripthash'))


class VoutNullDataFactory(factory.DictFactory):
    """
    {
        'n': 0,
        'scriptPubKey': {
            'asm': 'OP_RETURN', 
            'hex': '6a', 
            'type': 'nulldata'},
        'value': Decimal('0E-8')}
    """
    n = 0
    value = FuzzyDecimal(low=0.00000000, high=0.00000000, precision=8)
    scriptPubKey = factory.LazyFunction(lambda: factory.DictFactory(
        addresses=factory.LazyFunction(lambda: factory.ListFactory(only_one_address=FuzzyText(length=34))),
        asm='OP_RETURN',
        hex='6a',
        type='nulldata'))