import logging

from microsoftdnsserver.command_runner.powershell_runner import PowerShellCommand
from .base import DNSService
from ..util import dns_server_utils

class DnsServerModule(DNSService):
    """
        Wrapper of Windows-DnsServer powershell module

        https://docs.microsoft.com/en-us/powershell/module/dnsserver/?view=win10-ps
    """

    def __init__(self, runner):
        super().__init__()
        self.runner = runner

        self.logger = None
        pass

    def _initLogger(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        self.logger = logger


    def getDNSRecords(self, zone, name=None, recordType=None):
        """ uses Get-DnsServerResourceRecord cmdlet to get records in a zone """

        args = {
            'Zone': zone
        }

        if name:
            args['Name'] = name
        if recordType:
            args['RRType'] = recordType

        command = PowerShellCommand('Get-DnsServerResourceRecord', **args)
        self.run(command)


    def addARecord(self, zone, name, ip, ttl='1h', ageRecord=False):
        """ uses Add-DnsServerResourceRecordA cmdlet to add a resource in a zone """

        command = PowerShellCommand(
            'Add-DnsServerResourceRecordA',
            'AllowUpdateAny',
            ZoneName=zone,
            Name=name,
            IPv4Address=ip,
            TimeToLive=dns_server_utils.formatTtl(ttl)
        )

        self.run(command)

    def removeARecord(self, zone, name, recordData=None):
        """ uses Remove-DnsServerResourceRecord cmdlet to remove a record in a zone """

        args = {
            'ZoneName': zone,
            'RRType': 'A'
        }
        if name:
            args['Name'] = name
        if recordData:
            args['RecordData'] = recordData

        flags = ['Force']

        command = PowerShellCommand('Remove-DnsServerResourceRecord', *flags, **args)
        self.run(command)

    # ---

    def addTxtRecord(self, zone, name, content, ttl='1h'):
        """ uses Add-DnsServerResourceRecord cmdlet to add txt resource in a zone """

        command = PowerShellCommand(
            'Add-DnsServerResourceRecord',
            'AllowUpdateAny',
             'Txt',
            ZoneName=zone,
            Name=name,
            DescriptiveText=content,
            TimeToLive=dns_server_utils.formatTtl(ttl)
        )

        self.run(command)

    def removeTxtRecord(self, zone, name, recordData=None):
        """ uses Remove-DnsServerResourceRecord cmdlet to remove txt record in a zone """

        args = {
            'ZoneName': zone,
            'RRType': 'Txt'
        }
        if name:
            args['Name'] = name
        if recordData:
            args['RecordData'] = recordData

        flags = ['Force']

        command = PowerShellCommand('Remove-DnsServerResourceRecord', *flags, **args)
        self.run(command)

    # --

    def run(self, command):
        result = self.runner.run(command)

        if not result.success:
            self.logger.error("Command failed [%s]" % command.prepareCommand())

    def isDnsServerModuleInstalled(self):
        cmdlet = "Get-Module DNSServer -ListAvailable"
        result = self.runner.run(cmdlet)

        return result.success and len(result.out) > 0
