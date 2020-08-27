from microsoftdnsserver.exception.exception_common import MethodNotImplementedError


class DNSService(object):

    def __init__(self):
        pass

    def getDNSRecords(self, zone, name, recordType):
        raise MethodNotImplementedError()

    def addARecord(self, zone, name, ip, ttl, ageRecord):
        raise MethodNotImplementedError()

    def removeARecord(self, zone, name, recordData):
        raise MethodNotImplementedError()
