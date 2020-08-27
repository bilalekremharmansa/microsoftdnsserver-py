from microsoftdnsserver.command_runner.powershell_runner import PowershellCommand
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

        command = PowershellCommand('Get-DnsServerResourceRecord', **args)
        result = self.runner(command)


    def addARecord(self, zone, name, ip, ttl='1h', ageRecord=False):
        """ uses Add-DnsServerResourceRecordA cmdlet to add a resource in a zone """

        command = PowershellCommand(
            'Add-DnsServerResourceRecordA',
            'AllowUpdateAny',
            ZoneName=zone,
            Name=name,
            IPv4Address=ip,
            TimeToLive=self._formatTtl(ttl)
        )

        result = self.runner(command)

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

        command = PowershellCommand('Remove-DnsServerResourceRecord', *flags, **args)
        result = self.runner(command)


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
            if 'h' in ttl:
                hour = int(ttl[-1])
            elif 'm' in ttl:
                minute = int(ttl[-1])
            elif 's' in ttl:
                seconds = int(ttl[-1])

            raise Exception("time unit could not be determined [%s]" % unit)

        assert hour >= 0 and minute >= 0 and seconds >=0 , ' Time unit can not be negative'
        assert hour > 0 or minute > 0 or seconds > 0, 'At least one time unit must be provided'

        return '%s:%s:%s' % (hour, minute, seconds)