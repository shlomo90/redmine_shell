"""
"Shell" is the class object of Redmine shell. When Rshell instance is
constructed, The instance loads all hierarchy commands of Redmine shell.
Each command has parent or child if it is. the definitions of commands,
you can have a look at "__init__.py in "command" directories.

There are two command types: "CONTAINER", "EXECUTE".
"CONTAINER" means its command must have at least one child. It serves
similar commands as a group.
"EXECUTE" means the command that can just execute a node function.

Cursor class has information of where current shell command position is.
Cursor remembers how many we get in the container commands or out.
Cursor has a responsibility to lookup and walk commands.
"""


import os
import sys
from redmine_shell.command import Root
from redmine_shell.command.system import RedmineSystem
from redmine_shell.command.system.commands import History
from .config import VERSION, VERSION_CHECK_SERVER
from .constants import (
        BANNER_WELCOME, VERSION_CHECK_FORMAT, UPDATE_RECOMMAND_FORMAT,
        UPDATE_WARNING_MESSAGE, )
from .command import CommandType
from .input import redmine_input
from .helper import RedmineHelper
from .switch import get_current_redmine, get_next_redmine


class Shell():
    """ The start entry Class. """

    SYSTEM_COMMANDS = [("?", "Help Menu for Command Usage"),
                       ("help", "Help Menu for Command Usage"),
                       ("project", "Check current redmine's project list."),
                       ("current", "Help Menu for Command Usage"),
                       ("history", "Show history"),
                       ("back", "Go back to previous menu"),
                       ("clear", "Clear current terminal"),
                       ("cls", "Clear current terminal"),
                       ("exit", "Exit the program"),
                       ("switch", "Switch the redmine setting"),
                       ("home", "Go to home"), ]

    def __init__(self):
        self.root = Root("Root")
        self.root.load_children()
        self.system = RedmineSystem("System")
        self.cursor = Cursor(self.root)

        # Connect shell
        self.root.connect_shell(self)
        self.system.connect_shell(self)

    @classmethod
    def version_check(cls):
        """ Check current redmine_shell is updated or outdated. """

        helper = RedmineHelper(VERSION_CHECK_SERVER)
        data = helper.help_redmine(
            helper.wiki_page.get, "Wiki", project_id="test", timeout=3)
        if data is None:
            print("CANNOT CONNECT {} SERVER [TIMEOUT]".format(
                VERSION_CHECK_SERVER))
            return

        wiki = data.text
        versions = []
        for line in wiki.split('\n'):
            if line.startswith('h3. '):
                version = line.replace('h3. ', '').strip()
                versions.append(version)

        try:
            latest_version = versions[0]
        except IndexError:
            print("NO VERSION")
            return

        if VERSION == latest_version:
            print(VERSION_CHECK_FORMAT.format("UPDATED"))
        elif VERSION in versions:
            # OUTDATED
            print(UPDATE_RECOMMAND_FORMAT.format(latest_version))
            print("--> RELEASE NOTE")

            releases = wiki.split('---')
            latest_release = releases[0].strip()
            for line in latest_release.split('\n'):
                if line.startswith('h3. '):
                    continue

                print('    ' + line)
        else:
            print(VERSION_CHECK_FORMAT.format("INVALID"))
            print(UPDATE_WARNING_MESSAGE)

    def banner(self):
        """ Print Banner. """

        print("--------------------- Program Check -----------------------")
        self.version_check()
        print("")

        print("------------------------ BANNER ---------------------------")
        print(BANNER_WELCOME)
        print("-----------------------------------------------------------")

    def execute_command(self, command):
        """ Execute specific command. """

        if not command:
            return

        if self.system.execute_command(command) is True:
            # Save history
            history = History.instance()
            history.append(command)
            return

        child = self.cursor.find_child(command)
        if child is None:
            print("Invalid Command: {}".format(command))
            return

        # Save history
        history = History.instance()
        history.append(child.name)

        self.cursor.move_cursor(child)
        if self.cursor.current.type == CommandType.EXECUTE:
            self.cursor.current.run()
            self.cursor.rollback()
        return

    def do_shell(self):
        """ Start redmine shell. """
        self.banner()

        try:
            while True:
                curr = self.cursor.get_current()

                exe_cmds = self.cursor.list_children()
                sys_cmds = self.system.get_commands()
                tot_cmds = exe_cmds + sys_cmds

                try:
                    name, _, _ = get_current_redmine()
                    line = redmine_input("{}-{}> ".format(name, curr.name),
                                         tot_cmds, history=True).strip()
                # Ctrl-C : Send EOF.
                except KeyboardInterrupt:
                    print("")
                    continue
                # Ctrl-D : Send EOF.
                except EOFError:
                    print("")
                    if len(self.cursor.get_previous()) == 1:
                        line = 'exit'
                    else:
                        line = 'back'

                self.execute_command(line)
        except KeyboardInterrupt:
            print("bye")
            self.cleanup()

    def cleanup(self):
        """ Cleanup before shell close. """

        sys.exit(0)


class Cursor():
    """ Cursor is a helper that points to an hierarchy command. """

    def __init__(self, current):
        self.current = current
        self.prev = [current]

    def get_current(self):
        """ Return Current cursor. """

        return self.current

    def get_previous(self):
        """ Return Previous cursor. """

        return self.prev

    def list_sibling(self):
        """ Return the list of sibling commands. """

        if self.current.parent is None:
            return None

        children = self.current.parent.get_children()
        if len(children) == 1 and children[0] == self.current:
            return None

        return children

    def list_children(self):
        """ REturn the list of children commands. """

        children = self.current.get_children()
        ret = []
        for child in children:
            ret.append(child.name)
        return ret

    def find_child(self, key):
        """ Find current a child command that has the key. """

        if key.isdigit():
            idx = int(key)
            children = self.current.get_children()
            if idx < 0 or idx >= len(children):
                return None
            return children[idx]

        children = self.current.get_children()
        for child in children:
            if child.name == key:
                return child
        return None

    def move_cursor(self, command):
        """ Move cursor. """

        self.prev.append(self.current)
        self.current = command

    def do_question(self, shell):
        """ Print Help messages. """

        current = self.current
        children = current.get_children()
        print("---- Command Menu List ----")
        for i, child in enumerate(children):
            print("{:20}: Shortcut:[{}] {}".format(
                child.name, str(i), child.DESC))
        print("--- System Command List ---")
        for name, desc in shell.system.iter_commands():
            print("{:20}: {}".format(name, desc))
        print("---------- Done ---------")

    def rollback(self, goto_root=False):
        """ Rollback the previous state after an executing command. """

        def _goto_prev():
            self.current = self.prev[-1]

            # prev list must have one element at least.
            if len(self.prev) == 1:
                self.prev = self.prev
            else:
                self.prev = self.prev[:-1]

        if goto_root is True:
            while len(self.prev) != 1:
                _goto_prev()
        else:
            _goto_prev()
