class Record(object):

    def __init__(self, zone, name, type, content, ttl=1):
        self.zone = zone
        self.name = name
        self.type = type
        self.content = content
        self.ttl = ttl