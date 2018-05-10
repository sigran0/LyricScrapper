
import requests
import json


class RequestManager:

    def __init__(self):
        self.default_url = 'http://localhost:3000/api'
        self.target_url = ''
        self.on_target = False

    def reset(self):
        self.target_url = ''
        self.on_target = False

    def set_target_url(self, target):
        self.reset()

        self.on_target = True
        self.target_url = '{}/{}'.format(self.default_url, target)

    def post(self, data):

        if self.on_target is not True:
            raise RuntimeError('set_target_url() must me called before use this method')

        headers = {'Content-Type': 'application/json; charset=utf-8'}
        json_data = json.dumps(data)
        res = requests.post(self.target_url, data=json_data, headers=headers)

        if res.status_code is not 200:
            print(res)
            return False
        return True
