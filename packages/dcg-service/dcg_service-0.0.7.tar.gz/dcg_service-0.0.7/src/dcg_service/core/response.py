import json
from flask import request
from .exceptions import logger


class CustomResponse(object):
    def __init__(self, response):
        self.response = response

    @property
    def render(self):
        message = None
        data = dict()
        status_code = self.response.status_code
        response_data = json.loads(self.response.data)
        if type(response_data) == dict:
            message = response_data.pop('message', None)
            data = response_data.pop('data', None) if response_data.get('data') else response_data

        if 400 <= status_code <= 499:
            message = response_data.copy() if not message else message
            response_data.clear()

        response_json = {
            "data": data,
            "message": message,
            "title": self.response.status,
            "code": self.response.status_code
        }
        if type(response_data) == dict:
            response_json.update(response_data)

        self.response.data = json.dumps(response_json)
        self.log(response_json)
        return self.response

    def log(self, data):
        if self.response.status_code == 400:
            log = '[{} {} {}]--{}'.format(
                self.response.status_code, request.method,
                request.full_path, data.get('message'))
            logger.error(log)
