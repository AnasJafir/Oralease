# app/apis/inventory_api.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import InventoryItem
from app.schemas.inventory_schema import inventory_item_schema, inventory_items_schema
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

inventory_api_bp = Blueprint('inventory_api_v2', __name__)

# --- Lister le stock ---
@inventory_api_bp.route('/api/v2/inventory', methods=['GET'])
@jwt_required()
def get_inventory():
    items = InventoryItem.query.all()
    return inventory_items_schema.jsonify(items), 200

# --- Détail article ---
@inventory_api_bp.route('/api/v2/inventory/<int:id>', methods=['GET'])
@jwt_required()
def get_item(id):
    item = InventoryItem.query.get_or_404(id)
    return inventory_item_schema.jsonify(item), 200

# --- Ajouter article ---
@inventory_api_bp.route('/api/v2/inventory', methods=['POST'])
@jwt_required()
def add_item():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "Données manquantes"}), 400

    try:
        new_item = inventory_item_schema.load(json_data)
        db.session.add(new_item)
        db.session.commit()
        return inventory_item_schema.jsonify(new_item), 201

    except ValidationError as err:
        return jsonify(err.messages), 422

# --- Mise à jour article ---
@inventory_api_bp.route('/api/v2/inventory/<int:id>', methods=['PUT'])
@jwt_required()
def update_item(id):
    item = InventoryItem.query.get_or_404(id)
    json_data = request.get_json()

    try:
        updated_item = inventory_item_schema.load(json_data, instance=item, partial=True)
        db.session.commit()
        return inventory_item_schema.jsonify(updated_item), 200

    except ValidationError as err:
        return jsonify(err.messages), 422

# --- Supprimer article ---
@inventory_api_bp.route('/api/v2/inventory/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_item(id):
    item = InventoryItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Article supprimé"}), 200