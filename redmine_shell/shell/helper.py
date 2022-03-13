""" Redmine Helper file.
"""

import os
import tempfile
import subprocess
import signal
from redmine_shell.shell.config import DEFAULT_EDITOR
from redmine_shell.shell.error import InputError
from redminelib import Redmine, exceptions


class RedmineHelper(Redmine):
    """ RedmineHelper Class.

    RedmineHelper inherits Redmine class of redminlib.
    If you need your customized functions in RedmineHelper, Please Add "help_".
    """

    def __init__(self, url, key=None):
        super(RedmineHelper, self).__init__(url, key=key)
        self.rh_url = url
        self.rh_key = key

    def timeout_handler(self, signum, frame):
        raise TimeoutError("Signal Timeout!")

    def help_redmine(self, func, *args, timeout=None, **kwargs):
        # Connection Timeout 3 seconds.
        if timeout is not None:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(timeout)
            try:
                return func(*args, **kwargs)
            except BaseException:
                signal.alarm(0)
                return None
            finally:
                signal.alarm(0)
        else:
            return func(*args, **kwargs)

    def help_get_issue_subject(self, issue):
        """ Wrapper of get issue's subject. """
        return self.issue.get(issue).subject

    def help_user_input(self, init_content, editor=DEFAULT_EDITOR, _temp=None):
        """ Write the user input message to Temporary File and return.

        Params:
            init_content: First showed messages when it opened.
            editor      : the type of editors.
            _temp       : Use external tempfile object.
                          It should be delete mode.
        """

        if _temp is None:
            tmp_file = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        else:
            if _temp.delete is True:
                raise InputError("Tempfile should be delete mode.")

            tmp_file = _temp
        try:
            # Initialize Tempfile.
            tmp_file.write(init_content)
            tmp_file.truncate()
            tmp_file.flush()

            # Mac OS Issue
            # Vim in Mac OS sometimes doesn't save the file editted until
            # calling "close()" function.
            tmp_file.close()

            # Show the file to user.
            name = tmp_file.name
            if editor == 'code':
                cmd = '{} {} --wait'.format(editor, name)
                proc = subprocess.Popen(cmd, shell=True)
                exit_code = proc.wait()  # wait edit done..
                print('vscode edit done ({})'.format(exit_code))

            else:  # deafult (vi)
                cmd = '{} {}'.format(editor, name)
                os.system(cmd)

            # Read the tempfile
            with open(name, 'r') as f:
                data = f.read()

            return data

        except:
            os.unlink(tmp_file.name)
            return None
        os.unlink(tmp_file.name)
        return None

    def help_get_description(self, issue):
        """ Wrapper of getting issue's description. """
        desc = self.issue.get(issue).description
        return desc

    def help_update_field(self, issue, **kwargs):
        return self.issue.update(issue, **kwargs)

    def help_update_description(self, issue, desc):
        """ Wrapper of updating issue's description. """
        kwargs = {'description': desc}
        return self.help_update_field(issue, **kwargs)

    def help_edit_description(self, issue):
        """ Edit description by using editor. """
        desc = self.help_get_description(issue)
        enc_content = desc.encode()

        cnt = self.help_user_input(enc_content)
        print(cnt)

        ret = self.help_ask_yes_or_no("Are you sure?(y/N)", default_yes=False)
        if not ret:
            return True

        self.help_update_description(issue, cnt)

    @classmethod
    def help_ask_yes_or_no(cls, question, default_yes=True):
        """ Ask users the question. """

        from redmine_shell.shell.input import redmine_input
        try:
            answer = redmine_input(question)
            if answer.lower() == 'y':
                return True
            elif answer.lower() == 'n':
                return False
            else:
                if default_yes is True:
                    return True
                else:
                    return False
        except EOFError:
            print("")
            return False
        except KeyboardInterrupt:
            print("")
            return False

    def help_ask_issue_number(self):
        """ Interactively get issue number from user. """
        from redmine_shell.shell.input import redmine_input

        while True:
            try:
                # TODO: try except EOF Error..
                issue = int(redmine_input("Issue number?: ").strip())
            except ValueError:
                print("Input Wrong Number")
                return None
            except EOFError:
                print("")
                return None
            except KeyboardInterrupt:
                print("")
                return None

            answer = self.help_confirm_issue_number(issue)
            if answer == 'y':
                break

        return issue

    def help_confirm_issue_number(self, issue):
        ''' Confirm the issue's subject is correct.
        '''

        from redmine_shell.shell.input import redmine_input

        try:
            tmp_issue_ins = self.issue.get(issue)
        except exceptions.ResourceNotFoundError:
            print("Invalid issue number: out of range.")
            return None

        answer = redmine_input(
            "[#{} {}] -> (y/n)".format(
                tmp_issue_ins.id, tmp_issue_ins.subject))
        return answer

    @classmethod
    def help_ask_project_number(cls):
        ''' Ask the project number. '''

        from redmine_shell.shell.input import redmine_input
        try:
            pid = int(redmine_input("Project number: "))
        except ValueError:
            print("Error: Plz Input digital number!")
            return None
        except EOFError:
            print("")
            return None
        except KeyboardInterrupt:
            print("")
            return None
        return pid

    @classmethod
    def help_ask_wiki_number(cls):
        ''' Ask target wiki name. '''
        from redmine_shell.shell.input import redmine_input

        try:
            wiki = int(redmine_input("Target Wiki Number (default: 1): "))
        except EOFError:
            print("")
            return None
        except KeyboardInterrupt:
            print("")
            return None
        except ValueError:
            return None

        return wiki

    @classmethod
    def help_ask_wiki_name(cls):
        ''' Ask target wiki name. '''
        from redmine_shell.shell.redmine_input import redmine_input

        try:
            wiki = redmine_input("Target Wiki Name(default:wiki): ")
        except EOFError:
            print("")
            return None
        except KeyboardInterrupt:
            print("")
            return None

        if wiki.strip():
            return wiki
        else:
            return 'Wiki'

    def help_execute(self):
        """ Execute command. """
        raise NotImplementedError("function: help_execute not implemented")

    def help_create_issue(self, pid, description="Fill the description."):
        default_issue = {
            'project_id': pid,
            'subject': "No Subject (created by redmine_shell)",
            'description': description}
            #'tracker_id': bug or manage or ...blah
            #'status_id': solved? new?
        resource = self.issue.create(**default_issue)
        return resource

    def help_get_issue_instance(self, issue):
        return self.issue.get(issue)
