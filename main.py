from microsoftdnsserver.command_runner.powershell_runner import PowerShellRunner
from microsoftdnsserver.dns.dnsserver import DnsServerModule

if __name__ == '__main__':
    runner = PowerShellRunner()
    dns = DnsServerModule(runner)

#     dns.addARecord("zone", "bilalekrem.com", "192.168.100.150", ttl='10s')

    dns.addTxtRecord("bilalekrem.com", "bilalekrem.com", "testrecord", ttl='10s')
