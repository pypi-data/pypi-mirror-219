from functools import wraps
from flask import request, jsonify
from flask_babel import lazy_gettext as _
from .authentication import get_authorization_header, authenticate
from .encryption import decrypt
from .exceptions import AuthException, APPException


def is_authenticated(func):
    """
    Decorator for authenticate request,
    If token is authenticated user details added into "request.user".
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        headers = request.headers
        token = get_authorization_header(headers)
        if token:
            try:
                user = authenticate(token)
                setattr(request, 'user', user)
            except AuthException as error:
                return error.as_json()
        else:
            return AuthException().as_json()
        return func(*args, **kwargs)

    return wrapper


def is_agent(func):
    """
    Decorator for authenticate agent,
    If token is authenticated agent set to True into "request.user.is_agent".
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not bool(getattr(request, 'user', None) and getattr(request.user, 'is_agent', None)):
            return jsonify({"message": _("Permission denied.")}), 401
        return func(*args, **kwargs)

    return wrapper


def admin_authenticated(token):
    response = {"is_admin": False, "error": None}
    try:
        try:
            token = decrypt(token)
        except APPException:
            response['error'] = "Invalid Token."
            return response
        token = "Bearer %s" % token
        user, permissions = authenticate(token)
        if user.user_type == "ADMIN":
            response['is_admin'] = True
    except Exception as error:
        response['error'] = str(error)
    return response
