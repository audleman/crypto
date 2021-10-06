from django.test import TestCase
from django.test import TestCase
from btcexplore.utils.address_conversion import address_from_public_key
from btcexplore.tests.factories import BlockFactory, VinCoinbaseFactory


class TransactionTests(TestCase):

    def test_address_from_public_key(self):
        # for i in range(10):
        #     block = BlockFactory()
        #     print(block, block.hash)
        # for i in range(10):
        #     from pprint import pprint as pp
        #     print(VinCoinbaseFactory())
        pass
        