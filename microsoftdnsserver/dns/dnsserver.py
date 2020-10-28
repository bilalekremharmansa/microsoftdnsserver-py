import json

from microsoftdnsserver.command_runner.runner import Command, CommandRunner
from microsoftdnsserver.command_runner.powershell_runner import PowerShellCommand, PowerShellRunner
from .base import DNSService
from .record import RecordType
from ..util import dns_server_utils, logger


class DnsServerModule(DNSService):
    """
        Wrapper of Windows-DnsServer powershell module

        https://docs.microsoft.com/en-us/powershell/module/dnsserver/?view=win10-ps
    """

    def __init__(self, runner: CommandRunner = None):
        super().__init__()
        self.runner = runner
        if runner is None:
            self.runner = PowerShellRunner()

        self.logger = logger.createLogger("DnsServer")

    def getDNSRecords(self, zone: str, name: str = None, recordType: RecordType = None):
        """ uses Get-DnsServerResourceRecord cmdlet to get records in a zone """

        args = {
            'Zone': zone
        }

        if name:
            args['Name'] = name
        if recordType:
            args['RRType'] = recordType.value

        command = PowerShellCommand('Get-DnsServerResourceRecord', **args)
        result = self.run(command)

        jsonResult = json.loads(result.out)
        return dns_server_utils.formatDnsServerResult(zone, jsonResult)

    def addARecord(self, zone: str, name: str, ip: str, ttl: str = '1h'):
        """ uses Add-DnsServerResourceRecordA cmdlet to add a resource in a zone """

        command = PowerShellCommand(
            'Add-DnsServerResourceRecordA',
            'AllowUpdateAny',
            ZoneName=zone,
            Name=name,
            IPv4Address=ip,
            TimeToLive=dns_server_utils.formatTtl(ttl)
        )

        result = self.run(command)
        return result.success

    def removeARecord(self, zone: str, name: str):
        """ uses Remove-DnsServerResourceRecord cmdlet to remove a record in a zone """

        args = {
            'ZoneName': zone,
            'RRType': 'A'
        }
        if name:
            args['Name'] = name

        flags = ['Force']

        command = PowerShellCommand('Remove-DnsServerResourceRecord', *flags, **args)
        result = self.run(command)

        return result

    # ---

    def addTxtRecord(self, zone: str, name: str, content: str, ttl: str = '1h'):
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

        result = self.run(command)

        return result.success

    def removeTxtRecord(self, zone: str, name: str):
        """ uses Remove-DnsServerResourceRecord cmdlet to remove txt record in a zone """

        args = {
            'ZoneName': zone,
            'RRType': 'Txt'
        }
        if name:
            args['Name'] = name

        flags = ['Force']

        command = PowerShellCommand('Remove-DnsServerResourceRecord', *flags, **args)
        result = self.run(command)

        return result.success

    # --

    def run(self, command: Command):
        result = self.runner.run(command)

        if not result.success:
            self.logger.error("Command failed [%s]" % command.prepareCommand())

        return result

    def isDnsServerModuleInstalled(self):
        cmdlet = "Get-Module DNSServer -ListAvailable"
        result = self.runner.run(cmdlet)

        return result.success and len(result.out) > 0
