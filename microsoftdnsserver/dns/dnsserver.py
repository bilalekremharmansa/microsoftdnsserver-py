from microsoftdnsserver.command_runner.powershell_runner import PowerShellCommand
from .base import DNSService
from ..util.dns_server_utils import formatTtl

class DnsServerModule(DNSService):
    """
        Wrapper of Windows-DnsServer powershell module

        https://docs.microsoft.com/en-us/powershell/module/dnsserver/?view=win10-ps
    """

    def __init__(self, runner):
        super().__init__()
        self.runner = runner
        pass

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
        result = self.runner.run(command)


    def addARecord(self, zone, name, ip, ttl='1h', ageRecord=False):
        """ uses Add-DnsServerResourceRecordA cmdlet to add a resource in a zone """

        command = PowerShellCommand(
            'Add-DnsServerResourceRecordA',
            'AllowUpdateAny',
            ZoneName=zone,
            Name=name,
            IPv4Address=ip,
            TimeToLive=formatTtl(ttl)
        )

        result = self.runner.run(command)

    def removeARecord(self, zone, name, recordData=None):
        """ uses Remove-DnsServerResourceRecord cmdlet to remove a record in a zone """

        args = {
            'Zone': zone
        }
        if name:
            args['Name'] = name
        if recordData:
            args['RecordData'] = recordData

        flags = ['Force']

        command = PowerShellCommand('Remove-DnsServerResourceRecord', *flags, **args)
        result = self.runner.run(command)

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
            TimeToLive=formatTtl(ttl)
        )

        result = self.runner.run(command)

    def removeARecord(self, zone, name, recordData=None):
        """ uses Remove-DnsServerResourceRecord cmdlet to remove txt record in a zone """

        args = {
            'Zone': zone
        }
        if name:
            args['Name'] = name
        if recordData:
            args['RecordData'] = recordData

        flags = ['Force']

        command = PowerShellCommand('Remove-DnsServerResourceRecord', *flags, **args)
        result = self.runner.run(command)
