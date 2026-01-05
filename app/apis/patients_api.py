# app/apis/patients_api.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Patient
from app.schemas.patient_schema import patient_schema, patients_schema
from flask_jwt_extended import jwt_required, get_jwt 
from marshmallow import ValidationError

patients_api_bp = Blueprint('patients_api_v2', __name__)

# --- Récupérer tous les patients ---
@patients_api_bp.route('/api/v2/patients', methods=['GET'])
@jwt_required() # Protection JWT activée
def get_patients():
    patients = Patient.query.order_by(Patient.id.desc()).all()
    # Sérialisation automatique (incluant le déchiffrement)
    return patients_schema.jsonify(patients), 200

# --- Récupérer un patient ---
@patients_api_bp.route('/api/v2/patients/<int:id>', methods=['GET'])
@jwt_required()
def get_patient(id):
    patient = Patient.query.get_or_404(id)
    return patient_schema.jsonify(patient), 200

# --- Créer un patient (Avec Validation) ---
@patients_api_bp.route('/api/v2/patients', methods=['POST'])
@jwt_required()
def add_patient():
    json_data = request.get_json()
    
    if not json_data:
        return jsonify({"message": "Aucune donnée fournie"}), 400

    try:
        # 1. Validation des données via Marshmallow
        # Note: load() valide les types et les champs required
        data = patient_schema.load(json_data)
        
        # 2. Création de l'objet
        # Comme notre modèle gère le chiffrement dans __init__, on instancie manuellement
        new_patient = Patient(
            first_name=data.first_name,
            last_name=data.last_name,
            date_of_birth=data.date_of_birth,
            contact_number=json_data['contact_number'], # On passe la donnée brute pour chiffrement
            email=json_data['email'],
            medical_history=json_data.get('medical_history', '')
        )

        db.session.add(new_patient)
        db.session.commit()

        return patient_schema.jsonify(new_patient), 201

    except ValidationError as err:
        # Retourne les erreurs précises (ex: "Email invalide")
        return jsonify(err.messages), 422
    except Exception as e:
        return jsonify({"message": f"Erreur serveur: {str(e)}"}), 500

# --- Mettre à jour un patient ---
@patients_api_bp.route('/api/v2/patients/<int:id>', methods=['PUT'])
@jwt_required()
def update_patient(id):
    patient = Patient.query.get_or_404(id)
    json_data = request.get_json()

    try:
        # Validation partielle (partial=True)
        data = patient_schema.load(json_data, partial=True)
        
        # Mise à jour manuelle pour gérer le chiffrement si nécessaire
        if 'first_name' in json_data: patient.first_name = json_data['first_name']
        if 'last_name' in json_data: patient.last_name = json_data['last_name']
        if 'date_of_birth' in json_data: patient.date_of_birth = data.date_of_birth
        
        # Importation locale pour éviter les cycles, si nécessaire
        from app.utils.encryption import encrypt_data
        
        if 'contact_number' in json_data: 
            patient.contact_number = encrypt_data(json_data['contact_number'])
        if 'email' in json_data:
            patient.email = encrypt_data(json_data['email'])
        if 'medical_history' in json_data:
            patient.medical_history = encrypt_data(json_data['medical_history'])
            
        db.session.commit()
        return patient_schema.jsonify(patient), 200

    except ValidationError as err:
        return jsonify(err.messages), 422

# --- Supprimer un patient ---
@patients_api_bp.route('/api/v2/patients/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_patient(id):
    try:
        patient = Patient.query.get_or_404(id)
        
        # Suppresssion manuelle des dépendances pour éviter les problèmes de cascade/intégrité
        from app.models import Appointment, TreatmentPlan, Invoice, Quote, DentalChart, XRayAnalysis
        
        # IMPORTANT: L'ordre peut compter pour éviter les FK violations entre enfants
        
        # 1. Factures & Devis (peuvent être liés aux traitements)
        Invoice.query.filter_by(patient_id=id).delete()
        Quote.query.filter_by(patient_id=id).delete()
        
        # 2. Traitements (peuvent être liés aux factures, mais on vient de les supprimer)
        TreatmentPlan.query.filter_by(patient_id=id).delete()
        
        # 3. Rendez-vous
        Appointment.query.filter_by(patient_id=id).delete()
        
        # 4. Autres données cliniques
        DentalChart.query.filter_by(patient_id=id).delete()
        XRayAnalysis.query.filter_by(patient_id=id).delete()
        
        # 5. Le Patient lui-même
        db.session.delete(patient)
        db.session.commit()
        
        return jsonify({"message": "Patient et données associées supprimés avec succès"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erreur lors de la suppression: {str(e)}"}), 500