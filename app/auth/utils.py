from functools import wraps

from flask import abort
from flask_login import current_user
from flask_principal import Permission, RoleNeed, UserNeed, Identity, ActionNeed

from app import principal
from app.models import Permissions


@principal.identity_loader
def identity_loader():
    if not current_user.is_anonymous:
        identity = Identity(current_user.id)
        return identity


def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role.name))
        for perm in (
                Permissions.MAKE_APPOINTMENT,
                Permissions.EDIT_CONSULTATIONS,
                Permissions.CREATE_PARENTS,
                Permissions.CREATE_TEACHERS,
                Permissions.CREATE_HEAD_TEACHER,
        ):
            if current_user.role.permissions & perm:
                identity.provides.add(ActionNeed(perm))


def roles_required(*roles: str):
    # https://github.com/
    # Flask-Middleware/flask-security/blob/master/flask_security/decorators.py#L462
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perms = [Permission(RoleNeed(role)) for role in roles]
            for perm in perms:
                if not perm.can():
                    abort(403)
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def roles_accepted(*roles: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(RoleNeed(role) for role in roles))
            if perm.can():
                return fn(*args, **kwargs)
            abort(403)

        return decorated_view

    return wrapper


def permissions_required(*perms: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            permissions = [Permission(ActionNeed(perm)) for perm in perms]
            for perm in permissions:
                if not perm.can():
                    abort(403)
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def permissions_accepted(*perms: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perm = Permission(*(ActionNeed(perm) for perm in perms))
            if perm.can():
                return fn(*args, **kwargs)
            abort(403)

        return decorated_view

    return wrapper
