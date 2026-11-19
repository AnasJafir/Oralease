# app/treatment_plan.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import TreatmentPlan, Patient, DentalChart
import json
from app.authentication_decorators import login_required, role_required

treatment_bp = Blueprint('treatment_plan_api', __name__)


@treatment_bp.route('/api/treatment_plans/generate/<int:patient_id>', methods=['POST'])
@login_required
@role_required('admin', 'user')
def generate_treatment_plan(patient_id):
    """Generate a treatment plan from the patient record and dental chart.

    The plan is built from the patient's medical history and the stored
    dental chart. It is rule-based, with no external service involved.

    Parameters:
        patient_id (int): The patient the plan is generated for.

    Returns:
        A JSON response with the suggested plan and status 200 on success,
        or an error with status 404 if the patient is not found.
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    dental_chart = DentalChart.query.filter_by(patient_id=patient_id).first()
    chart_data = dental_chart.tooth_data if dental_chart else None

    treatment_suggestions = elaborate_treatment_plan(patient, chart_data)
    treatment_plan = TreatmentPlan(
        patient_id=patient_id,
        diagnosis=treatment_suggestions.get("diagnosis", ""),
        treatment_details=json.dumps(treatment_suggestions),
    )
    db.session.add(treatment_plan)
    db.session.commit()

    return jsonify({"treatment_plan": treatment_suggestions}), 200


def elaborate_treatment_plan(patient, chart_data):
    """Build a rule-based treatment plan from patient data and dental chart.

    Parameters:
        patient: The patient object.
        chart_data: The dental chart data with tooth-specific conditions.

    Returns:
        A dictionary describing the suggested plan.
    """
    treatment_plan = {"diagnosis": ""}

    # Patient history considerations
    treatment_plan["Medical History"] = patient.medical_history

    # Dental chart assessment
    if chart_data:
        treatment_plan["Tooth Conditions"] = chart_data

    return treatment_plan
