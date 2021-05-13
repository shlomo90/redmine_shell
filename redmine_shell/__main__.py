"""
Author: shlomo90

"redmine_shell" is a shell program to edit a redmine server easily for
CLI Command users. This program basically uses "python-redmine"
module that is an APIs to communicate a redmine server by REST API.
This program is also interactive and supports basic things of Bash shell."""


import sys
import redmine_shell.shell.config as config
from redmine_shell.shell import Shell


def debug_on():
    if "debug" in sys.argv:
        # config.DEBUG is singleton.
        config.DEBUG = True


if __name__ == "__main__":
    debug_on()
    Shell().do_shell()
