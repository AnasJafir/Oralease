# app/treatment_plan.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import TreatmentPlan, Patient, DentalChart, XRayAnalysis
import json
from app.authentication_decorators import login_required, role_required

treatment_bp = Blueprint('treatment_api', __name__)
@treatment_bp.route('/api/treatment_plans/generate/<int:patient_id>', methods=['POST'])
@login_required
@role_required('admin', 'user')
def generate_treatment_plan(patient_id):
    """
    API endpoint for generating treatment plans based on patient data, dental chart, and X-ray analysis.

    This function handles the generation of treatment plans for a given patient ID, incorporating data from the patient's record,
    dental chart, and X-ray analysis to provide personalized recommendations.

    Parameters:
        patient_id (int): The ID of the patient for whom the treatment plan is being generated.

    Returns:
        A JSON response containing a suggested treatment plan based on the patient's data and status code 200 if successful.
        A JSON response with an error message and status code 404 if the patient is not found or no analysis results are available.
    """
    # Retrieve patient information from the database
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    # Retrieve dental chart data
    dental_chart = DentalChart.query.filter_by(patient_id=patient_id).first()
    chart_data = dental_chart.tooth_data if dental_chart else None

    # Retrieve latest X-ray analysis
    xray_analysis = XRayAnalysis.query.filter_by(patient_id=patient_id).order_by(XRayAnalysis.created_at.desc()).first()
    analysis_results = xray_analysis.analysis_results if xray_analysis else None

    if not analysis_results:
        return jsonify({"error": "No X-ray analysis results available for this patient"}), 404

    # Implement logic to generate treatment suggestions based on patient data, dental chart, and X-ray analysis
    treatment_suggestions = elaborate_treatment_plan(patient, chart_data, analysis_results)  # Call the AI logic
    treatment_plan = TreatmentPlan(
        patient_id=patient_id,
        diagnosis=analysis_results.get("diagnosis", ""),
        treatment_details=json.dumps(treatment_suggestions)
    )
    # Persist generated plan (optional but useful)
    db.session.add(treatment_plan)
    db.session.commit()

    # Return the generated treatment plan as a JSON response
    return jsonify({"treatment_plan": treatment_suggestions}), 200

def elaborate_treatment_plan(patient, chart_data, analysis_results):
    """
    Elaborates a treatment plan based on patient history, dental chart data, and X-ray analysis results.

    This function takes patient data, dental chart data, and X-ray analysis results as input and generates a comprehensive treatment plan,
    incorporating considerations for each aspect of the patient's dental health.

    Parameters:
        patient: The patient object containing patient information.
        chart_data: The dental chart data containing tooth-specific conditions.
        analysis_results: The X-ray analysis results providing insights into potential dental issues.

    Returns:
        A dictionary containing the elaborated treatment plan based on the patient's condition.
    """
    treatment_plan = {}

    # Patient History Considerations
    treatment_plan["Medical History"] = patient.medical_history

    # Dental Chart Assessment
    if chart_data:
        treatment_plan["Tooth Conditions"] = chart_data

    # X-Ray Analysis
    if analysis_results:
        treatment_plan["Cavity"] = analysis_results["cavity"]

    # Further steps may include adding specific treatment recommendations based on the above analysis

    return treatment_plan