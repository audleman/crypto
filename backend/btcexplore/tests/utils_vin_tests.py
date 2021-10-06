from django.test import TestCase
from btcexplore.utils.vin import get_vin_type, VinType
from jsonschema.exceptions import ValidationError

class GetVinTypeTests(TestCase):

    def test_coinbase_type(self):
        
        # Good schema
        tx = {'coinbase': '04ffff001d0103', 'sequence': 4294967295}
        vin_type = get_vin_type(tx)
        self.assertEqual(vin_type, VinType.COINBASE)

        # Bad schema        
        tx = {'foo': 'bar'}
        with self.assertRaises(ValidationError):
            get_vin_type(tx)

        # Additional properties not allowed
        tx = {'coinbase': '04ffff001d0103', 'sequence': 4294967295, 'extra_param': 'baz'}
        with self.assertRaises(ValidationError):
            get_vin_type(tx)
        
