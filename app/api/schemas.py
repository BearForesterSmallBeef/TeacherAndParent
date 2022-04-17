from app import ma
from ..models import Consultation
from marshmallow import validates_schema, ValidationError, fields


class ConsultationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Consultation
        include_fk = True

    teacher_id = ma.auto_field(required=True)
    date = ma.auto_field(required=True)
    start_time = ma.auto_field(required=True)
    finish_time = ma.auto_field(required=True)

    @validates_schema
    def not_free_consultation_requires_parent(self, data, **_kwargs):
        if not data["status"] and "parent_id" not in data:
            raise ValidationError("Not free consultation requires parent")


class LoginSchema(ma.Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)
