""" Redmint switch. """


from redmine_shell.shell.config import LOGIN


class SingletonInstane():
    ''' Singleton Base class. '''
    __instance = None

    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        ''' Get instance of singleton. '''
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__get_instance
        return cls.__instance


class Login(SingletonInstane):
    ''' Redmine Login. '''
    def __init__(self):
        self.index = 0
        self.login = None

    def next(self):
        ''' Get next login info. '''

        self.index = (self.index + 1) % len(LOGIN)
        config = self.login = LOGIN[self.index]
        return config['NAME'], config['URL'], config['KEY']

    def current(self):
        ''' Get current login info. '''
        if self.login is None:
            config = LOGIN[self.index]
            self.login = config
        else:
            config = self.login

        return config['NAME'], config['URL'], config['KEY']

    def current_preview(self):
        ''' Get preview setting info. '''

        if self.login is None:
            config = LOGIN[self.index]
            self.login = config
        else:
            config = self.login

        return config['PREVIEW_PROJ_NUM'], config['PREVIEW_WIKI_NAME']


def get_current_redmine():
    ''' Get current redmine login information. '''

    login = Login.instance()
    return login.current()


def get_current_redmine_preview():
    ''' Get current redmine preview setting information. '''

    login = Login.instance()
    return login.current_preview()


def get_next_redmine():
    ''' Get next redmine login information. '''
    login = Login.instance()
    return login.next()
