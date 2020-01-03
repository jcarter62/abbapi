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

        # print(self.appname)
        # print(self.get_time_stamp_string())
        self.filename = self.appname + '-' + self.get_time_stamp_string() + '.txt'
        # print(self.filename)
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
        if os.getenv('FLASK_DEBUG') == 1:
            self.log2console = True
        else:
            self.log2console = False

    def log_message(self, msg='', req=None):
        now_string = arrow.now().format("YYYY/MM/DD-HH:mm:ss")
        obj = {
            'stamp': now_string,
            'url': 'X',
            'ip': 'X',
            'agent': 'X',
            'message': msg
        }

        if req != None:
            obj['url'] = req.path
            obj['ip'] = req.remote_addr
            obj['agent'] = req.user_agent


        current_file = None
        try:
            new_file = LogFile(appname=self.appname).full_path
            current_file = self.app.logger.handlers[0].baseFilename
        except Exception as e:
            print('Exception %s' % str(e))

        try:
            if current_file != new_file:
                if self.app.logger.handlers.__len__() > 0:
                    handler = self.app.logger.handlers[0]
                    self.app.logger.removeHandler(hdlr=handler)

                handler = logging.FileHandler(filename=new_file)
                self.app.logger.addHandler(handler)
        except Exception as e:
            print('Exception %s' % str(e))

        fmt = '%(ip)s %(stamp)s %(url)s %(agent)s: %(message)s'
        self.logger.info(fmt % obj)
        if self.log2console:
            print(fmt % obj)

        return

