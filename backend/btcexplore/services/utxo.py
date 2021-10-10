"""
Methods/utilities for UTXOs

"""
from btcexplore.models import Utxo
from btcexplore.utils.address_conversion import address_from_public_key
from btcexplore.utils.vin import get_vin_type, VinType, UnknownVinSchema
from btcexplore.utils.vout import get_vout_type, VoutType, UnknownVoutSchema
from datetime import date, timedelta

from enum import Enum

AVG_DAYS_PER_MONTH = 30.416
ONE_YEAR = 365

class UtxoAgeBand(Enum):
    D1  = '1d'
    W1  = '1w'
    M1  = '1m'
    M3  = '3m'
    M6  = '6m'
    Y1  = '1y'
    Y2  = '2y'
    Y3  = '3y'
    Y5  = '5y'
    Y7  = '7y'
    Y10 = '10y'
    Y10_PLUS = 'over_10y'

def utxo_age_band(utxo: Utxo, curr_date: date):
    age = curr_date - utxo.created.date()
    if age  < timedelta(days=1):
        return UtxoAgeBand.D1
    elif age < timedelta(weeks=1):
        return UtxoAgeBand.W1
    elif age < timedelta(days=AVG_DAYS_PER_MONTH):
        return UtxoAgeBand.M1
    elif age < timedelta(days=AVG_DAYS_PER_MONTH * 3):
        return UtxoAgeBand.M3
    elif age < timedelta(days=AVG_DAYS_PER_MONTH * 6):
        return UtxoAgeBand.M6
    elif age < timedelta(days=ONE_YEAR):
        return UtxoAgeBand.Y1
    elif age < timedelta(days=ONE_YEAR * 2):
        return UtxoAgeBand.Y2
    elif age < timedelta(days=ONE_YEAR * 3):
        return UtxoAgeBand.Y3
    elif age < timedelta(days=ONE_YEAR * 5):
        return UtxoAgeBand.Y5
    elif age < timedelta(days=ONE_YEAR * 7):
        return UtxoAgeBand.Y7
    elif age < timedelta(days=ONE_YEAR * 10):
        return UtxoAgeBand.Y10
    else:
        return UtxoAgeBand.Y10_PLUS