# app/apis/auth_api.py
from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db, jwt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_api_bp = Blueprint('auth_api_new', __name__)

@auth_api_bp.route('/api/auth/login', methods=['POST'])
def login():
    """
    Authentification API qui retourne un token JWT.
    Utilisé par l'application Mobile/Desktop.
    """
    if not request.is_json:
        return jsonify({"msg": "JSON manquant dans la requête"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Nom d'utilisateur ou mot de passe manquant"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Création du token d'accès avec l'identité (ID utilisateur) et le rôle
        access_token = create_access_token(identity=user.id, additional_claims={"role": user.role})
        return jsonify(access_token=access_token, role=user.role), 200
    else:
        return jsonify({"msg": "Mauvais identifiants"}), 401

@auth_api_bp.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Route protégée pour tester le token."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"msg": "Utilisateur introuvable"}), 404
        
    return jsonify(id=user.id, username=user.username, role=user.role), 200