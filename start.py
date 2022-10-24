import os
from redmine_shell.shell import Shell


def debug_on():
    import redmine_shell.shell.config as config
    # config.DEBUG is singleton.
    config.DEBUG = True


def init(mode):
    if mode == 'debug':
        debug_on()


if __name__ == "__main__":
    mode = os.environ.get("REDMINE_SHELL_MODE", "normal")
    init(mode)
    shell = Shell()
    shell.start()
