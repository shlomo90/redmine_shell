"""
"Shell" is an entry class of redmine_shell. The shell commands are loaded
when it constructs a "Shell" instance. (See __init__)

Here are commands hiararchy. (order by my preference)

* issue
** update_issue
** read_issue
** list_issue
** list_journal
** weekreport_issue (feature_open_weekreport)
* wiki
** update_wiki
** read_wiki
* review_page
** new_review_page
* todo
** show_todo
** show_todo_all
** create_todo
** edit_todo
** remove_todo
"""


import sys
from redmine_shell.command import Root
from redmine_shell.command.system import RedmineSystem
from redmine_shell.command.system.commands import History
from .constants import (
        BANNER_WELCOME, UPDATE_RECOMMAND_FORMAT,
        UPDATE_WARNING_MESSAGE, )
from .command import CommandType
from .input import redmine_input
from .helper import RedmineHelper
from .switch import get_current_redmine, LoginError


class Shell():
    """ The start entry Class. """

    def __init__(self):
        # Normal Commands
        self.root = Root("Root")
        self.root.load_children()

        # To help navigating
        self.cursor = Cursor(self.root)

        # System Commands
        self.system = RedmineSystem("System")
        self.system.load_children()

        # Root, System commands connect to Shell
        self.root.connect_shell(self)
        self.system.connect_shell(self)

    def banner(self):
        """ Print Banner. """

        print("")
        print("------------------------ BANNER ---------------------------")
        print(BANNER_WELCOME)
        print("")

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

    def load_run_commands(self):
        ''' Load "~/.redmine_shell_rc".

        return:
            (True, None): Load Success.
            (False, "error message"): Load Failed and Reason.
        '''

        # Make singleton Login instance to load "~/.redmine_shell_rc" file.
        try:
            login = get_current_redmine()
        except LoginError as le:
            return False, le.args[0]

        return True, None

    def start(self):
        """ Start redmine shell. """
        result, err = self.load_run_commands()
        if result is False:
            print("ERR: {}".format(err))
            self.cleanup()

        self.banner()
        self.interactive()

    def interactive(self):
        try:
            while True:
                exe_cmds = self.cursor.list_children()
                # system commands doen't use Cursor.
                sys_cmds = self.system.get_commands()
                tot_cmds = exe_cmds + sys_cmds

                try:
                    name = get_current_redmine()[0]   #0: name
                    curr = self.cursor.get_current()
                    line = redmine_input(
                        "{}-{}> ".format(name, curr.name),
                        tot_cmds, history=True
                    ).strip()

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

    def batch(self, commands, remember_cursor=False):
        save_cursor = self.cursor.duplicate()

        # Start from Root
        self.cursor.goto_root()

        try:
            for cmd in commands:
                exe_cmds = self.cursor.list_children()
                # system commands doen't use Cursor.
                sys_cmds = self.system.get_commands()
                tot_cmds = exe_cmds + sys_cmds

                name = get_current_redmine()[0]   #0: name
                curr = self.cursor.get_current()
                print("Run: {}".format(cmd))
                self.execute_command(cmd)
        except KeyboardInterrupt:
            print("bye")
            self.cleanup()

        if remember_cursor is True:
            self.cursor = save_cursor
        return True

    def cleanup(self):
        """ Cleanup before shell close. """

        sys.exit(0)


class Cursor():
    """ Cursor class to help navigating commands.

    Each command may have parents or children. Users can get in or out of
    "container" type commands. Cursor provides some APIs to navigate them.
    """

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
        """ Return the list of children commands. """

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

        if goto_root is True:
            self.goto_root()
        else:
            self._goto_prev()

    def goto_root(self):
        while len(self.prev) != 1:
            self._goto_prev()

    def _goto_prev(self):
        self.current = self.prev[-1]

        # prev list must have one element at least.
        if len(self.prev) == 1:
            self.prev = self.prev
        else:
            self.prev = self.prev[:-1]

    def duplicate(self):
        ''' duplicate current cursor instance. '''
        from copy import deepcopy
        return deepcopy(self)
