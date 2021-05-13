from redmine_shell.shell.config import DEBUG
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.command.review_page.commands import (
    NewReviewPage, UpdateReviewPage)
from redmine_shell.command.system.commands import (
    Help, ListProject, Question, Current, History, Back, Clear, Cls, Exit,
    Switch, Home)


COMMAND = [
    Help("help"),
    Question("?"),
    Current("current"),
    History.instance("history"),
    Back("back"),
    Clear("clear"),
    Cls("cls"),
    Exit("exit"),
    Switch("switch"),
    Home("home"),
    ListProject("project"), ]


class RedmineSystem(Command):
    ''' Redmine System Commands. '''

    name = "System"
    CHILDREN = COMMAND

    def _init_type(self):
        self.type = CommandType.SYSTEM

    def find_child(self, command):
        for child in self.CHILDREN:
            if child.name == command:
                return child

        return None

    def get_commands(self):
        names = []
        for child in self.CHILDREN:
            names.append(child.name)

        return names
    
    def execute_command(self, command):
        """ Execute System commands. """

        child = self.find_child(command)
        if child:
            child.run(self.shell)
            return True
        else:
            return False

    def iter_commands(self):
        for child in self.CHILDREN:
            yield child.name, child.DESC
