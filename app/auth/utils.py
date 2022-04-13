from functools import wraps

from flask import abort
from flask_login import current_user


def roles_required(*roles: str):
    # https://github.com/
    # Flask-Middleware/flask-security/blob/master/flask_security/decorators.py#L462
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            for role in roles:
                if not current_user.has_role(role):
                    abort(403)
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def roles_accepted(*roles: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            for role in roles:
                if current_user.has_role(role):
                    return fn(*args, **kwargs)
            abort(403)

        return decorated_view

    return wrapper


def permissions_required(*perms: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            for perm in perms:
                if not current_user.can(perm):
                    abort(403)
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def permissions_accepted(*perms: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            for perm in perms:
                if current_user.can(perm):
                    return fn(*args, **kwargs)
            abort(403)

        return decorated_view

    return wrapper
