''' Issue Commands. '''


import os
import time
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


class CreateUser(Command):
    ''' Create User Command. '''
    name = "create_user"
    DESC = "Create User"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        '''
        User information to be created
        > User: []
        > Url: []
        > Key: []
        '''

        # open help messages
        # write your user info down.
        # get the user, key values
        # open ~/.redmine_shell_rc
        # check the name is duplicated 
        # Add the information
        # Done

        #{
        #    "NAME": {
        #        "URL": "xxxxxxxxxxxxxxxxxxxxxx",
        #        "KEY": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        #    }
        #}
        pass


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

        # open help messages
        # write your user info down.
        # get the user value
        # open ~/.redmine_shell_rc
        # check the name exists
        # if user is only one, no success.
        # Delete the information
        # save ~/.redmine_shell_rc
        # If current user is the one switch
        # Done

        #{
        #    "NAME": {
        #        "URL": "xxxxxxxxxxxxxxxxxxxxxx",
        #        "KEY": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        #    }
        #}
        pass
