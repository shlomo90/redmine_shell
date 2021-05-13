''' Review Page Menu. '''


from redmine_shell.shell.config import DEBUG
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.command.review_page.commands import (
        NewReviewPage, UpdateReviewPage)


COMMAND = [NewReviewPage("new_review_page"),
           UpdateReviewPage("update_review_page"),]


class RedmineReviewPage(Command):
    ''' Redmine Review Page Menu. '''

    name = "review_page"
    DESC = "Review Page"
    CHILDREN = COMMAND

    def _init_type(self):
        self.type = CommandType.CONTAINER

    def run(self):
        """ EXECUTE TYPE COMMAND SHOULD BE OVERRIDEN """
        raise NotImplementedError("name:{} function:run".format(self.name))
