''' Wiki Commands. '''


from redmine_shell.shell.command import Command, CommandType
from redmine_shell.command.wiki.commands import ReadWiki, UpdateWiki


COMMAND = [ReadWiki("read_wiki"), UpdateWiki("update_wiki"), ]


class RedmineWiki(Command):
    CHILDREN = COMMAND
    DESC = "Redmine Wiki"

    def _init_type(self):
        self.type = CommandType.CONTAINER
