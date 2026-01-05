# app/apis/treatment_api.py
from flask import Blueprint, request, jsonify
from app.services.treatment_service import TreatmentService
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

treatment_api_bp = Blueprint('treatment_api_v2', __name__)

@treatment_api_bp.route('/api/v2/treatments', methods=['GET'])
@jwt_required()
def get_treatments():
    patient_id = request.args.get('patient_id')
    treatments = TreatmentService.get_treatments(patient_id)
    return jsonify(treatments), 200

@treatment_api_bp.route('/api/v2/treatments/<int:id>', methods=['GET'])
@jwt_required()
def get_treatment(id):
    plan = TreatmentService.get_treatment_by_id(id)
    return jsonify(plan), 200

@treatment_api_bp.route('/api/v2/treatments', methods=['POST'])
@jwt_required()
def create_treatment():
    json_data = request.get_json()
    try:
        new_plan = TreatmentService.create_treatment(json_data)
        return jsonify(new_plan), 201
    except ValidationError as err:
        return jsonify(err.messages), 422

@treatment_api_bp.route('/api/v2/treatments/<int:id>', methods=['PUT'])
@jwt_required()
def update_treatment(id):
    json_data = request.get_json()
    try:
        updated_plan = TreatmentService.update_treatment(id, json_data)
        return jsonify(updated_plan), 200
    except ValidationError as err:
        return jsonify(err.messages), 422

@treatment_api_bp.route('/api/v2/treatments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_treatment(id):
    TreatmentService.delete_treatment(id)
    return jsonify({"message": "Plan de traitement supprimé"}), 200