import subprocess
import sys

from .runner import Command, CommandRunner, Result

DEBUG=True

class PowerShellCommand(Command):

    def __init__(self, cmdlet, *flags, **args):
        super().__init__()

        self.cmdlet = cmdlet
        self.flags = flags
        self.args = args

    def prepareCommand(self):
        cmd = ['powershell.exe', self.cmdlet]

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

    def run(self, command):
        assert (command, PowerShellCommand)

        cmd = command.prepareCommand()

        if DEBUG:
            print(' '.join(cmd))
            return

        proc = subprocess.Popen(cmd, stdout=sys.stdout)
        try:
            out, _ = proc.communicate(timeout=60)
        except:
            proc.kill()
            out, _ = proc.communicate()
        finally:
            pass

        success = proc.returncode == 0
        return Result(success, proc.returncode, out)



