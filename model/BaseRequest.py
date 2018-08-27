import requests


class BaseRequest:
    def __init__(self, tokenType, accessToken, url):
        self.status = 'Not requested'
        self.response = []
        self.status_code = int()
        self.url = url
        self.header = {
            'Authorization': tokenType + ' ' + accessToken,
            'Content-Type': 'application/json',
            'X-EE-EL-Tracking-Header': '00D2E510-0749-40D6-A805-7A598448988F',
            'X-EE-API-Originator': 'MyEE'}
        self.request = requests.get(url=self.url, headers=self.header)
        if self.request.status_code == 200:
            self.response = self.request.json()
            self.status = 'Obtained'
            self.status_code = self.request.status_code
        else:
            self.status = "Failed"
            self.response = []
            self.status_code = self.request.status_code


