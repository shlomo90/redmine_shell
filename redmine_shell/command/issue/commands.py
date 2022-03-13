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
    get_current_redmine_week_report_issue)
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.shell.helper import RedmineHelper
from redmine_shell.shell.error import InputError
from redmine_shell.command.system.commands import (
    ListProject, ListTracker, ListAssignUser)
from threading import Thread
from urllib import parse



# Surpress warning messages.
requests.packages.urllib3.disable_warnings()


class CreateIssue(Command):
    ''' Create Issue Command. '''
    name = "create_issue"
    DESC = "Create Issue"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        # Just create Redmine Issue with project ID.
        # Rest configurations will be updated by "edit_issue"
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)
        pid = ri.help_ask_project_number()
        if pid is None:
            return True

        # TODO: Need to ask user id (Assigned_ID)

        try:
            issue = ri.help_create_issue(pid)
        except:
            print("Create Issue Failed.")
            return True

        try:
            ri.help_edit_description(issue.id)
        except:
            print("Edit description Fail")
            return True
        return True


class ListIssue(Command):
    ''' List Issue Command. '''
    name = "list_issue"
    DESC = "List Issue"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def _load_issues(self, ri, pid, limit, offset):
        issues = ri.issue.filter(project_id=pid, limit=limit, offset=offset)

    def buffer_issues(self, ri, pid, limit, offset):
        t = Thread(target=self._load_issues, args=(ri, pid, limit, offset))
        t.start()

    def _print_list_issue(self, issues):
        lines = ["issue: [pic] project name", "-----+----------------"]
        try:
            for issue in issues:
                try:
                    lines.append("{: >5}: [{}] {}".format(
                        issue.id, issue.assigned_to, issue.subject))
                except Exception:
                    lines.append("{: >5}: [       ] {}".format(
                        issue.id, issue.subject))
        except Exception:
            print("Err...")
            return None
        return lines

    def run(self):
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)
        pid = ri.help_ask_project_number()
        if pid is None:
            return True

        data = {'return': None, 'redmine_issue': ri,
                'project_number': pid, 'limit': 500,
                'offset': 0}

        def _get_contents(data):
            ri = data['redmine_issue']
            issues = ri.issue.filter(project_id=data['project_number'],
                                     limit=data['limit'],
                                     offset=data['offset'])
            data['return'] = self._print_list_issue(issues)

        t = Thread(target=_get_contents, args=(data,))
        t.start()

        while True:
            t.join()
            t = None

            contents = data['return']
            if not contents:
                break

            if len(contents) != data['limit'] + 2: #headers
                ri.help_user_input('\n'.join(data['return']).encode())
                break
            else:
                # buffering
                data['return'] = None
                data['offset'] += data['limit']
                t = Thread(target=_get_contents, args=(data,))
                t.start()

                ri.help_user_input('\n'.join(contents).encode())

                from redmine_shell.shell.input import redmine_input
                try:
                    cont = redmine_input("Continue?(y/n) ")
                except EOFError:
                    print("")
                    return True
                except KeyboardInterrupt:
                    print("")
                    return True

                if cont == 'y':
                    continue
                else:
                    break
        return True


class ReadIssue(Command):
    ''' Read Issue Command. '''
    name = "read_issue"
    DESC = "Read Issue"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        # TODO: Get api_key from .api_key
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url,
                          key=key)
        issue = ri.help_ask_issue_number()
        if issue is None:
            return True
        try:
            desc = ri.help_get_description(issue)
        except:
            print("Get description Fail")
            return True

        ri.help_user_input(desc.encode())
        return True


class UpdateIssue(Command):
    ''' Update Issue Command. '''
    DESC = "Update Issue"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def _preview_checker(self, path, ri):
        # This is already validated.
        pnum, wname = get_current_redmine_preview()
        if pnum is None or wname is None:
            print("No set PREVIEW_WIKI_NAME, PREVIEW_PROJ_NUM")
            return True

        # Check period time is one second.
        period = 1

        # The exit condition is the file (not swapfile) is closed.
        # Parent process will delete the file after editting is done.
        last_mtime = 0
        while os.path.isfile(path) is True:
            time.sleep(period)

            latest_mtime = os.stat(path).st_mtime
            if latest_mtime != last_mtime:
                # Read the new edited file
                with open(path, 'r') as fobj:
                    data = fobj.read()
                ri.wiki_page.update(wname, project_id=pnum, text=data)
                last_mtime = latest_mtime

    def run(self):
        # TODO: Get api_key from .api_key
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url,
                          key=key)
        issue = ri.help_ask_issue_number()
        if issue is None:
            return True

        if ri.help_ask_yes_or_no(
                "Do you wanna use preview of issue?(y/N) ",
                default_yes=False) is True:
            pnum, wname = get_current_redmine_preview()
            # PREVIEW_WIKI_NAME, PREVIEW_PROJ_NUM
            # should be imported without errors.
            # These variables are used for the access temporary wiki page
            # as a preview.
            if pnum is None or wname is None:
                print("No set PREVIEW_WIKI_NAME, PREVIEW_PROJ_NUM")
                return None

            url_path = 'redmine.piolink.com/projects/{}/wiki/{}'.format(
                    pnum, wname)

            url_addr = 'https://' + parse.quote(url_path)

            webbrowser.open_new(url_addr)

            # NamedTemporaryFile instance should have "delete" flag False.
            # Because "help_user_input" uses the "delete" mode temp file.
            tfile = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)

            t = Thread(target=self._preview_checker, args=(tfile.name, ri))
            t.start()

            # Load issue's description and open an interactive editor.
            desc = ri.help_get_description(issue)
            cnt = ri.help_user_input(desc.encode(), _temp=tfile)

            # Removing the tempfile triggers to exit the thread.
            os.unlink(tfile.name)
            t.join()

            ret = ri.help_ask_yes_or_no(
                "Are you sure?(y/N) ", default_yes=False)
            if not ret:
                return True

            # Show what you've edited.
            print(cnt)
            ri.help_update_description(issue, cnt)
            return True

        else:
            try:
                ri.help_edit_description(issue)
            except:
                print("Edit description Fail")
                return True
        return True


class ListJournal(Command):
    ''' List Journal Command. '''
    DESC = "List issue's journals"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def run(self):
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)

        from redmine_shell.shell.input import redmine_input
        try:
            nissue = redmine_input("Issue number: ")
        except EOFError:
            print("")
            return True
        except KeyboardInterrupt:
            print("")
            return True

        if nissue.isdigit() is False:
            print("Error: Plz Input digital number!")
            return True

        lines = []
        issue = ri.issue.get(nissue, include=['journals'])
        for journal in issue.journals:
            print(dir(journal))
            lines.append("Journal ID: {}\n{}".format(
                journal.id, journal.notes.replace('\r', '').strip()))
        msg = '\n====================================\n'.join(lines)
        ri.help_user_input(msg.encode())


class WeekReportIssue(Command):
    ''' Update WeekReport Issue Command. '''
    DESC = "Week Report Issue"

    def _init_type(self):
        self.type = CommandType.EXECUTE

    def _preview_checker(self, path, ri):
        # This is already validated.
        pnum, wname = get_current_redmine_preview()
        if pnum is None or wname is None:
            print("No set PREVIEW_WIKI_NAME, PREVIEW_PROJ_NUM")
            return True

        # Check period time is one second.
        period = 1

        # The exit condition is the file (not swapfile) is closed.
        # Parent process will delete the file after editting is done.
        last_mtime = 0
        while os.path.isfile(path) is True:
            time.sleep(period)

            latest_mtime = os.stat(path).st_mtime
            if latest_mtime != last_mtime:
                # Read the new edited file
                with open(path, 'r') as fobj:
                    data = fobj.read()
                ri.wiki_page.update(wname, project_id=pnum, text=data)
                last_mtime = latest_mtime

    def _get_latest_subtask_issue(self, issue, url, key):
        ''' Get latest subtask issue id.
        '''

        week_url = '/'.join([url, "issues", str(issue) + '.json?include=children'])
        headers = {
            'Content-Type': 'application/json',
            'X-Redmine-API-Key': key,
        }

        session = requests.Session()
        # TODO: print gracefully warning message.
        session.verify = False

        r = session.get(week_url, headers=headers)
        if r is None:
            return None

        if r.status_code != 200:
            return None

        subtasks = r.json()['issue']['children']
        if len(subtasks) == 0:
            return None

        return subtasks[-1]['id']

    def run(self):
        # TODO: Get api_key from .api_key
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)

        # Read issue number from config.py
        wissue = get_current_redmine_week_report_issue()
        if wissue is None:
            return True

        issue = self._get_latest_subtask_issue(wissue, url, key)
        if issue is None:
            return True

        if ri.help_confirm_issue_number(issue) != 'y':
            return True

        if ri.help_ask_yes_or_no(
                "Do you wanna use preview of issue?(y/N) ",
                default_yes=False) is True:
            pnum, wname = get_current_redmine_preview()
            # PREVIEW_WIKI_NAME, PREVIEW_PROJ_NUM
            # should be imported without errors.
            # These variables are used for the access temporary wiki page
            # as a preview.
            if pnum is None or wname is None:
                print("No set PREVIEW_WIKI_NAME, PREVIEW_PROJ_NUM")
                return None

            url_path = 'redmine.piolink.com/projects/{}/wiki/{}'.format(
                    pnum, wname)

            url_addr = 'https://' + parse.quote(url_path)

            webbrowser.open_new(url_addr)

            # NamedTemporaryFile instance should have "delete" flag False.
            # Because "help_user_input" uses the "delete" mode temp file.
            tfile = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)

            t = Thread(target=self._preview_checker, args=(tfile.name, ri))
            t.start()

            # Load issue's description and open an interactive editor.
            desc = ri.help_get_description(issue)
            cnt = ri.help_user_input(desc.encode(), _temp=tfile)

            # Removing the tempfile triggers to exit the thread.
            os.unlink(tfile.name)
            t.join()

            ret = ri.help_ask_yes_or_no("Are you sure?(y/N) ", default_yes=False)
            if not ret:
                return True

            # Show what you've edited.
            print(cnt)
            ri.help_update_description(issue, cnt)
            return True

        else:
            try:
                ri.help_edit_description(issue)
            except:
                print("Edit description Fail")
                return True
        return True


class EditField(Command):
    ''' Edit Field Command. '''
    name = "edit_field"
    DESC = "Edit Field of Issue"

    def run(self):
        _, url, key = get_current_redmine()
        ri = RedmineHelper(url=url, key=key)
        issue = ri.help_ask_issue_number()
        if issue is None:
            return True

        return self.edit_field(ri, issue)

    def edit_field(self, ri, issue):
        def _get_value(line):
            start_index = line.find('[')
            end_index = line.rfind(']')
            if start_index == -1 or end_index == -1:
                raise InputError("There is no square brackets")
            else:
                return line[start_index+1:end_index]

        # First
        issue_res = ri.help_get_issue_instance(issue)
        help_messages = []
        kwargs = {
            'project_id': self.get_project(help_messages, ri, issue_res),
            'subject': self.get_subject(help_messages, issue_res),
        }
        answer = ri.help_user_input('\n'.join(help_messages).encode())
        for line in answer.split('\n'):
            try:
                line = line.strip()
                if line.startswith('> Project') is True:
                    kwargs['project_id'] = int(_get_value(line))
                elif line.startswith('> Subject') is True:
                    kwargs['subject'] = _get_value(line)
            except:
                continue
        ret = ri.help_update_field(issue_res.id, **kwargs)
        if ret is False:
            return False

        # Second
        issue_res = ri.help_get_issue_instance(issue)
        help_messages = []
        kwargs = {
            'assigned_to_id': int(self.get_user(help_messages, ri, issue_res)),
            'tracker_id': int(self.get_tracker(help_messages, ri, issue_res)),
        }
        self.get_start_date(help_messages, issue_res)
        self.get_due_date(help_messages, issue_res)
        answer = ri.help_user_input('\n'.join(help_messages).encode())
        for line in answer.split('\n'):
            try:
                line = line.strip()
                if line.startswith('> User') is True:
                    assign = _get_value(line)
                    if assign:
                        kwargs['assigned_to_id'] = int(_get_value(line))
                    else:
                        continue
                elif line.startswith('> Tracker') is True:
                    kwargs['tracker_id'] = int(_get_value(line))
                elif line.startswith('> Start Date') is True:
                    time_value = time.strptime(_get_value(line).strip(), "%Y/%m/%d")
                    kwargs['start_date'] = datetime.date(
                        time_value.tm_year, time_value.tm_mon, time_value.tm_mday)
                elif line.startswith('> Due Date') is True:
                    time_value = time.strptime(_get_value(line).strip(), "%Y/%m/%d")
                    kwargs['due_date'] = datetime.date(
                        time_value.tm_year, time_value.tm_mon, time_value.tm_mday)
            except:
                print("hmmm")
                continue
        ret = ri.help_update_field(issue_res.id, **kwargs)
        if ret is False:
            return False
        return True

    def get_project(self, help_messages, ri, issue_res):
        help_messages += ListProject.get_project_lines(ri)
        help_messages.append('> Project: [{}]'.format(issue_res.project.id))
        help_messages.append('')
        return issue_res.project.id

    def get_subject(self, help_messages, issue_res):
        help_messages.append('> Subject: [{}]'.format(issue_res.subject))
        help_messages.append('')
        return issue_res.subject

    def get_user(self, help_messages, ri, issue_res):
        help_messages += ListAssignUser.get_user_lines(ri)
        default_user_id = getattr(issue_res, "assigned_to", issue_res.author).id
        help_messages.append('> User: [{}]'.format(default_user_id))
        help_messages.append('')
        return default_user_id
    
    def get_tracker(self, help_messages, ri, issue_res):
        help_messages += ListTracker.get_tracker_lines(ri)
        # TODO: Some projects may not support these tracker IDs. Be careful!
        help_messages.append('> Tracker: [{}]'.format(issue_res.tracker.id))
        help_messages.append('')
        return issue_res.tracker.id

    def get_start_date(self, help_messages, issue_res):
        empty_date = "! Current {} date is empty. Fill or leave it."
        default_start_date = getattr(issue_res, "start_date", None)
        if default_start_date is None:
            default_start_date = datetime.date.today()
            help_messages.append(empty_date.format('start'))
        help_messages.append('> Start Date: [{}]'.format(default_start_date.strftime("%Y/%m/%d")))
        help_messages.append('')
        return default_start_date
    
    def get_due_date(self, help_messages, issue_res):
        empty_date = "! Current {} date is empty. Fill or leave it."
        default_due_date = getattr(issue_res, "due_date", None)
        if default_due_date is None:
            default_due_date = datetime.date.today()
            help_messages.append(empty_date.format('due'))
        help_messages.append('> Due Date: [{}]'.format(default_due_date.strftime("%Y/%m/%d")))
        help_messages.append('')
        return default_due_date
