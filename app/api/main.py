from flask import request, Blueprint
from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
from flask_jwt_extended import jwt_required
from flask_restful import Api
from marshmallow import ValidationError

from app import docs, db
from .auth import auth_bp
from .errors import EntityNotFound
from .errors import handle_error
from .schemas import ConsultationSchema
from ..models import Consultation

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api_bp.register_blueprint(auth_bp)
Api.handle_error = handle_error
api = Api(api_bp, catch_all_404s=True)


@doc(tags=["consultation"],
     params={"consultation_id": {"description": "identification of consultation"}})
class ConsultationResource(MethodResource):
    decorators = [jwt_required()]

    @doc(summary="get consultation")
    @marshal_with(ConsultationSchema, code=200)
    def get(self, consultation_id):
        consultation = Consultation.query.get(consultation_id)
        if consultation is None:
            raise EntityNotFound()
        return Consultation.query.get(consultation_id)

    @doc(summary="edit whole consultation", responses={200: {
        "schema": {'type': 'object', 'properties': {'status': {'type': 'string', 'example': "ok"}}},
        "description": "success status"}})
    @use_kwargs(ConsultationSchema)
    def put(self, consultation_id, **_kwargs):
        consultation = Consultation.query.get(consultation_id)
        if consultation is None:
            raise EntityNotFound()
        schema = ConsultationSchema()
        update_kwargs = schema.load(request.get_json())
        if not all(i in update_kwargs for i in schema.declared_fields):
            raise ValidationError("Not all fields")
        for key, value in update_kwargs.items():
            setattr(consultation, key, value)  # обновляем поля
        db.session.commit()
        return {"status": "ok"}

    @doc(summary="edit some fields in consultation", responses={200: {
        "schema": {'type': 'object', 'properties': {'status': {'type': 'string', 'example': "ok"}}},
        "description": "success status"}})
    def patch(self, consultation_id):
        consultation = Consultation.query.get(consultation_id)
        if consultation is None:
            raise EntityNotFound()
        update_kwargs = ConsultationSchema().load(request.get_json(), partial=True)
        for key, value in update_kwargs.items():
            setattr(consultation, key, value)
        db.session.commit()
        return {"status": "ok"}

    @doc(summary="delete consultation", responses={200: {
        "schema": {'type': 'object', 'properties': {'status': {'type': 'string', 'example': "ok"}}},
        "description": "success status"}})
    def delete(self, consultation_id):
        consultation = Consultation.query.get(consultation_id)
        if consultation is None:
            raise EntityNotFound()
        db.session.delete(consultation)
        db.session.commit()
        return {"status": "ok"}


@doc(tags=["consultation list"])
class ConsultationListResource(MethodResource):
    decorators = [jwt_required()]

    @doc(summary="get consultation list")
    @marshal_with(ConsultationSchema(many=True), code=200)
    def get(self):
        consultations = Consultation.query.all()
        return consultations

    @doc(summary="add consultation")
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
