"""
https://en.bitcoin.it/wiki/Protocol_documentation#Addresses

Version = 1 byte of 0 (zero); on the test network, this is 1 byte of 111
Key hash = Version concatenated with RIPEMD-160(SHA-256(public key))
Checksum = 1st 4 bytes of SHA-256(SHA-256(Key hash))
Bitcoin Address = Base58Encode(Key hash concatenated with Checksum)
"""

import hashlib
import base58

# Network version: 00 for mainnet
VERSION = '00'

def address_from_public_key(pub_key):
    """
    IN:  ECDSA bitcoin public key

    OUT: base58 address
    """

    # 1 - SHA-256 hash of pub_key
    sha = hashlib.sha256(bytearray.fromhex(pub_key)).digest()

    # 2 - RIPEMD-160 of 1
    ripe = hashlib.new('ripemd160', sha).hexdigest()

    # 3 - Add network version to 2
    key_hash = f'{VERSION}{ripe}'

    # 4 - Double SHA-256 of 3 to generate checksum
    checksum = hashlib.sha256(bytearray.fromhex(key_hash)).digest()
    checksum = hashlib.sha256(checksum).hexdigest()[0:8]

    # 5 - Add 4 to end of 3
    key_hash_plus_checksum = bytes(bytearray.fromhex(key_hash + checksum))

    # 6 - Base58 encoding of 5
    address = base58.b58encode(key_hash_plus_checksum).decode('utf-8')

    return address