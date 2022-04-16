from flask import Blueprint
from flask_restful import Api

from .errors import handle_error


api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
Api.handle_error = handle_error
api = Api(api_bp, catch_all_404s=True)