from flask import request
from appsettings import Settings
import requests

class Login:

    result: str

    def __init__(self, username, password, req) -> None:
        self.result = {'result': 'failure', 'message': ''}
        self.username = username
        self.password = password
        self.request = req

    def execute(self):
        result = {'result': 'failure', 'message': ''}
        if self.check_key(self.request):
            username = request.form['username']
            password = request.form['password']
            settings = Settings()
            url = settings.auth_api + '/login'
            formdata = {'username': username, 'password': password}
            try:
                data = requests.post(url, data=formdata)
                if data.status_code == 200:
                    data = data.json()
                    token = data['token']
                    result['token'] = token
                    result['result'] = 'success'
            except requests.exceptions.RequestException as e:
                result['message'] = e.__str__()
        return result

    def check_key(self, req : request):
        r = req
        result = False
        try:
            key = r.form['key']
            if key == Settings().key:
                result = True
        except KeyError:
            # key not found, so we did not pass
            result = False

        return result

