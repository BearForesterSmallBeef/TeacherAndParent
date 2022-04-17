from flask import Blueprint
from flask_apispec import MethodResource, use_kwargs, marshal_with, doc
from flask_jwt_extended import create_access_token
from flask_restful import Api
from flask_restful import abort
from marshmallow import fields, Schema

from app import docs, jwt
from .schemas import LoginSchema
from ..models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
auth_api = Api(auth_bp)


@doc(tags=["auth"])
class LoginUserResource(MethodResource):

    @use_kwargs(LoginSchema, location="query")
    @marshal_with(Schema.from_dict({"access_token": fields.Str()}), code=201)
    def post(self, login, password):
        from flask_jwt_extended import decode_token
        user = User.query.filter_by(login=login).first()
        if user is not None and user.verify_password(password):
            access_token = create_access_token(user)
            print(decode_token(access_token))
            return {"access_token": access_token}, 201
        abort(401, description="Invalid credentials")


auth_api.add_resource(LoginUserResource, "/login", endpoint="auth_login")


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()


@auth_bp.before_app_first_request
def register_docs():
    docs.register(LoginUserResource, endpoint="auth_login", blueprint="auth")
