from appsettings import Settings
import requests

class UserInfo:

    email: str
    message: str
    name: str
    token: str
    username: str
    code: int

    def __init__(self, token=''):
        self.email = ''
        self.message = ''
        self.name = ''
        self.token = token
        self.username = ''
        self.code = 0

        self.details()
        return

    def details(self):
        if self.token == '':
            return
        settings = Settings()
        url = settings.auth_api + '/token_details'
        form_data = {'token': self.token}
        try:
            data = requests.post(url, data=form_data)
            if data.status_code == 200:
                data = data.json()
                self.email = data['email']
                self.message = ''
                self.name = data['name']
                self.username = data['username']
                self.code = 200
            else:
                self.token = ''
                self.message = 'Return Code %s' % str(data.status_code)
                self.code = data.status_code
        except requests.exceptions.RequestException as e:
            self.message = e.__str__()
            self.code = 400
        return
