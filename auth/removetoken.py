from appsettings import Settings
import requests


class RemoveToken:

    token: str
    code: int

    def __init__(self, token=''):
        self.token = token
        self.code = 0
        if token == '':
            return
        self.expire_token()
        return

    def expire_token(self):
        settings = Settings()
        url = settings.auth_api + '/expire'
        form_data = {'token': self.token}
        try:
            data = requests.post(url, data=form_data)
            self.code = data.status_code
        except requests.exceptions.RequestException as e:
            self.code = 400
        return

