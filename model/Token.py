import requests
import datetime


class Token:
    def __init__(self):
        self.token_status = 'Not requested'
        self.token_status_code = int()
        self.access_token = str()
        self.token_type = str()

