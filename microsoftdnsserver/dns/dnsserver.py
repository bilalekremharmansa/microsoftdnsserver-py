from microsoftdnsserver.command_runner.powershell_runner import PowerShellCommand
from .base import DNSService


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
        result = self.runner(command)


    def addARecord(self, zone, name, ip, ttl='1h', ageRecord=False):
        """ uses Add-DnsServerResourceRecordA cmdlet to add a resource in a zone """

        command = PowerShellCommand(
            'Add-DnsServerResourceRecordA',
            'AllowUpdateAny',
            ZoneName=zone,
            Name=name,
            IPv4Address=ip,
            TimeToLive=self._formatTtl(ttl)
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
            TimeToLive=self._formatTtl(ttl)
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

    # ---

    def _formatTtl(self, ttl):
        """
        formatTtl converts given ttl string to Windows-DnsServer module's
        time to live format.

        "1h" -> 01:00:00 # a hour

        "30m" -> 00:30:00 # half an hour

        "1h 30m" -> 01:30:00 # an hour and half an hour

        "1h 30m 45s" -> 01:30:45 # an hour, 30 minutes and 45 seconds

        At least one time unit must be provided

        :param ttl: time to live
        :return: formatted time to live string for Windows-DnsServer module
        """
        hour = 0
        minute = 0
        seconds = 0

        units = ttl.split(' ')
        for unit in units:
            print('h' in unit)
            if 'h' in unit:
                hour = int(unit[:-1])
                continue
            elif 'm' in ttl:
                minute = int(unit[:-1])
                continue
            elif 's' in ttl:
                seconds = int(unit[:-1])
                continue

            raise Exception("time unit could not be determined [%s]" % unit)

        assert hour >= 0 and minute >= 0 and seconds >=0 , ' Time unit can not be negative'
        assert hour > 0 or minute > 0 or seconds > 0, 'At least one time unit must be provided'

        return '%02d:%02d:%02d' % (hour, minute, seconds)