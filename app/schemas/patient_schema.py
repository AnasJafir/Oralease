# app/schemas/patient_schema.py
from app.extensions import ma
from app.models import Patient
from marshmallow import fields, post_load
from app.utils.encryption import decrypt_data, encrypt_data

class PatientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        load_instance = True # Désérialiser directement en objet Patient
        include_fk = True

    # Champs en lecture seule (gérés par le serveur)
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Validation personnalisée
    first_name = fields.Str(required=True, error_messages={"required": "Le prénom est obligatoire."})
    last_name = fields.Str(required=True, error_messages={"required": "Le nom est obligatoire."})
    date_of_birth = fields.Date(required=True)

    # Gestion transparente du chiffrement pour l'API
    # L'API reçoit du texte clair, le schéma s'occupera du reste
    contact_number = fields.Method("get_decrypted_contact", deserialize="encrypt_contact")
    email = fields.Method("get_decrypted_email", deserialize="encrypt_email")
    medical_history = fields.Method("get_decrypted_history", deserialize="encrypt_history")

    def get_decrypted_contact(self, obj):
        return decrypt_data(obj.contact_number) if obj.contact_number else None

    def get_decrypted_email(self, obj):
        return decrypt_data(obj.email) if obj.email else None
    
    def get_decrypted_history(self, obj):
        return decrypt_data(obj.medical_history) if obj.medical_history else None

    # Note: Le chiffrement se fait dans le __init__ du modèle Patient,
    # donc on passe les valeurs brutes ici.
    def encrypt_contact(self, value): return value
    def encrypt_email(self, value): return value
    def encrypt_history(self, value): return value

# Instances du schéma pour utilisation dans les contrôleurs
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)