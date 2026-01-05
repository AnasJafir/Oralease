# app/apis/xray_api.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import XRayAnalysis, Patient
from app.ai_utils import analyze_xray
from flask_jwt_extended import jwt_required

xray_api_bp = Blueprint('xray_api_v2', __name__)

@xray_api_bp.route('/api/v2/xray/analyze', methods=['POST'])
@jwt_required()
def analyze_xray_endpoint():
    """
    Endpoint pour uploader une radio et recevoir une analyse IA.
    Attend un champ form-data 'image' et un 'patient_id'.
    """
    if 'image' not in request.files:
        return jsonify({"error": "Aucune image fournie"}), 400
    
    patient_id = request.form.get('patient_id')
    if not patient_id:
        return jsonify({"error": "ID Patient manquant"}), 400

    # Vérification de l'existence du patient
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient introuvable"}), 404

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Nom de fichier vide"}), 400

    try:
        # Lecture de l'image binaire
        image_data = file.read()

        # Appel au service IA sécurisé
        analysis_result = analyze_xray(image_data)

        if "error" in analysis_result:
            return jsonify(analysis_result), 500

        # Sauvegarde de l'analyse dans l'historique
        new_analysis = XRayAnalysis(
            patient_id=patient_id,
            xray_image=image_data, # Stockage binaire (attention à la taille en prod, S3 préféré)
            analysis_results=analysis_result
        )
        
        db.session.add(new_analysis)
        db.session.commit()

        return jsonify({
            "message": "Analyse terminée avec succès",
            "analysis_id": new_analysis.id,
            "result": analysis_result
        }), 200

    except Exception as e:
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500