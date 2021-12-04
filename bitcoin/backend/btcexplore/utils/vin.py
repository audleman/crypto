"""
Utilities for working with the `vin` section of a Transaction
"""
from jsonschema import validate, ValidationError
from enum import Enum, auto


class VinType(Enum):
    COINBASE = auto()
    TXOUT = auto()


SCHEMAS = {
    VinType.COINBASE: {
        'type': 'object',
        'properties': {
            'coinbase': {'type': 'string'},
            'sequence': {'type': 'number'}
        },
        'required': ['coinbase', 'sequence'],
        'additionalProperties': False
    },
    VinType.TXOUT: {
        'type': 'object',
        'properties': {
            'scriptSig': {
                'type': 'object',
                'properties': {
                    'asm': {'type': 'string'},
                    'hex': {'type': 'string'},
                },
                'required': ['asm', 'hex'],
                'additionalProperties': False
            },
            'sequence': {'type': 'number'},
            'txid': {'type': 'string'},
            'vout': {'type': 'number'}
        },
        'required': ['scriptSig', 'sequence', 'txid', 'vout'],
        'additionalProperties': False
    }
}


class UnknownVinSchema(Exception):
    pass


def get_vin_type_by_schema(instance):
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
    raise UnknownVinSchema(instance)


def get_vin_type(instance):
    if 'coinbase' in instance:
        return VinType.COINBASE
    elif 'txid' in instance:
        return VinType.TXOUT
    else:
        raise UnknownVinSchema(instance)