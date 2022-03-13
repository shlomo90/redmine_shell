''' Redmine Template Command. '''


from redmine_shell.shell.config import DEBUG
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.command.template.commands import (
    CreateTemplate, RemoveTemplate, EditTemplate, ReadTemplate,
    ListTemplate)


COMMAND = [
        CreateTemplate("create"),
        RemoveTemplate("remove"),
        EditTemplate("edit"),
        ReadTemplate("read"),
        ListTemplate("list"),
]


class RedmineTemplate(Command):
    ''' Redmine Template Class. '''

    CHILDREN = COMMAND
    DESC = "Template setting for Redmine."

    def _init_type(self):
        self.type = CommandType.CONTAINER

    def run(self):
        """ EXECUTE TYPE COMMAND SHOULD BE OVERRIDEN """
        raise NotImplementedError("name:{} function:run".format(self.name))
