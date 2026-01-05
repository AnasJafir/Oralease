# app/models.py
from app.extensions import db
from datetime import datetime
from sqlalchemy import LargeBinary
from app.utils.encryption import encrypt_data, decrypt_data
from werkzeug.security import generate_password_hash, check_password_hash

# --- Modèle Utilisateur ---
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False) # 'admin', 'doctor', 'secretary'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# --- Modèle Patient ---
# --- Modèle Patient ---
class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    
    # Champs sensibles chiffrés (HDS)
    contact_number = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.LargeBinary, unique=True, nullable=False)
    medical_history = db.Column(db.LargeBinary, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships with Cascade Delete
    appointments = db.relationship('Appointment', backref='patient', cascade='all, delete-orphan')
    treatment_plans = db.relationship('TreatmentPlan', backref='patient', cascade='all, delete-orphan')
    dental_charts = db.relationship('DentalChart', backref='patient', cascade='all, delete-orphan')
    xray_analyses = db.relationship('XRayAnalysis', backref='patient', cascade='all, delete-orphan')
    invoices = db.relationship('Invoice', backref='patient', cascade='all, delete-orphan')
    quotes = db.relationship('Quote', backref='patient', cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, date_of_birth, contact_number, email, medical_history):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        # Chiffrement automatique à la création
        self.contact_number = encrypt_data(contact_number)
        self.email = encrypt_data(email)
        self.medical_history = encrypt_data(medical_history)

# --- Autres Modèles ---
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='Scheduled')
    type = db.Column(db.String(50), default='Consultation')

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    threshold = db.Column(db.Integer, default=25)
    # Unité de mesure (boîte, pièce, kg, etc.)
    unit = db.Column(db.String(50), nullable=True)
    # Description courte pour l'équipe (optionnelle)
    description = db.Column(db.Text, nullable=True)
    # Prix de vente unitaire (pour la caisse / facturation)
    sell_price = db.Column(db.Float, nullable=True)

class TreatmentPlan(db.Model):
    __tablename__ = 'treatment_plans'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment_details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')

class DentalChart(db.Model):
    __tablename__ = 'dental_charts'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    tooth_data = db.Column(db.JSON, nullable=True)

class XRayAnalysis(db.Model):
    __tablename__ = 'xray_analyses'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    xray_image = db.Column(db.LargeBinary, nullable=False)
    analysis_results = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    # New Field: Link to Treatment Plan
    treatment_plan_id = db.Column(db.Integer, db.ForeignKey('treatment_plans.id', ondelete='SET NULL'), nullable=True)
    
    total_amount = db.Column(db.Float, nullable=False) 
    status = db.Column(db.String(50), default='Draft') 
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    items = db.Column(db.JSON, nullable=False) 
    
    treatment_plan = db.relationship('TreatmentPlan', backref='invoices')

class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Draft') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.Column(db.JSON, nullable=False)