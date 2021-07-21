''' Issue Commands. '''


import os
import time
import tempfile
import requests
import webbrowser

from redmine_shell.shell.config import DEBUG, DEFAULT_EDITOR
from redmine_shell.shell.switch import (
    get_current_redmine, get_current_redmine_preview)
from redmine_shell.shell.command import Command, CommandType
from redmine_shell.shell.helper import RedmineHelper
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
        print("{}: Not Implemented Yet!".format(self.name))
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

        if ri.help_ask_preview_issue() is True:
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

            ret = ri.help_ask_write_issue()
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
