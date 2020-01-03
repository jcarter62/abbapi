class Settings:

    def __init__(self, appname='abbapi'):
        self.appname = appname
        self.mongo_host = ''
        self.mongo_port = 0
        self.sqlserver = ''
        self.sqldb = ''
        self.load_config()

    def __str__(self):
        nl = '\n'
        s = 'host:' + self.mongo_host + nl + \
            'mongo_port:' + str(self.mongo_port) + nl + \
            'sqlserver:' + self.sqlserver + nl + \
            'sqldb:' + self.sqldb + nl + \
            'config file:' + self.config_filename()
        return s

    def config_filename(self):
        import os
        osname = os.name
        if osname == 'nt':
            _data_folder = os.path.join(os.getenv('APPDATA'), self.appname)
        else:
            _data_folder = os.path.join(os.getenv('HOME'), self.appname)

        if not os.path.exists(_data_folder):
            os.makedirs(_data_folder)

        filename = os.path.join(_data_folder, 'settings.json')
        return filename

    def load_config(self):
        import json
        filename = self.config_filename()
        try:
            with open(filename, 'r') as f:
                db_obj = json.load(f)
        except Exception as e:
            # Assume, we do not have a file, create a default object.
            db_obj = {
                "mongo_host": "localhost",
                "mongo_port": 27017,
                "sqlserver": "sql-svr\\mssqlr2",
                "sqldb": "wmis_ibm"
            }

        self.mongo_host = db_obj['mongo_host']
        self.mongo_port = db_obj['mongo_port']
        self.sqlserver = db_obj['sqlserver']
        self.sqldb = db_obj['sqldb']
        return

    def save_config(self):
        import json
        obj = {
            "mongo_host": self.mongo_host ,
            "mongo_port": self.mongo_port,
            "sqlserver": self.sqlserver,
            "sqldb": self.sqldb
        }

        filename = self.config_filename()
        with open(filename, 'w') as outfile:
            json.dump(obj, outfile)


