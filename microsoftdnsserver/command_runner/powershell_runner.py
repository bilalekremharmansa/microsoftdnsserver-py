import subprocess

from .runner import Command, CommandRunner, Result
from ..util import logger


DEFAULT_POWERSHELL_EXE_PATH = "C:\Windows\syswow64\WindowsPowerShell\\v1.0\powershell.exe"


class PowerShellCommand(Command):

    def __init__(self, cmdlet: str, *flags, **args):
        super().__init__()

        self.cmdlet = cmdlet
        self.flags = flags
        self.args = args

    def prepareCommand(self):
        cmd = [self.cmdlet]

        # add flags, ie -Force
        for flag in self.flags:
            cmd.append('-%s' % flag)

        # add arguments
        for arg, value in self.args.items():
            cmd.append('-%s %s' % (arg, value))

        # convert to json to make machine readable
        cmd.append('|')
        cmd.append('ConvertTo-Json')

        return cmd

    def _postProcessResult(self):
        pass


class PowerShellRunner(CommandRunner):

    def __init__(self, powerShellPath: str = None):
        self.logger = logger.createLogger("PowerShellRunner")

        self.powerShellPath = powerShellPath
        if powerShellPath is None:
            self.powerShellPath = DEFAULT_POWERSHELL_EXE_PATH

    def run(self, command: PowerShellCommand) -> Result:
        assert isinstance(command, PowerShellCommand)

        cmd = command.prepareCommand()
        cmd.insert(0, self.powerShellPath)

        self.logger.debug("Running: [%s]" % ' '.join(cmd))

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            out, err = proc.communicate(timeout=60)
        except:
            proc.kill()
            out, err = proc.communicate()
        finally:
            pass

        out = out.decode('utf-8')
        err = err.decode('utf-8')

        self.logger.debug("Returned: \n\tout:[%s], \n\terr:[%s]" % (out, err))

        success = proc.returncode == 0
        return Result(success, proc.returncode, out, err)



