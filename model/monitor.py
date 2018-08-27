from model.RequestManager import RequestManager
from model.content_hub import ContentHub


class Monitor:
    def __init__(self, username, endpoint='digital-ss', req_status='Not requested', req_status_code='Not requested'):
        self.username = username
        self.req_status = req_status
        self.req_status_code = req_status_code
        self.endpoint = endpoint
        self.hub = ContentHub()
        self.request_manager = RequestManager()
        self.result_list = list()
        self.index = 0

    def get_status(self, req_name, password):
        try:
            parent_to_be_found = self.request_manager.get_parent_response(request_name=req_name)
            paresponse_list = list()
            if parent_to_be_found is not None and parent_to_be_found != 'Forbidden':
                for i in self.hub.responses[parent_to_be_found].values():
                    paresponse_list.append(i)
            elif parent_to_be_found is None:
                paresponse_list = [parent_to_be_found]
            for paresponse in paresponse_list:
                url_list = self.request_manager.get_url(name=req_name, paresponse=paresponse, endpoint=self.endpoint)
                for url in url_list:
                    request_data = self.request_manager.make_request(req_name=req_name,
                                                                     url=url,
                                                                     username=self.username,
                                                                     password=password)
                    self.index += 1
                    self.req_status = request_data['status']
                    self.req_status_code = request_data['status_code']
                    self.result_list.append({"index": self.index, "status": self.req_status, "status_code": self.req_status_code})
                    if self.req_status == "Obtained":
                        if self.hub.responses.get(req_name) is None:
                            self.hub.responses[req_name] = dict()
                            self.hub.responses[req_name][self.index] = request_data['response']
                        else:
                            self.hub.responses[req_name][self.index] = request_data['response']
        except KeyError:
            pass

    def refresh_status(self):
        self.req_status = 'Not requested'
        self.req_status_code = 'Not requested'
        self.result_list = list()
        self.index = 0
