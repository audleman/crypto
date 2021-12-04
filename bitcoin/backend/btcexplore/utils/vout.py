"""
Utilities for working with the `vout` section of a Transaction
"""
from jsonschema import validate, ValidationError
from enum import Enum
from django.db import models


class VoutType(models.TextChoices):
    PUBKEY      = 1
    PUBKEYHASH  = 2
    NONSTANDARD = 3
    MULTISIG    = 4
    SCRIPTHASH  = 5
    NULLDATA    = 6


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
    VoutType.SCRIPTHASH: {
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
                        'pattern': 'OP_HASH160 .* OP_EQUAL'
                    },
                    'hex': {'type': 'string'},
                    'reqSigs': {'type': 'number'},
                    'type': {'type': 'string', 'pattern': 'scripthash'}
                },
                'required': ['addresses', 'asm', 'hex', 'reqSigs', 'type'],
                'additionalProperties': False
            }
        },
        'required': ['n', 'value', 'scriptPubKey'],
        'additionalProperties': False
    },
    VoutType.MULTISIG: {
        'type': 'object',
        'properties': {
            'n': {'type': 'number'},
            'value': {'type': 'number'},
            'scriptPubKey': {
                'type': 'object',
                'properties': {
                    'addresses': {'type': 'array', 'minItems': 2, 'maxItems': 3},
                    'asm': {
                        'type': 'string',
                        'pattern': '.* OP_CHECKMULTISIG'
                    },
                    'hex': {'type': 'string'},
                    'reqSigs': {'type': 'number'},
                    'type': {'type': 'string', 'pattern': 'multisig'}
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
                'required': ['type'],
                'additionalProperties': True
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
    Hand-coded logic. Not as cool as jsonschema but efficient
    """
    if instance['scriptPubKey']['type'] == 'pubkey':
        return VoutType.PUBKEY
    elif instance['scriptPubKey']['type'] == 'pubkeyhash':
        return VoutType.PUBKEYHASH
    elif instance['scriptPubKey']['type'] == 'scripthash':
        return VoutType.SCRIPTHASH
    elif instance['scriptPubKey']['type'] == 'multisig':
        return VoutType.MULTISIG
    elif instance['scriptPubKey']['type'] == 'nonstandard':
        return VoutType.NONSTANDARD
    elif instance['scriptPubKey']['type'] == 'nulldata':
        return VoutType.NULLDATA
    raise UnknownVoutSchema(instance)


def get_vout_type_by_schema(instance):
    """
    Use the very nice JSON validation provided by JSONSchema

    HOWEVER - appears to be incredibly slow 
    """
    for schema_type, schema in SCHEMAS.items():
        try:
            validate(instance, schema)
            return schema_type
        except ValidationError:
            pass
    import ipdb; ipdb.set_trace()
    raise UnknownVoutSchema(instance)
