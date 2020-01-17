from appsettings import Settings
import requests

class UserInfo:

    email: str
    message: str
    name: str
    token: str
    username: str

    def __init__(self, token=''):
        self.email = ''
        self.message = ''
        self.name = ''
        self.token = token
        self.username = ''

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
        except requests.exceptions.RequestException as e:
            self.message = e.__str__()
        return
