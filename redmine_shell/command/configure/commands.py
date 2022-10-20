''' Issue Commands. '''


import os
import time
import json
import datetime
import tempfile
import requests
import webbrowser

from redmine_shell.shell.config import DEBUG, DEFAULT_EDITOR
from redmine_shell.shell.switch import (
    get_current_redmine, get_current_redmine_preview,
    get_current_redmine_week_report_issue, get_current_redmine_config)
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.shell.helper import RedmineHelper
from redmine_shell.shell.error import InputError
from redmine_shell.shell.inventory import Inventory
from redmine_shell.command.system.commands import (
    ListProject, ListTracker, ListAssignUser, ListStatus)
from threading import Thread
from urllib import parse



# Surpress warning messages.
requests.packages.urllib3.disable_warnings()


def _get_value(line):
    start_index = line.find('[')
    end_index = line.rfind(']')
    if start_index == -1 or end_index == -1:
        raise InputError("There is no square brackets")
    else:
        return line[start_index+1:end_index]


CREATE_HELP_MESSAGE = '''
User information to be created
> USER: []
> URL: []
> KEY: []
'''

class CreateUser(Command):
    ''' Create User Command. '''
    name = "create_user"
    DESC = "Create User"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        '''
        User information to be created
        > USER: []
        > URL: []
        > KEY: []
        '''

        # write your user info down.
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)
        answer = ri.help_user_input(CREATE_HELP_MESSAGE.encode())

        # get the user, key values
        kwargs = {}
        for line in answer.split('\n'):
            try:
                line = line.strip()
                if line.startswith('> USER') is True:
                    kwargs['USER'] = _get_value(line)
                elif line.startswith('> URL') is True:
                    kwargs['URL'] = _get_value(line)
                elif line.startswith('> KEY') is True:
                    kwargs['KEY'] = _get_value(line)
            except:
                continue

        return self.create_config(kwargs)

    def create_config(self, kwargs):
        home = os.environ.get("HOME")
        path = "{}/.redmine_shell_rc".format(home)
        with open(path, 'r') as f:
            rc = json.load(f)

        user = kwargs['USER']
        del kwargs['USER']
        for name, conf in rc.items():
            if name == user:
                #duplicated.
                print("USER:{} Name is duplicated.".format(name))
                return

        rc[user] = {}
        rc[user].update(kwargs)

        with open(path, "w") as f:
            json.dump(rc, f)
        return 'reload'


DELETE_HELP_MESSAGE = '''
User information to be deleted
> USER: []
'''

class DeleteUser(Command):
    ''' Delete User Command. '''
    name = "delete_user"
    DESC = "Delete User"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        '''
        Delete User
        > User: []
        '''

        conf = self.get_config()
        users = conf.keys()

        help_messages = ['--- User Lists ---']
        for name, _ in conf.items():
            help_messages.append(name)
        help_messages.append('')
        help_messages.append(DELETE_HELP_MESSAGE)

        # write your user info down.
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)
        answer = ri.help_user_input('\n'.join(help_messages).encode())

        # get the user, key values
        kwargs = {}
        for line in answer.split('\n'):
            try:
                line = line.strip()
                if line.startswith('> USER') is True:
                    kwargs['USER'] = _get_value(line)
            except:
                continue

        return self.delete_config(kwargs)

    def get_config(self):
        home = os.environ.get("HOME")
        path = "{}/.redmine_shell_rc".format(home)
        with open(path, 'r') as f:
            rc = json.load(f)
        return rc

    def delete_config(self, kwargs):
        home = os.environ.get("HOME")
        path = "{}/.redmine_shell_rc".format(home)
        with open(path, 'r') as f:
            rc = json.load(f)

        user = kwargs['USER']
        if user in rc:
            del rc[user]
            with open(path, "w") as f:
                json.dump(rc, f)
            return 'reload'
