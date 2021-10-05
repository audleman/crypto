#!/usr/bin/env python
# https://en.bitcoin.it/wiki/Protocol_documentation#Addresses

import hashlib
import base58


def address_from_public_key(pub_key):
    """
    IN:  ECDSA bitcoin public key

    OUT: base58 address
    """

    # 1 - SHA-256 hash of pub_key
    sha = hashlib.sha256(bytearray.fromhex(pub_key))

    # 2 - RIPEMD-160 of 1
    ripe = hashlib.new('ripemd160', sha.digest()).hexdigest()

    # 3 - Add network bytes to 2
    key_hash = f'00{ripe}'

    # 4 - Double SHA-256 of 3 to generate checksum
    checksum = hashlib.sha256(bytearray.fromhex(key_hash)).digest()
    checksum = hashlib.sha256(checksum).hexdigest()[0:8]

    # 5 - Add 4 to end of 3
    key_hash = bytes(bytearray.fromhex(key_hash + checksum))

    # 6 - Base58 encoding of 5
    address = base58.b58encode(key_hash).decode('utf-8')

    return address