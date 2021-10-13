''' Redmine Script Command. '''


from redmine_shell.shell.config import DEBUG
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.command.script.commands import (
    RunScript, CreateScript, EditScript, RemoveScript, ShowScriptAll)


COMMAND = [
        RunScript("run"),
        ShowScriptAll("show_all"),
        CreateScript("create"),
        EditScript("edit"),
        RemoveScript("remove"),
]


class RedmineScript(Command):
    ''' Redmine Script Class. '''

    CHILDREN = COMMAND
    DESC = "Script setting for Redmine."

    def _init_type(self):
        self.type = CommandType.CONTAINER

    def run(self):
        """ EXECUTE TYPE COMMAND SHOULD BE OVERRIDEN """
        raise NotImplementedError("name:{} function:run".format(self.name))
