from django.test import TestCase
from btcexplore.utils.address_conversion import address_from_public_key

# Create your tests here.
class AddressConversionTests(TestCase):

    def test_address_from_public_key(self):
        # Random pubkey
        pub_key = '0450863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A04887E5B23522CD470243453A299FA9E77237716103ABC11A1DF38855ED6F2EE187E9C582BA6'
        self.assertEqual(
            address_from_public_key(pub_key),
            '16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM')
        # Genesis block
        pub_key = '04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f'
        self.assertEqual(
            address_from_public_key(pub_key),
            '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa')