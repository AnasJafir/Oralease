from flask import Blueprint, request, jsonify
from app.models import Invoice, Quote, InventoryItem
from app.schemas.invoice_schema import invoice_schema, invoices_schema, quote_schema, quotes_schema
from app.extensions import db
from flask_jwt_extended import jwt_required

invoices_api_bp = Blueprint('invoices_api', __name__)

# --- INVOICES ---
@invoices_api_bp.route('/api/v2/invoices', methods=['GET'])
@jwt_required()
def get_invoices():
    patient_id = request.args.get('patient_id')
    if patient_id:
        invoices = Invoice.query.filter_by(patient_id=patient_id).all()
    else:
        invoices = Invoice.query.all()
    return jsonify(invoices_schema.dump(invoices)), 200

@invoices_api_bp.route('/api/v2/invoices/<int:id>', methods=['GET'])
@jwt_required()
def get_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    return jsonify(invoice_schema.dump(invoice)), 200

@invoices_api_bp.route('/api/v2/invoices', methods=['POST'])
@jwt_required()
def create_invoice():
    data = request.get_json()
    try:
        # --- Calcul de sécurité du total côté backend ---
        items = data.get("items", [])
        if not isinstance(items, list) or not items:
            return jsonify({"error": "Les lignes de facture (items) sont requises."}), 400

        calculated_total = 0.0
        for item in items:
            qty = float(item.get("quantity", 0) or 0)
            price = float(item.get("price", 0) or 0)
            calculated_total += qty * price

        data["total_amount"] = calculated_total

        new_invoice = invoice_schema.load(data)
        db.session.add(new_invoice)

        # --- Déduction simple du stock pour la démo ---
        # Hypothèse démo : la description de la ligne = nom de l'article d'inventaire.
        for item in items:
            name = item.get("description")
            qty = item.get("quantity")
            if not name or not qty:
                continue

            inventory_item = InventoryItem.query.filter_by(name=name).first()
            if inventory_item:
                try:
                    qty_int = int(qty)
                except (TypeError, ValueError):
                    qty_int = 0

                # On ne descend pas en dessous de 0 pour la démo
                inventory_item.quantity = max(0, (inventory_item.quantity or 0) - max(0, qty_int))

        db.session.commit()
        return jsonify(invoice_schema.dump(new_invoice)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 422

@invoices_api_bp.route('/api/v2/invoices/<int:id>', methods=['PUT'])
@jwt_required()
def update_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    data = request.get_json()
    try:
        updated_invoice = invoice_schema.load(data, instance=invoice, partial=True)
        db.session.commit()
        return jsonify(invoice_schema.dump(updated_invoice)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 422

@invoices_api_bp.route('/api/v2/invoices/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    db.session.delete(invoice)
    db.session.commit()
    return jsonify({"message": "Facture supprimée"}), 200

# --- QUOTES (Similaire) ---
@invoices_api_bp.route('/api/v2/quotes', methods=['GET'])
@jwt_required()
def get_quotes():
    patient_id = request.args.get('patient_id')
    if patient_id:
        quotes = Quote.query.filter_by(patient_id=patient_id).all()
    else:
        quotes = Quote.query.all()
    return jsonify(quotes_schema.dump(quotes)), 200

@invoices_api_bp.route('/api/v2/quotes', methods=['POST'])
@jwt_required()
def create_quote():
    data = request.get_json()
    try:
        new_quote = quote_schema.load(data)
        db.session.add(new_quote)
        db.session.commit()
        return jsonify(quote_schema.dump(new_quote)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 422
