# app/schemas/appointment_schema.py
from app.extensions import ma
from app.models import Appointment
from marshmallow import fields, validates, ValidationError
from datetime import datetime

class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        load_instance = True
        include_fk = True # Inclure patient_id

    # Champs en lecture seule
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # Validation personnalisée
    appointment_date = fields.DateTime(required=True, error_messages={"required": "La date du rendez-vous est requise."})
    patient_id = fields.Int(required=True, error_messages={"required": "L'ID du patient est requis."})
    notes = fields.Str(allow_none=True)
    status = fields.Str(load_default='Scheduled')
    type = fields.Str(load_default='Consultation')

    # Exemple de validation métier : Pas de RDV dans le passé (optionnel)
    # @validates('appointment_date')
    # def validate_date(self, value):
    #     if value < datetime.now():
    #         raise ValidationError("La date du rendez-vous ne peut pas être dans le passé.")

# Instances
appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)