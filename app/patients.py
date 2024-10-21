from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app import db
from app.utils.encryption import encrypt_data, decrypt_data
from app.models import Patient, Appointment, InventoryItem, TreatmentPlan
from datetime import datetime, timedelta
from app.authentication_decorators import login_required, role_required

# Create a Blueprint instance
patients_bp = Blueprint('patients', __name__)

# Dashboard route
@patients_bp.route('/')
@login_required
@role_required('admin', 'user')
def index():
    """
    This is the main dashboard route. When a user logs in, they will be redirected to this route.
    It shows upcoming appointments and low inventory items.
    
    :returns: A rendered template
    """
    # Get today's date
    today = datetime.utcnow()
    
    # Calculate two days from today's date
    two_days_from_now = today + timedelta(days=2)
    
    # Query the Appointment table to retrieve all upcoming appointments within the next two days
    # The appointments are sorted by their dates in ascending order
    upcoming_appointments = Appointment.query.filter(
        Appointment.appointment_date.between(today, two_days_from_now)
    ).order_by(Appointment.appointment_date.asc()).all()
    
    # Query the InventoryItem table to retrieve all items that are low in stock
    # Low in stock means the quantity is less than the threshold
    low_inventory_items = InventoryItem.query.filter(InventoryItem.quantity < InventoryItem.threshold).all()
    
    # If the user is not logged in (i.e., 'user_id' is not in the session), redirect them to the login page
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Retrieve the user's role from the session
    user_role = session.get('role')
    
    # Render the dashboard template, passing in the upcoming appointments, low inventory items, and the user's role
    return render_template('dashboard.html', upcoming_appointments=upcoming_appointments, low_inventory_items=low_inventory_items, role=user_role)
# Add Patient Route (GET for form, POST to submit)
@patients_bp.route('/add_patient', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'user')
def add_patient():
    """
    Route to add a new patient to the system.

    GET: Renders the 'add_patient.html' template which contains the form for inputting patient details.
    POST: Processes the form submission, encrypts sensitive data, adds the new patient to the database,
    and redirects the user to the patient list page.
    """
    # If the request method is GET, render the form template
    if request.method == 'GET':
        return render_template('add_patient.html')
    
    # When the form is submitted via POST, retrieve the submitted form data
    data = request.form

    # Extract sensitive information from form data for encryption
    contact_number = data['contact_number']  # Contact number of the patient
    email = data['email']                    # Email address of the patient
    medical_history = data.get('medical_history', '')  # Medical history, defaulting to an empty string if not provided

    # Create a new Patient object, encrypting sensitive data before storage
    new_patient = Patient(
        first_name=data['first_name'],                   # Patient's first name
        last_name=data['last_name'],                     # Patient's last name
        date_of_birth=data['date_of_birth'],             # Patient's date of birth
        contact_number=encrypt_data(contact_number),     # Encrypt and store contact number
        email=encrypt_data(email),                       # Encrypt and store email address
        medical_history=encrypt_data(medical_history)    # Encrypt and store medical history
    )

    # Add the new Patient object to the database session
    db.session.add(new_patient)
    # Commit the session to save the new patient to the database
    db.session.commit()
    
    # After successfully adding the patient, redirect to the patient list page
    return redirect(url_for('patients.get_patients'))



# List Patients Route
@patients_bp.route('/patients', methods=['GET'])
@login_required
@role_required('admin', 'user')
def get_patients():
    """
    This function handles the GET request to retrieve all patients from the database.
    It then decrypts sensitive fields such as contact number, email, and medical history before rendering the list of patients template.
    """
    # Retrieve all patients from the database and order them by ID in ascending order
    patients = Patient.query.order_by(Patient.id.asc()).all()
    
    # Decrypt sensitive fields for display
    for patient in patients:
        patient.contact_number = decrypt_data(patient.contact_number)
        patient.email = decrypt_data(patient.email)
        patient.medical_history = decrypt_data(patient.medical_history)

    # Render the list of patients template with the decrypted patient data
    return render_template('list_patients.html', patients=patients)


# Update Patient Route (GET for form, POST to update)
@patients_bp.route('/update_patient/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'user')
def update_patient(id):
    """
    Handles GET and POST requests to update patient information.

    GET request:
        Retrieves patient data for the given ID and renders the update_patient.html template with the decrypted patient data.

    POST request:
        Updates the patient information with the provided data, encrypting sensitive fields before storing them in the database.

    :param id: ID of the patient to update.
    """
    # Retrieve the requested patient from the database
    patient = Patient.query.get(id)

    # If the patient is not found, return a 404 error
    if not patient:
        return {"error": "Patient not found"}, 404

    # Handle GET request to retrieve patient data for updating
    if request.method == 'GET':
        # Create a dictionary to store the decrypted patient data
        patient_data = {
            'id': patient.id,  # Patient's ID
            'first_name': patient.first_name,  # Patient's first name
            'last_name': patient.last_name,  # Patient's last name
            'date_of_birth': patient.date_of_birth,  # Patient's date of birth
            # Decrypt the contact number and medical history to store in the dictionary
            'contact_number': decrypt_data(patient.contact_number),
            'email': decrypt_data(patient.email),
            'medical_history': decrypt_data(patient.medical_history)
        }

        # Render the update_patient.html template with the decrypted patient data
        return render_template('update_patient.html', patient=patient_data)

    # Handle POST request to update patient information
    else:
        # Retrieve the updated patient information from the POST request
        data = request.form

        # Update the patient information
        patient.first_name = data['first_name']  # Patient's first name
        patient.last_name = data['last_name']  # Patient's last name
        patient.date_of_birth = data['date_of_birth']  # Patient's date of birth

        # Encrypt the contact number, email, and medical history before storing them in the database
        # Ensure that you're encrypting only plain strings
        patient.contact_number = encrypt_data(data['contact_number'])  # This should be a plain string
        patient.email = encrypt_data(data['email'])  # This should be a plain string
        patient.medical_history = encrypt_data(data['medical_history'])  # This should be a plain string

        # Commit the updated patient information to the database
        db.session.commit()

        # Redirect the user to the patient list page after successful update
        return redirect(url_for('patients.get_patients'))


# Retrieve a Single Patient by ID
@patients_bp.route('/patient/<int:id>', methods=['GET'])
@login_required
@role_required('admin', 'user')
def get_patient(id):
    """
    Handles GET requests to retrieve patient data for the given ID.

    Retrieves the patient record from the database and renders the view_patient.html template with the decrypted patient data.

    :param id: ID of the patient to retrieve.
    """
    # Query the database for a patient with the specified ID
    patient = Patient.query.get(id)
    
    # If no patient is found with the given ID, return a 404 error with a message
    if not patient:
        return {"error": "Patient not found"}, 404
    
    # Decrypt the contact number for display purposes
    patient.contact_number = decrypt_data(patient.contact_number)
    # Decrypt the email for display purposes
    patient.email = decrypt_data(patient.email)
    # Decrypt the medical history for display purposes
    patient.medical_history = decrypt_data(patient.medical_history)
    
    # Render the 'view_patient.html' template, passing the decrypted patient data
    return render_template('view_patient.html', patient=patient)


# Delete Patient Route
@patients_bp.route('/delete_patient/<int:id>', methods=['POST'])
@login_required
@role_required('admin', 'user')
def delete_patient(id):
    """
    Handles POST requests to delete a patient by ID.

    Retrieves the patient record from the database and deletes it. Redirects the user to the patient list page after successful deletion.

    :param id: ID of the patient to delete.
    """
    # Retrieve the patient record from the database using the given ID
    patient = Patient.query.get(id)
    
    # If the patient record isn't found, return a 404 error with a message
    if not patient:
        return {"error": "Patient not found"}, 404
    
    # Delete the patient record from the database
    db.session.delete(patient)
    
    # Commit the deletion to the database
    db.session.commit()
    
    # Redirect the user to the patient list page after successful deletion
    return redirect(url_for('patients.get_patients'))  # Redirect to the patient list after deletion

@patients_bp.route('/search_patient', methods=['POST'])
@login_required
@role_required('admin', 'user')
def get_patient_by_name():
    """
    Handles POST requests to search for a patient by name.

    Retrieves the patient record from the database and decrypts the sensitive data.
    Returns a rendered template with the decrypted patient data and related appointments and treatment plans.
    """
    try:
        # Get the patient name to search for from the POST request
        patient_name = request.form['patient_name'].strip()
        
        # Split the name by spaces to allow searching by first and last names
        name_parts = patient_name.split()

        # If the user provided both first and last names, search for both
        if len(name_parts) == 2:
            first_name, last_name = name_parts
            patients = Patient.query.filter(
                (Patient.first_name.ilike(f'%{first_name}%')) &
                (Patient.last_name.ilike(f'%{last_name}%'))
            ).all()

        # If only one part was provided, search both first and last names
        else:
            patients = Patient.query.filter(
                (Patient.first_name.ilike(f'%{patient_name}%')) |
                (Patient.last_name.ilike(f'%{patient_name}%'))
            ).all()

        # If no patients were found, render an error message
        if not patients:
            return render_template('patient_not_found.html', patient_name=patient_name)
        
        # If a match was found, decrypt patient data for each patient and related appointments and treatment plans
        patients_data = []
        for patient in patients:
            patient_data = {
                'id': patient.id,
                'first_name': patient.first_name,
                'last_name': patient.last_name,
                'date_of_birth': patient.date_of_birth,
                'contact_number': decrypt_data(patient.contact_number),
                'email': decrypt_data(patient.email),
                'medical_history': decrypt_data(patient.medical_history)
            }
            appointments = Appointment.query.filter_by(patient_id=patient.id).all()
            treatment_plans = TreatmentPlan.query.filter_by(patient_id=patient.id).all()
            patients_data.append({
                'patient': patient_data,
                'appointments': appointments,
                'treatment_plans': treatment_plans
            })

        # Render the 'view_patient_with_appointments.html' template with patient data
        return render_template('view_patient_with_appointments.html', patients_data=patients_data)
                             
    except Exception as e:
        return render_template('error.html', message="An error occurred while processing your request.")
