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
    sha = hashlib.sha256()
    sha.update(bytearray.fromhex(pub_key))

    # 2 - RIPEMD-160 of 1
    rip = hashlib.new('ripemd160')
    rip.update(sha.digest())
    ripe_str = rip.hexdigest()

    # 3 - Add network bytes to 2
    key_hash = f'00{ripe_str}'

    # 4 - Double SHA-256 of 3 to generate checksum
    sha = hashlib.sha256()
    sha.update(bytearray.fromhex(key_hash))
    checksum = sha.digest()
    sha = hashlib.sha256()
    sha.update(checksum)
    checksum = sha.hexdigest()[0:8]
    
    # 5 - Add 4 to end of 3
    key_hash = bytes(bytearray.fromhex(key_hash + checksum))

    # 6 - Base58 encoding of 5
    address = base58.b58encode(key_hash).decode('utf-8')

    return address