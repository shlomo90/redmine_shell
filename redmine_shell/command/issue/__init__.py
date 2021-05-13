''' Issue Commands. '''


from redmine_shell.shell.config import DEBUG
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.command.issue.commands import (ListIssue, CreateIssue,
        ReadIssue, UpdateIssue, ListJournal)


COMMAND = [ListIssue("list_issue"), CreateIssue("create_issue"),
           ReadIssue("read_issue"), UpdateIssue("update_issue"),
           ListJournal("list_journal"), ]


class RedmineIssue(Command):
    CHILDREN = COMMAND
    DESC = "Edit Redmine Issue"

    def __init__(self, name):
        super(RedmineIssue, self).__init__(name)


    def _init_type(self):
        self.type = CommandType.CONTAINER
