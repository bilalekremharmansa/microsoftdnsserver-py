from typing import List

from microsoftdnsserver.dns.record import Record, RecordType
from microsoftdnsserver.exception.exception_common import MethodNotImplementedError


class DNSService(object):

    def __init__(self):
        pass

    def getDNSRecords(self, zone: str, name: str, recordType: RecordType) -> List[Record]:
        raise MethodNotImplementedError()

    def addARecord(self, zone: str, name: str, ip: str, ttl: str) -> bool:
        raise MethodNotImplementedError()

    def removeARecord(self, zone: str, name: str) -> bool:
        raise MethodNotImplementedError()

    def addTxtRecord(self, zone: str, name: str, content, ttl: str) -> bool:
        raise MethodNotImplementedError()

    def removeTxtRecord(self, zone: str, name: str) -> bool:
        raise MethodNotImplementedError()