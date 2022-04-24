from flask import request, Blueprint
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Api, abort
from marshmallow import ValidationError

from app import docs, db
from .auth import auth_bp, auth_params
from .errors import EntityNotFound
from .errors import handle_error
from .schemas import ConsultationSchema
from .utils import permissions_accepted
from ..models import Consultation, Permissions

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api_bp.register_blueprint(auth_bp)
Api.handle_error = handle_error
api = Api(api_bp)


@doc(tags=["consultation"],
     params={"consultation_id": {"description": "identification of consultation"}})
class ConsultationResource(MethodResource):
    decorators = [jwt_required()]

    @doc(summary="get consultation", params=auth_params)
    @marshal_with(ConsultationSchema, code=200)
    def get(self, consultation_id):
        consultation: Consultation = Consultation.query.get(consultation_id)
        if consultation is None:
            raise EntityNotFound()
        can_access = consultation.is_accessible_by(current_user)
        if not can_access:
            abort(403, description="You can not access that consultation")
        return consultation

    @doc(summary="edit whole consultation", responses={200: {
        "schema": {'type': 'object', 'properties': {'status': {'type': 'string', 'example': "ok"}}},
        "description": "success status"}}, params=auth_params)
    @use_kwargs(ConsultationSchema)
    def put(self, consultation_id, **_kwargs):
        consultation = Consultation.query.get(consultation_id)
        if consultation is None:
            raise EntityNotFound()
        can_access = consultation.is_accessible_by(current_user)
        if not can_access:
            abort(403, description="You can not access that consultation")
        schema = ConsultationSchema()
        update_kwargs = schema.load(request.get_json())
        update_kwargs["id"] = consultation_id  # user can't edit id of entity
        missing_fields = {}
        for i in schema.declared_fields:
            if i not in update_kwargs:
                missing_fields[i] = ["field is missing"]
        if missing_fields:
            raise ValidationError(missing_fields)
        for key, value in update_kwargs.items():
            setattr(consultation, key, value)  # обновляем поля
        db.session.commit()
        return {"status": "ok"}

    @doc(summary="edit some fields in consultation", responses={200: {
        "schema": {'type': 'object', 'properties': {'status': {'type': 'string', 'example': "ok"}}},
        "description": "success status"}}, params=auth_params)
    def patch(self, consultation_id):
        consultation = Consultation.query.get(consultation_id)
        if consultation is None:
            raise EntityNotFound()
        can_access = consultation.is_accessible_by(current_user)
        if not can_access:
            abort(403, description="You can not access that consultation")
        update_kwargs = ConsultationSchema().load(request.get_json(), partial=True)
        for key, value in update_kwargs.items():
            setattr(consultation, key, value)
        db.session.commit()
        return {"status": "ok"}

    @doc(summary="delete consultation", responses={200: {
        "schema": {'type': 'object', 'properties': {'status': {'type': 'string', 'example': "ok"}}},
        "description": "success status"}}, params=auth_params)
    def delete(self, consultation_id):
        consultation = Consultation.query.get(consultation_id)
        if consultation is None:
            raise EntityNotFound()
        can_access = consultation.is_accessible_by(current_user)
        if not can_access:
            abort(403, description="You can not access that consultation")
        db.session.delete(consultation)
        db.session.commit()
        return {"status": "ok"}


@doc(tags=["consultation list"])
class ConsultationListResource(MethodResource):
    decorators = [jwt_required()]

    @doc(summary="get consultation list", params=auth_params)
    @marshal_with(ConsultationSchema(many=True), code=200)
    def get(self):
        consultations = Consultation.query
        # TODO: build hybrid method expression
        consultations = filter(lambda x: x.is_accessible_by(current_user), consultations)
        return consultations

    @doc(summary="add consultation", params=auth_params)
    @permissions_accepted(Permissions.MANAGE_CONSULTATIONS)  # TODO: documentation for access
    @use_kwargs(ConsultationSchema)
    @marshal_with(ConsultationSchema, code=200)
    def post(self, **_kwargs):
        consultation = ConsultationSchema(load_instance=True).load(request.get_json())
        db.session.add(consultation)
        db.session.commit()
        return consultation


api.add_resource(ConsultationResource, "/consultations/<int:consultation_id>",
                 endpoint="consultation")

api.add_resource(ConsultationListResource, "/consultations",
                 endpoint="consultation_list")


@api_bp.before_app_first_request
def register_docs():
    docs.register(ConsultationResource, endpoint="consultation", blueprint="api")

    docs.register(ConsultationListResource, endpoint="consultation_list", blueprint="api")
