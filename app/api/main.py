from flask import request
from flask_apispec import MethodResource, marshal_with, doc
from marshmallow import ValidationError

from app import docs, db
from . import api
from .errors import EntityNotFound
from .schemas import ConsultationSchema
from ..models import Consultation


@doc(tags=["consultation"])
class ConsultationResource(MethodResource):

    @doc(summary="get consultation")
    @marshal_with(ConsultationSchema, code=200)
    def get(self, consultation_id):
        consultation = Consultation.query.get(consultation_id)
        if consultation is None:
            raise EntityNotFound()
        return Consultation.query.get(consultation_id)

    @doc(summary="edit whole consultation")
    def put(self, consultation_id):
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

    @doc(summary="edit some fields in consultation")
    def patch(self, consultation_id):
        consultation = Consultation.query.get(consultation_id)
        if consultation is None:
            raise EntityNotFound()
        update_kwargs = ConsultationSchema().load(request.get_json(), partial=True)
        for key, value in update_kwargs.items():
            setattr(consultation, key, value)
        db.session.commit()
        return {"status": "ok"}

    @doc(summary="delete consultation")
    def delete(self, consultation_id):
        consultation = Consultation.query.get(consultation_id)
        if consultation is None:
            raise EntityNotFound()
        db.session.delete(consultation)
        db.session.commit()
        return {"status": "ok"}


@doc(tags=["consultation list"])
class ConsultationListResource(MethodResource):

    @doc(summary="get consultation list")
    @marshal_with(ConsultationSchema(many=True), code=200)
    def get(self):
        consultations = Consultation.query.all()
        return consultations

    @doc(summary="add consultation")
    @marshal_with(ConsultationSchema, code=200)
    def post(self):
        consultation = ConsultationSchema(load_instance=True).load(request.get_json())
        db.session.add(consultation)
        db.session.commit()
        return consultation


def register_apis():
    api.add_resource(ConsultationResource, "/consultations/<int:consultation_id>",
                     endpoint="consultation")
    docs.register(ConsultationResource, endpoint="consultation", blueprint="api")

    api.add_resource(ConsultationListResource, "/consultations",
                     endpoint="consultation_list")
    docs.register(ConsultationListResource, endpoint="consultation_list", blueprint="api")
