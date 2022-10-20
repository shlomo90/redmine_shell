""" Menu commands structure.

Redmine Shell Menu commands consist of directories as like:
    - issue
    - review_page
    - script
    - wiki
    - configure

When redmine shell starts to be loaded, Shell class instance loads the
This script file and its sub directories in order.
Do load commands. """


from redmine_shell.shell.command import Command, CommandType
from redmine_shell.command.issue import RedmineIssue
from redmine_shell.command.review_page import RedmineReviewPage
from redmine_shell.command.script import RedmineScript
from redmine_shell.command.wiki import RedmineWiki
from redmine_shell.command.template import RedmineTemplate
from redmine_shell.command.configure import RedmineConfigure


class Root(Command):
    """ Root Command class. """

    CHILDREN = [RedmineIssue("issue"),
                RedmineReviewPage("review_page"),
                RedmineScript("script"),
                RedmineWiki("wiki"),
                RedmineTemplate('template'),
                RedmineConfigure('configure'), ]

    def _init_type(self):
        self.type = CommandType.CONTAINER

    def run(self):
        """ EXECUTE TYPE COMMAND SHOULD BE OVERRIDEN """
        raise NotImplementedError("name:{} function:run".format(self.name))
