"""
Author: shlomo90

redmine_shell is a program based on shell terminal.
It helps easily to edit issues, wiki, etc. in your redmine server.
If you are a heavy CLI terminal user (or vim?), This is the one
you are looking for.
"""


from redmine_shell.shell import Shell


def debug_on():
    import sys
    import redmine_shell.shell.config as config

    if "debug" not in sys.argv:
        return

    # config.DEBUG is singleton.
    config.DEBUG = True


if __name__ == "__main__":
    debug_on()

    redmine_shell = Shell()
    redmine_shell.start()
