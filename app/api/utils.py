from functools import wraps

from flask_restful import abort
from flask_jwt_extended import current_user


def permissions_accepted(*perms: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            for perm in perms:
                if current_user.can(perm):
                    return fn(*args, **kwargs)
            abort(403, description="You have no access to perform this operation.")

        return decorated_view

    return wrapper
