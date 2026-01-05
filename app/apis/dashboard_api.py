# app/apis/dashboard_api.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.models import Appointment, Patient
from app.extensions import db
from datetime import datetime, date

dashboard_api_bp = Blueprint('dashboard_api_v2', __name__)

@dashboard_api_bp.route('/api/v2/dashboard/summary', methods=['GET'])
@jwt_required()
def get_dashboard_summary():
    """
    Récupère les données pour le tableau de bord :
    - Nombre de patients uniques aujourd'hui
    - Liste des rendez-vous du jour
    Note : Revenus et Status sont mockés car non présents en DB.
    """
    today = date.today()
    
    # Récupérer les RDV du jour
    # On filtre sur la date du jour (en supposant que appointment_date est un DateTime, on cast ou on filtre par range)
    # Pour simplifier, on prend tout ce qui commence par la date d'aujourd'hui
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    print(f"DEBUG: Searching appointments for date: {today}")
    print(f"DEBUG: Range: {today_start} - {today_end}")

    appointments_today = Appointment.query.filter(
        Appointment.appointment_date >= today_start,
        Appointment.appointment_date <= today_end
    ).order_by(Appointment.appointment_date.asc()).all()
    
    print(f"DEBUG: Found {len(appointments_today)} appointments.")
    
    # 1. Patients du jour (nombre de RDV uniques ou patients uniques ?) -> Dashboard demande "Patients du jour" -> comptons les RDV
    patients_count = len(appointments_today)
    
    # 2. Transformer les RDV pour le frontend
    appointments_data = []
    for apt in appointments_today:
        patient_name = f"{apt.patient.first_name} {apt.patient.last_name}" if apt.patient else "Inconnu"
        
        # Utilisation des vrais champs en base
        apt_type = apt.type
        status = apt.status
        
        urgent = False
        if "urgence" in apt_type.lower() or "emergency" in apt_type.lower():
            urgent = True
            
        appointments_data.append({
            "id": apt.id,
            "patient_id": apt.patient_id,
            "time": apt.appointment_date.strftime("%H:%M"),
            "patient": patient_name,
            "type": apt_type,
            "status": status,
            "urgent": urgent
        })

    # 3. Calcul Revenus (Factures Payées ce mois-ci)
    from app.models import Invoice
    from sqlalchemy import func
    
    current_month = today.month
    current_year = today.year
    
    revenue_query = db.session.query(func.sum(Invoice.total_amount)).filter(
        Invoice.status == 'Paid',
        func.extract('month', Invoice.issue_date) == current_month,
        func.extract('year', Invoice.issue_date) == current_year
    ).scalar()
    
    monthly_revenue = revenue_query if revenue_query else 0.0
    formatted_revenue = f"{monthly_revenue:,.2f} €".replace(",", " ").replace(".", ",")

    stats = {
        "patients_today": patients_count,
        "revenue": formatted_revenue, 
        "occupancy": "85%" # TODO: Calculer occupations
    }

    return jsonify({
        "stats": stats,
        "appointments": appointments_data
    }), 200
