# app/schemas/treatment_schema.py
from app.extensions import ma
from app.models import TreatmentPlan
from marshmallow import fields, validate

class TreatmentPlanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TreatmentPlan
        load_instance = True
        include_fk = True

    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True, error_messages={"required": "L'ID patient est requis."})
    diagnosis = fields.Str(required=True, validate=validate.Length(min=3))
    treatment_details = fields.Str(required=True)
    status = fields.Str(validate=validate.OneOf(["Pending", "In Progress", "Completed"]))
    created_at = fields.DateTime(dump_only=True)
    
    # Nested patient data for display
    patient = fields.Nested('PatientSchema', only=('first_name', 'last_name'), dump_only=True)

# Instances
treatment_plan_schema = TreatmentPlanSchema()
treatment_plans_schema = TreatmentPlanSchema(many=True)