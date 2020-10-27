def formatTtl(ttl):
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

    assert hour >= 0 and minute >= 0 and seconds >=0, ' Time unit can not be negative'
    assert hour > 0 or minute > 0 or seconds > 0, 'At least one time unit must be provided'

    return '%02d:%02d:%02d' % (hour, minute, seconds)

def formatDnsServerResult(result):
    response = {
        'DistinguishedName': result['DistinguishedName'],
        'HostName': result['HostName'],
        'RecordClass': result['RecordClass'],
        'RecordType': result['RecordType'],
        'TimeToLive': result['TimeToLive']['TotalMilliseconds']
    }

    # --
    recordDataProperties = result['RecordData']['CimInstanceProperties']
    _, value = recordDataProperties.split('=')
    response['RecordData'] = value

    return response
