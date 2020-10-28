from collections.abc import Iterable

from ..dns.record import Record, RecordType


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
    assert isinstance(ttl, str)
    assert len(ttl) > 0, "empty ttl value"

    hour = 0
    minute = 0
    seconds = 0

    units = ttl.split(' ')
    for unit in units:
        if 'h' in unit:
            hour = int(unit[:-1])
            continue
        elif 'm' in unit:
            minute = int(unit[:-1])
            continue
        elif 's' in unit:
            seconds = int(unit[:-1])
            continue

        raise Exception("time unit could not be determined [%s]" % unit)

    assert hour < 24, 'hour can not be more than 23'
    assert minute < 60, 'minute can not be more than 59'
    assert seconds < 60, 'seconds can not be more than 59'

    assert hour >= 0 and minute >= 0 and seconds >= 0, 'Time unit can not be negative'
    assert hour > 0 or minute > 0 or seconds > 0, 'At least one time unit must be provided'

    return '%02d:%02d:%02d' % (hour, minute, seconds)


def parseTtl(timeToLive):
    hours = timeToLive['Hours']
    minutes = timeToLive['Minutes']
    seconds = timeToLive['Seconds']

    ttl_str = ''
    if hours:
        ttl_str += '%sh ' % hours

    if minutes:
        ttl_str += '%sm ' % minutes

    if seconds:
        ttl_str += '%ss ' % seconds

    return ttl_str[:-1]


def isRecordTypeSupported(recordType):
    return recordType in RecordType.list()


def formatDnsServerResult(zone, cmdletResults):
    if not isinstance(cmdletResults, list):
        cmdletResults = [cmdletResults]

    recordResults = []
    for result in cmdletResults:
        name = result['HostName']
        recordType = result['RecordType']

        if not isRecordTypeSupported(recordType):
            continue

        recordDataProperties = result['RecordData']['CimInstanceProperties']

        recordData = dict()
        if isinstance(recordDataProperties, str):
            key, value = recordDataProperties.split('=')
            # value's has at begin and end, remove it
            recordData[key.strip()] = value[1:-1]
        else:
            for props in recordDataProperties:
                key, value = props.split('=')
                recordData[key.strip()] = value

        assert len(recordData) < 2, "Unexpected data, expected only one record data property, actual: [%s]" % recordData

        content = next(iter(recordData.values()))
        ttl = parseTtl(result['TimeToLive'])

        recordResults.append(Record(zone, name, RecordType.value_of(recordType), content, ttl))

    return recordResults
