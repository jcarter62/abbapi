from flask import request
from appsettings import Settings
import requests


class Login:

    #
    # These are the published data items of this class
    #
    result: str
    message: str
    token: str

    def __init__(self, username='', password='', key='') -> None:
        self.username = username
        self._password_ = password
        self._key_ = key
        self.result = 'fail'
        self.message = ''
        self.token = ''
        if self.check_key():
            self.execute()
        return

    def execute(self):
        self.message = ''
        self.result = 'fail'
        self.token = ''
        settings = Settings()
        url = settings.auth_api + '/login'
        formdata = {'username': self.username, 'password': self._password_}
        try:
            data = requests.post(url, data=formdata)
            if data.status_code == 200:
                data = data.json()
                self.token = data['token']
                self.message = ''
                self.result = 'success'
        except requests.exceptions.RequestException as e:
            self.message = e.__str__()
        return

    def check_key(self):
        result = False
        try:
            if self._key_ == Settings().key:
                result = True
            else:
                self.message = 'key invalid'
        except Exception as e:
            # key not found, so we did not pass
            self.message = e.__str__()
        return result
