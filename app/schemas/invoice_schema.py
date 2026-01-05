from app.extensions import ma
from app.models import Invoice, Quote
from marshmallow import fields, validate

class InvoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Invoice
        load_instance = True
        include_fk = True

    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    treatment_plan_id = fields.Int(allow_none=True)
    total_amount = fields.Float(required=True)
    status = fields.Str(validate=validate.OneOf(["Draft", "Issued", "Paid", "Cancelled"]))
    issue_date = fields.DateTime(dump_only=True)
    due_date = fields.DateTime(allow_none=True)
    items = fields.List(fields.Dict(), required=True) # Check structure later
    patient = fields.Nested('PatientSchema', only=('first_name', 'last_name'), dump_only=True)

class QuoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Quote
        load_instance = True
        include_fk = True

    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    total_amount = fields.Float(required=True)
    status = fields.Str(validate=validate.OneOf(["Draft", "Sent", "Accepted", "Rejected"]))
    created_at = fields.DateTime(dump_only=True)
    items = fields.List(fields.Dict(), required=True)
    patient = fields.Nested('PatientSchema', only=('first_name', 'last_name'), dump_only=True)

invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)
quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)
