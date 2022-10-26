''' System Commands
'''


import os
from redmine_shell.shell.switch import get_current_redmine, get_next_redmine
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.shell.helper import RedmineHelper
from redmine_shell.shell.singleton import SingletonInstane
from redmine_shell.shell.constants import DATA_PATH, HOME_PATH
import pyperclip3 as pc


HISTORY_PATH = HOME_PATH + '/.redmine_shell/history'


class Help(Command):
    """ Help system command. """
    DESC = "Help Menu for Command Usage"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        shell.cursor.do_question(shell)


class Question(Help):
    pass


class Current(Help):
    pass


class History(Command, SingletonInstane):
    """ History Class.

    Load history commands from a history file and print them.
    Also, Append new commands to the file.
    """

    DESC = "Show history"
    history_contents = []

    def load(self):
        """ Read the history file. """
        return self.history_contents

    def append(self, command):
        """ Append a new command to the history. """
        self.history_contents.append(command)

    def run(self, shell):
        """ EXECUTE TYPE COMMAND SHOULD BE OVERRIDEN """

        commands = self.load()
        print("============================")
        if commands:
            print("\n".join(commands))
        else:
            print("No history")
        print("============================")


class HistoryMove():
    ''' History Moving. '''
    def __init__(self, history=None):
        if history is None:
            self.history = []
        else:
            self.history = history
        self.free = []

    @classmethod
    def _move(cls, dst, src):
        try:
            cmd = src.pop()
        except IndexError:
            return None
        dst.append(cmd)
        return cmd

    def move_up(self):
        ''' Lookup history upward. '''
        return HistoryMove._move(self.free, self.history)

    def move_down(self):
        ''' Lookup history downward. '''
        return HistoryMove._move(self.history, self.free)


class Back(Command):

    DESC = "Go back to previous menu"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        shell.cursor.rollback()


class Home(Command):
    DESC = "Go to home"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        shell.cursor.rollback(goto_root=True)


class Clear(Command):
    DESC = "Clear current terminal"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        os.system("clear")


class Cls(Clear):
    pass


class Exit(Command):
    DESC = "Exit the program"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        print("bye!")
        shell.cleanup()


class Switch(Command):
    DESC = "Switch the redmine setting"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        get_next_redmine()


class ListProject(Command):
    ''' List Project Command. '''
    DESC = "Check current redmine's project list."

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)
        lines = self.get_project_lines(ri)
        text = '\n'.join(lines)
        ri.help_user_input(text.encode())
        print(text)

    @classmethod
    def get_project_lines(cls, ri):
        lines = ["pid: project name", "---+----------------"]
        for project in ri.project.all():
            pid = project.id
            pname = project.name
            lines.append("{: >3}: {}".format(pid, pname))
        return lines


class ListTracker(Command):
    ''' List Tracker Command. '''
    DESC = "Check current redmine's Tracker list."

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)
        lines = self.get_tracker_lines(ri)
        text = '\n'.join(lines)
        ri.help_user_input(text.encode())
        print(text)
        return text

    @classmethod
    def get_tracker_lines(cls, ri):
        lines = ["tid: tracker name", "---+----------------"]
        for tracker in ri.tracker.all():
            tid = tracker.id
            tname = tracker.name
            lines.append("{: >3}: {}".format(tid, tname))
        return lines


class ListAssignUser(Command):
    ''' List Assign Users Command. '''
    DESC = "Check current redmine's Assigned Users list."

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)
        lines = self.get_user_lines(ri)
        text = '\n'.join(lines)
        ri.help_user_input(text.encode())
        print(text)
        return text

    @classmethod
    def get_user_lines(cls, ri):
        lines = ["Ass: User name", "---+----------------"]
        for user in ri.user.all():
            uid = user.id
            uname = "{} {}".format(user.firstname, user.lastname)
            lines.append("{: >3}: {}".format(uid, uname))
        return lines


class ListStatus(Command):
    ''' List Status Command. '''
    DESC = "Check current redmine's Status list."

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)
        lines = self.get_status_lines(ri)
        text = '\n'.join(lines)
        ri.help_user_input(text.encode())
        print(text)
        return text

    @classmethod
    def get_status_lines(cls, ri):
        lines = ["sid: Status name", "---+----------------"]
        for value in ri.issue_status.all().values():
            sid = value['id']
            sname = value['name']
            lines.append("{: >3}: {}".format(sid, sname))
        return lines



class CopyScript(Command):
    ''' Copy the script in clipboard. '''
    DESC = "Copy the script in clipboard."

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        from redmine_shell.shell.input import redmine_input
        script = redmine_input("script: ").strip()
        _, url, key = get_current_redmine()
        path = os.path.abspath('/'.join([DATA_PATH, key, script, 'memo']))
        if os.path.exists(path) is False:
            print("No script")
            return True

        with open(path, 'r') as f:
            data = f.read()

        pc.copy(data)
        print("Copy Done!")


class StartShell(Command):
    ''' Enter the bash shell. '''
    DESC = "Start Shell"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self, shell):
        os.system('/bin/bash')
        return
