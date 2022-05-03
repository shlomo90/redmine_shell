""" Redmint switch. """


from pathlib import Path
from redmine_shell.shell.singleton import SingletonInstane
import json


class LoginError(BaseException):
    pass


class Login(SingletonInstane):
    ''' Redmine Login. '''
    def __init__(self):
        self.index = 0
        self.login = None
        self.data = None
        self.load_rc()

    def load_rc(self):
        try:
            home_dir = str(Path.home())
        except RuntimeError:
            raise LoginError("Couldn't find Home directory.")

        rc_path = "/".join([home_dir, ".redmine_shell_rc"])

        try:
            with open(rc_path, "r") as rcfile:
                rc = json.load(rcfile)
        except IOError:
            raise LoginError("No redmine_shell_rc file.")
        except FileNotFoundError:
            raise LoginError("No redmine_shell_rc file.")
        except json.decoder.JSONDecodeError as e:
            raise LoginError("Decoding redmine_shell_rc file Error: {}".format(
                e))

        if not rc:
            raise LoginError("No data in redmine_shell_rc file.")

        data = []
        for name, value in rc.items():
            if value.get("URL", None) is None:
                raise LoginError("URL is mandatory.")
            if value.get("KEY", None) is None:
                raise LoginError("KEY is mandatory.")

            login = {}
            login['NAME'] = name
            login['URL'] = value.get('URL')
            login['KEY'] = value.get('KEY')
            login['PREVIEW_PROJ_NUM'] = value.get('PREVIEW_PROJ_NUM')
            login['PREVIEW_WIKI_NAME'] = value.get('PREVIEW_WIKI_NAME')
            login['WEEK_REPORT_ISSUE'] = value.get('WEEK_REPORT_ISSUE')
            login['USE_TEMPLATE'] = value.get('USE_TEMPLATE', False)
            data.append(login)

        self.data = data

    def iterate_login(self):
        for login in self.data:
            yield login

    def next(self):
        ''' Get next login info. '''

        self.index = (self.index + 1) % len(self.data)
        config = self.login = self.data[self.index]
        return config['NAME'], config['URL'], config['KEY']

    def current(self):
        ''' Get current login info. '''
        if self.login is None:
            config = self.data[self.index]
            self.login = config
        else:
            config = self.login

        return config['NAME'], config['URL'], config['KEY']

    def current_config(self):
        ''' Get current login info. '''
        if self.login is None:
            config = self.data[self.index]
            self.login = config
        else:
            config = self.login
        return config

    def current_preview(self):
        ''' Get preview setting info. '''

        if self.login is None:
            config = self.data[self.index]
            self.login = config
        else:
            config = self.login

        return (
            config.get('USE_PREVIEW', False),
            config['PREVIEW_PROJ_NUM'],
            config['PREVIEW_WIKI_NAME'])

    def current_week_report_issue(self):
        ''' Get Week Report Issue. '''

        if self.login is None:
            config = self.data[self.index]
            self.login = config
        else:
            config = self.login

        return config['WEEK_REPORT_ISSUE']


def get_login():
    ''' Get login instance. '''
    return Login.instance()


def get_current_redmine():
    ''' Get current redmine login information. '''

    login = Login.instance()
    return login.current()


def get_current_redmine_preview():
    ''' Get current redmine preview setting information. '''

    login = Login.instance()
    return login.current_preview()

def get_current_redmine_week_report_issue():
    ''' Get current redmine week report issue information. '''

    login = Login.instance()
    return login.current_week_report_issue()


def get_next_redmine():
    ''' Get next redmine login information. '''
    login = Login.instance()
    return login.next()


def get_current_redmine_config():
    ''' Get current redmine config. '''

    login = Login.instance()
    return login.current_config()
