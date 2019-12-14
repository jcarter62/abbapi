import logging
import os
import arrow
from flask import request

class LogDir:

    def __init__(self, app_name='log'):
        import os
        # app_name = 'log'
        osname = os.name
        if osname == 'nt':
            _log_folder = os.path.join(os.getenv('APPDATA'), 'log', app_name)
        else:
            _log_folder = os.path.join(os.getenv('HOME'), '.log', app_name)

        os.makedirs(_log_folder, exist_ok=True)

        self.log_folder = _log_folder
        return

class LogFile:

    def get_time_stamp_string(self):
        now = arrow.now()
        fn = now.format('YYYYMMDD')
        return fn

    def __init__(self, appname=''):
        if appname == '':
            self.appname = 'app'
        else:
            self.appname = appname

        self.filename = self.appname + '-' + self.get_time_stamp_string() + '.txt'
        log_dir = LogDir(appname).log_folder
        self.full_path = os.path.join(log_dir, self.filename)
        return


class AppLogging:

    def __init__(self, appname='log', app=None):
        self.app = app
        self.appname = appname
        self.logfile = LogFile(appname=self.appname)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.log_file_handler = logging.FileHandler(filename=self.logfile.full_path)
        self.logger.addHandler(self.log_file_handler)

    def log_message(self, msg='', req=None):
        now_string = arrow.now().format("YYYY/MM/DD-HH:mm:ss")
        obj = {
            'stamp': now_string,
            'url': req.path,
            'ip': req.remote_addr,
            'agent': req.user_agent,
        }

        new_file = LogFile(appname=self.app).full_path
        current_file = self.app.logger.handlers[0].baseFilename
        if current_file != new_file:
            handler = self.app.logger.handlers[0]
            self.app.logger.removeHandler(hdlr=handler)
            handler = logging.FileHandler(filename=new_file)
            self.app.logger.addHandler(handler)

        self.logger.info('%(ip)s %(stamp)s %(url)s %(agent)s' % obj)

        return

