from model.BaseRequest import BaseRequest
import requests
from model.Token import Token


class RequestManager:
    def __init__(self):
        self.requests_dict = {
            'self': {'paresponse': None,
                     'user_type': ['PAYM', 'PAYG']},
            'billing-accounts': {'paresponse': 'self',
                                 'user_type': ['PAYM', 'PAYG']},
            'mobile-subscriptions': {'paresponse': 'billing-accounts',
                                     'user_type': ['PAYM', 'PAYG']},
            'allowances-prepay': {'paresponse': 'mobile-subscriptions',
                                  'user_type': ['PAYG']},
            'packs': {'paresponse': 'mobile-subscriptions',
                                    'user_type': ['PAYG']},
            'add-ons': {'paresponse': 'mobile-subscriptions',
                        'user_type': ['PAYG', 'PAYM']},
            'add-ons-available': {'paresponse': 'mobile-subscriptions',
                                  'user_type': ['PAYG', 'PAYM']},
            'prepay-credit': {'paresponse': 'mobile-subscriptions',
                              'user_type': ['PAYG']},
            'rollover': {'paresponse': 'mobile-subscriptions',
                         'user_type': ['PAYG']},
            'loyalty-stamps': {'paresponse': 'mobile-subscriptions',
                               'user_type': ['PAYG']},
            'boosts': {'paresponse': 'mobile-subscriptions',
                       'user_type': ['PAYG']},
            'boosts-available': {'paresponse': 'mobile-subscriptions',
                                 'user_type': ['PAYG']},
            'packs-available': {'paresponse': 'mobile-subscriptions',
                                'user_type': ['PAYG']},
            'prepay-usage-items': {'paresponse': 'mobile-subscriptions',
                                   'user_type': ['PAYG']},
            'topups': {'paresponse': 'mobile-subscriptions',
                       'user_type': ['PAYG']},
            'allowances-postpay': {'paresponse': 'mobile-subscriptions',
                                   'user_type': ['PAYM']},
            'contract': {'paresponse': 'mobile-subscriptions',
                                       'user_type': ['PAYM']},
            'content-lock': {'paresponse': 'mobile-subscriptions',
                         'user_type': ['PAYM']},
            'allowances-data': {'paresponse': 'mobile-subscriptions',
                             'user_type': ['PAYM']},
            'data-gifts': {'paresponse': 'mobile-subscriptions',
                             'user_type': ['PAYM']},
            'unbilled-usage': {'paresponse': 'mobile-subscriptions',
                             'user_type': ['PAYM']},
            'outside-allowance-summaries': {'paresponse': 'mobile-subscriptions',
                             'user_type': ['PAYM']},
            'inside-allowance-summaries': {'paresponse': 'mobile-subscriptions',
                                            'user_type': ['PAYM']},
            'allowances-data-show-gifting-data': {'paresponse': 'mobile-subscriptions',
                                           'user_type': ['PAYM']},
            'inlife-recommendations': {'paresponse': 'mobile-subscriptions',
                                                  'user_type': ['PAYM']},
            'upgrade-eligibility': {'paresponse': 'mobile-subscriptions',
                                       'user_type': ['PAYM']},
        }
        self.token = Token()

    def get_parent_response(self, request_name):
        try:
            parent_to_be_found = self.requests_dict[request_name]['paresponse']
            return parent_to_be_found
        except KeyError:
            return 'Forbidden'

    def get_url(self, name, paresponse, endpoint):
        url_list = list()
        if name == "self":
            url_list.append("https://api-test1.ee.co.uk/{}/v1/person-identities/self".format(endpoint))
            return url_list
        elif name == "billing-accounts":
            for billing_account in paresponse[name]:
                links = billing_account.get("links")
                for link in links:
                    if link["rel"] == "self":
                        url_list.append(link["href"])
            return url_list
        elif name == "mobile-subscriptions":
            for mobile_subscription in paresponse["mobile-subscriptions"]:
                links = mobile_subscription.get("links")
                for link in links:
                    if link["rel"] == "self":
                        url_list.append(link["href"])
            return url_list
        else:
            for link in paresponse["links"]:
                if link["rel"] == name:
                    url_list.append(link["href"])
            return url_list

    def get_token(self, username, password):
        token_request = requests.post(
            url="https://api-test1.ee.co.uk/v1/identity/token",
            headers={
                'Authorization': 'Basic eTR3a2ZRR3dOVGluSFFNU0FBVTg0Znd5RzRyYzY2S2o6UEtCakgzbzBuM1l1SGxvMw==',
                'Content-Type': 'application/x-www-form-urlencoded'},
            data='grant_type=password&password=' + password.replace('@', '%40') + '&redirect_uri=token&username=' + username.replace('@', '%40'))
        if token_request.status_code == 200:
            token_response = token_request.json()
            access_token = token_response["access_token"]
            token_type = token_response["token_type"]
            status = 'Obtained'
        else:
            access_token = None
            token_type = None
            status = 'Failed'
        token = {'token_type': token_type,
                 'access_token': access_token,
                 'status': status,
                 'status_code': token_request.status_code}
        return token

    def make_request(self, req_name, username, password, url):
        if req_name == 'self':
            token_data = self.get_token(username, password)
            if token_data['status'] == 'Obtained':
                self.token.access_token = token_data['access_token']
                self.token.token_type = token_data['token_type']
                token_type = self.token.token_type
                access_token = self.token.access_token
            else:
                return {'request_name': 'token',
                        'response': None,
                        'status': 'Failed',
                        'status_code': token_data['status_code']}
        else:
            token_type = self.token.token_type
            access_token = self.token.access_token
        request = BaseRequest(tokenType=token_type, accessToken=access_token, url=url)
        return {'request_name': req_name,
                'response': request.response,
                'status': request.status,
                'status_code': request.status_code}