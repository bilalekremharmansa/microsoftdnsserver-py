import unittest

from microsoftdnsserver.dns.record import RecordType
from microsoftdnsserver.util import dns_server_utils


class TestRecords(unittest.TestCase):

    def test_supported_record_types(self):
        self.assertTrue(dns_server_utils.isRecordTypeSupported('A'))
        self.assertTrue(dns_server_utils.isRecordTypeSupported('Txt'))

        self.assertFalse(dns_server_utils.isRecordTypeSupported('SOA'))
        self.assertFalse(dns_server_utils.isRecordTypeSupported('TXT'))

    def test_record_type_value_of(self):
        record_type_a = RecordType.value_of('A')

        self.assertEqual(RecordType.A, record_type_a)

        record_type_txt = RecordType.value_of('Txt')

        self.assertEqual(RecordType.TXT, record_type_txt)


if __name__ == '__main__':
    unittest.main()