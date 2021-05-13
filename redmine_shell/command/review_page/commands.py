''' Review Page Commands. '''


import datetime
from redmine_shell.shell.switch import get_current_redmine
from redmine_shell.shell.constants import TEMPLATE_COMMON, TEMPLATE_CONTENT
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.shell.helper import RedmineHelper


WEEKDAY_MAP = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}


def get_current_date_format():
    ''' Return current date. '''

    time_fmt = datetime.datetime.now()
    return (time_fmt.year, time_fmt.month, time_fmt.day,
            WEEKDAY_MAP[time_fmt.weekday()])


class RedmineReviewPage(RedmineHelper):
    ''' Redmine Review Page Command. '''

    def edit_template_text(self, template):
        ''' Edit Template Text. '''

        text = self.help_user_input(template.encode()).strip()
        new = []
        for line in text.split('\n'):
            line = line.strip()
            if line == '':
                new.append(line)
                continue

            if line[0] == '#':
                continue

            new.append(line)

        return '\n'.join(new).strip()

    def new_review_page(self):
        ''' New Review Page. '''

        issue = self.help_ask_issue_number()
        if not issue:
            return False

        subject = self.help_get_issue_subject(issue)
        if not subject:
            return False

        year, month, day, weekday = get_current_date_format()

        pages = []
        # Tempfile for template.
        template = TEMPLATE_COMMON.format(issue=issue, subject=subject,
                                          year=year, month=month, day=day,
                                          weekday=weekday)
        pages.append(self.edit_template_text(template))
        template = TEMPLATE_CONTENT
        pages.append(self.edit_template_text(template))

        review = '\r\n'.join(pages)
        self.issue.update(issue, notes=review)
        return True

    def help_execute(self):
        """ Execute command. """
        raise NotImplementedError("function: help_execute not implemented")


class NewReviewPage(Command):
    ''' New Review Page Command. '''
    DESC = "Create Issue's Review Page"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, url, key = get_current_redmine()
        rrp = RedmineReviewPage(url=url, key=key)
        return rrp.new_review_page()


class UpdateReviewPage(Command):
    ''' Update Review Page Command. '''
    DESC = "Update Issue's Review Page"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        print("Not Implemented Yet")
        return True
