

class Setup:

    def __init__(self):
        pass

    def clear(self):
        from os import name, getenv, system
        _term = getenv('TERM')
        if getenv('TERM') is None:
            pass
        else:
            if name == 'nt':    # for windows
                _ = system('cls')
            else:   # for mac and linux(here, os.name is 'posix')
                _ = system('clear')

    def user_input(self, msg, def_val) -> str:
        result = def_val
        s = '%s (%s):' % (msg, def_val)
        inp = input(s)
        if inp != '':
            result = inp
        return result

    def execute(self):
        from .settings import Settings
        self.clear()
        settings = Settings()

        settings.mongo_host = self.user_input(msg='Please provide Mongo DB Host Address', def_val=settings.mongo_host)
        settings.mongo_port = self.user_input(msg='Please provide Mongo DB Port', def_val=settings.mongo_port)
        settings.sqlserver = self.user_input(msg='SQL Server Name', def_val=settings.sqlserver)
        settings.sqldb = self.user_input(msg='SQL Server Database', def_val=settings.sqldb)
        settings.datafile = self.user_input(msg='Sites datafile', def_val=settings.datafile)
        settings.key = self.user_input(msg='key', def_val=settings.key)
        settings.auth_api = self.user_input(msg='Auth API Url', def_val=settings.auth_api)

        if self.user_input(msg='Update config file ? ', def_val='yes') == 'yes':
            settings.save_config()

        print(str(settings))
