from microsoftdnsserver.exception.exception_common import MethodNotImplementedError


class Command(object):

    def prepareCommand(self):
        raise MethodNotImplementedError()


class CommandRunner(object):

    def run(self, cmd):
        raise MethodNotImplementedError()


class Result(object):

    def __init__(self, success, code, out, err):
        self.success = success
        self.code = code
        self.out = out
        self.err = err