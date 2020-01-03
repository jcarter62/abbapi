import json
import os


class Settings:

    def __str__(self) -> str:
        nl = '\n'
        s = 'server:' + self.server + nl + \
            'db:' + self.db + nl
        return s

    def __init__(self) -> None:
        self.server = ''
        self.db = ''

        self.load_config()
        super().__init__()

    def config_filename(self) -> str:
        appname = 'abbapi'
        osname = os.name
        if osname == 'nt':
            _data_folder = os.path.join(os.getenv('APPDATA'), appname)
        else:
            _data_folder = os.path.join(os.getenv('HOME'), '.' + appname)

        if not os.path.exists(_data_folder):
            os.makedirs(_data_folder)

        filename = os.path.join(_data_folder, 'settings.json')
        return filename

    def initial_settings(self) -> object:
        result = {
            "sqlserver": "sql-svr\\mssqlr2",
            "database": "wmis_ibm",
        }
        return result

    def load_config(self):
        filename = self.config_filename()

        try:
            with open(filename, 'r') as f:
                sobj = json.load(f)
        except Exception  as e:
            sobj = self.initial_settings()
            self.save_config(sobj)

        self.server = sobj['sqlserver']
        self.db = sobj['database']
        return

    def save_config(self, obj):
        filename = self.config_filename()
        with open(filename, 'w') as output:
            json.dump(obj, output)
        return

    def user_input(self, msg, def_val) -> str:
        result = def_val
        s = '%s (%s):' % (msg, def_val)
        inp = input(s)
        if inp != '':
            result = inp
        return result

    def user_update(self):
        print('')
        i_server = self.user_input('SQL Server', self.server)
        i_db = self.user_input('Database', self.db)
        obj = {
            "sqlserver": i_server,
            "database": i_db,
        }
        self.save_config(obj=obj)

    def settings(self) -> object:
        result = {
            "sqlserver": self.server,
            "database": self.db
        }
        return result
