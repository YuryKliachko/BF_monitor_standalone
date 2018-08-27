
class ContentHub():
    def __init__(self):
        self.token_type = 'Not requested'
        self.access_token = 'Not requested'
        self.responses = dict()

    def store_token(self, token_type, access_token):
        self.token_type = token_type
        self.access_token = access_token
