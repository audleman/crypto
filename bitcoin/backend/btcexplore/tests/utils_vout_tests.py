from django.test import TestCase
from btcexplore.utils.vout import get_vout_type, VoutType, UnknownVoutSchema
from btcexplore.tests.factories import VoutPubkeyFactory, VoutPubkeyhashFactory



class GetVoutPubkeyTypeTests(TestCase):

    def test_pubkey_type_good(self):
        tx = VoutPubkeyFactory()
        vout_type = get_vout_type(tx)
        self.assertEqual(vout_type, VoutType.PUBKEY)

    def test_pubkey_malformed_asm(self):
        """
        asm should end with OP_CHECKSIG
        """
        tx = VoutPubkeyFactory()
        tx['scriptPubKey']['asm'] = tx['scriptPubKey']['asm'].replace('OP_CHECKSIG', '')
        with self.assertRaises(UnknownVoutSchema):
             get_vout_type(tx)

    def test_pubkey_wrong_type(self):
        """
        asm should end with OP_CHECKSIG
        """
        tx = VoutPubkeyFactory()
        tx['scriptPubKey']['type'] = 'wrongtype'
        with self.assertRaises(UnknownVoutSchema):
             get_vout_type(tx)



class GetVoutPubkeyhashTypeTests(TestCase):

    def test_pubkeyhash_type_good(self):
        tx = VoutPubkeyhashFactory()
        vout_type = get_vout_type(tx)
        self.assertEqual(vout_type, VoutType.PUBKEYHASH)

    def test_pubkeyhash_malformed(self):
        """
        asm script missing part of function stack
        """
        tx = VoutPubkeyhashFactory()
        tx['scriptPubKey']['asm'] = tx['scriptPubKey']['asm'].replace('OP_CHECKSIG', '')
        with self.assertRaises(UnknownVoutSchema):
            get_vout_type(tx)

    def test_pubkeyhash_multiple_addresses_disallowed(self):
        """
        Only one address allowed. Multiple is multisig (?) which is a TODO
        """
        tx = VoutPubkeyhashFactory()
        tx['scriptPubKey']['addresses'] = ['1', '2']
        with self.assertRaises(UnknownVoutSchema):
            get_vout_type(tx)
