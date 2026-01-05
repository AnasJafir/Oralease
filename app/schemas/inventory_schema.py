# app/schemas/inventory_schema.py
from app.extensions import ma
from app.models import InventoryItem
from marshmallow import fields, validates, ValidationError

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InventoryItem
        load_instance = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, error_messages={"required": "Le nom de l'article est requis."})
    quantity = fields.Int(required=True, error_messages={"required": "La quantité est requise."})
    threshold = fields.Int(missing=25) # Valeur par défaut si non fournie
    unit = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    sell_price = fields.Float(allow_none=True)

    @validates('quantity')
    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("La quantité ne peut pas être négative.")

# Instances
inventory_item_schema = InventorySchema()
inventory_items_schema = InventorySchema(many=True)