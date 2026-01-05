# app/apis/appointments_api.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Appointment
from app.schemas.appointment_schema import appointment_schema, appointments_schema
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from datetime import datetime

appointments_api_bp = Blueprint('appointments_api_v2', __name__)

# --- Lister les RDV ---
@appointments_api_bp.route('/api/v2/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    """Récupère tous les rendez-vous, triés par date."""
    appointments = Appointment.query.order_by(Appointment.appointment_date.asc()).all()
    return appointments_schema.jsonify(appointments), 200

# --- Détail d'un RDV ---
@appointments_api_bp.route('/api/v2/appointments/<int:id>', methods=['GET'])
@jwt_required()
def get_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    return appointment_schema.jsonify(appointment), 200

# --- Créer un RDV ---
@appointments_api_bp.route('/api/v2/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Données manquantes"}), 400

    try:
        # Validation et création de l'objet
        new_appointment = appointment_schema.load(json_data)
        
        db.session.add(new_appointment)
        db.session.commit()
        
        return appointment_schema.jsonify(new_appointment), 201

    except ValidationError as err:
        return jsonify(err.messages), 422
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# --- Mise à jour RDV ---
@appointments_api_bp.route('/api/v2/appointments/<int:id>', methods=['PUT'])
@jwt_required()
def update_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    json_data = request.get_json()

    try:
        # Mise à jour partielle
        updated_appointment = appointment_schema.load(json_data, instance=appointment, partial=True)
        
        db.session.commit()
        return appointment_schema.jsonify(updated_appointment), 200

    except ValidationError as err:
        return jsonify(err.messages), 422

# --- Supprimer RDV ---
@appointments_api_bp.route('/api/v2/appointments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    return jsonify({"message": "Rendez-vous supprimé avec succès"}), 200