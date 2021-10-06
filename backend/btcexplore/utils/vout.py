"""
Utilities for working with the `vout` section of a Transaction
"""
from jsonschema import validate, ValidationError
from enum import Enum


class VoutType(Enum):
    PUBKEY = 1
    PUBKEYHASH = 2
    NONSTANDARD = 3


SCHEMAS = {
    VoutType.PUBKEY: {
        'type': 'object',
        'properties': {
            'scriptPubKey': {
                'type': 'object',
                'properties': {
                    'asm': {'type': 'string', 'pattern': '.* OP_CHECKSIG'},
                    'hex': {'type': 'string'},
                    'type': {'type': 'string', 'pattern': 'pubkey'}
                },
                'required': ['asm', 'hex', 'type'],
                'additionalProperties': False
            },
            'n': {'type': 'number'},
            'value': {'type': 'number'},

        },
        'required': ['scriptPubKey', 'n', 'value'],
        'additionalProperties': False
    },
    VoutType.PUBKEYHASH: {
        'type': 'object',
        'properties': {
            'n': {'type': 'number'},
            'value': {'type': 'number'},
            'scriptPubKey': {
                'type': 'object',
                'properties': {
                    'addresses': {'type': 'array', 'minItems': 1, 'maxItems': 1},
                    'asm': {
                        'type': 'string',
                        'pattern': 'OP_DUP OP_HASH160 .* OP_EQUALVERIFY OP_CHECKSIG'
                    },
                    'hex': {'type': 'string'},
                    'reqSigs': {'type': 'number'},
                    'type': {'type': 'string', 'pattern': 'pubkeyhash'}
                },
                'required': ['addresses', 'asm', 'hex', 'reqSigs', 'type'],
                'additionalProperties': False
            }
        },
        'required': ['n', 'value', 'scriptPubKey'],
        'additionalProperties': False
    },
    VoutType.NONSTANDARD: {
        'type': 'object',
        'properties': {
            'n': {'type': 'number'},
            'scriptPubKey': {
                'type': 'object',
                'properties': {
                    'asm': {'type': 'string'},
                    'hex': {'type': 'string'},
                    'type': {'type': 'string', 'pattern': 'nonstandard'}
                },
                'required': ['asm', 'hex', 'type'],
                'additionalProperties': False
            },
            'value': {'type': 'number'}
        },
        'required': ['n', 'value', 'scriptPubKey'],
        'additionalProperties': False        
    }
}


class UnknownVoutSchema(Exception):
    pass


def get_vout_type(instance):
    """
    Check vout instance against known JSON schemas
    """
    for schema_type, schema in SCHEMAS.items():
        try:
            validate(instance, schema)
            return schema_type
        except ValidationError:
            pass
    raise UnknownVoutSchema(instance)
