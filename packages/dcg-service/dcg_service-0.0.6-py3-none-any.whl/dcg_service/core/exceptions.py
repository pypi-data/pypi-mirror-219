"""
Contains override Exception class.
"""
from flask import jsonify
from flask_babel import lazy_gettext as _
from . import app, utils
from .logger import logger
from .response import CustomResponse


class APPException(Exception):
    """
    Provide `.status_code` and `.default_detail` properties.
    """
    code = 500
    default_detail = _('An error occurred.')
    error_field = 'error'

    def __init__(self, detail=None, status_code=None):
        self.detail = detail or self.default_detail
        self.messages = [self.detail] if isinstance(self.detail, (str, bytes)) else self.detail
        self.status_code = status_code or self.code
        super(APPException, self).__init__(detail)

    def __str__(self):
        """
        Return exception str error.
        """
        return str(self.detail)

    def get_exception_message(self, args: Exception.args):
        """
        Return Exception messages as dict.
        :param args: `Exception.args`
        :return: dict
        """
        all_exception_detail = dict()
        if isinstance(args, tuple):
            for arg in args:
                if getattr(arg, 'args', None):
                    all_exception_detail.update(self.get_exception_message(arg.args))
                elif isinstance(arg, dict):
                    all_exception_detail.update(arg)
                else:
                    all_exception_detail.update({self.error_field: str(arg)})
        return all_exception_detail

    @property
    def messages_dict(self):
        """
        Return `exceptions` of type Dict.
        """
        exception_detail = self.get_exception_message(self.args)

        return exception_detail

    def as_json(self):
        """
        Return `flask.jsonify` response.
        """
        response = jsonify(self.messages_dict)
        response.status_code = self.status_code
        return response


class AuthException(APPException):
    """
    Token Authentication exception.
    """
    code = 401
    default_detail = _('No authentication credentials were provided.')
    error_field = 'message'


class APIException(APPException):
    """
    API exception.
    """
    code = 400
    default_detail = _('Something went wrong.')
    error_field = 'message'


class NotImplementedException(Exception):
    pass


@app.errorhandler(APPException)
def app_exception_handler(error):
    logger.critical('[ERROR]--{}'.format(str(error)))
    return error.as_json()


@app.errorhandler(Exception)
def all_exception_handler(error):
    utils.save_error_es_db()
    logger.critical('[ERROR]--{}'.format(str(error)))
    response = jsonify({'message': _('Something went wrong')})
    response.status_code = 400
    return response


@app.after_request
def after_request(response):
    if response.content_type == 'application/json':
        return CustomResponse(response).render
    return response
