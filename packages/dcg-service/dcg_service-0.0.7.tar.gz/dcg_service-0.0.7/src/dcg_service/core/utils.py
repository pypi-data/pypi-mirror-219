import json
import traceback
from datetime import datetime
from flask import request


class UserObject:
    """
    Custom user class
    Helps to convert dict to class object instance.
    """

    is_authenticated = False
    is_staff = False
    is_superuser = False
    is_agent = False
    permissions = list()

    def __init__(self, dict1):
        self.__dict__.update(dict1)


def get_user_obj(data):
    """
    using 'json.loads' method and passing 'json.dumps'
    method and custom object hook as arguments
    """
    if not isinstance(data, dict):
        raise TypeError("get_user_obj 'data' argument must be a dict.")
    return json.loads(json.dumps(data), object_hook=UserObject)


def save_error_es_db():
    from . import EsClient
    just_the_string = traceback.format_exc()

    body = {
        "Path": request.path,
        "Method": request.method,
        "Entity": "orders",
        "Data": str(just_the_string),
        "StatusCode": 500,
        "Timestamp": datetime.now()
    }
    EsClient.index(index='error_logs', body=body)
    return True
