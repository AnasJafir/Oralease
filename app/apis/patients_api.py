from flask import Blueprint, request, jsonify, session
from app import db
from app.utils.encryption import encrypt_data, decrypt_data
from app.models import Patient, Appointment, InventoryItem, TreatmentPlan
from datetime import datetime, timedelta
from app.authentication_decorators import login_required, role_required

# Create a Blueprint instance
patients_api_bp = Blueprint('patients_api', __name__)

# RESTful API route to get all patients
@patients_api_bp.route('/api/patients', methods=['GET'])
@login_required
@role_required('admin', 'user')
def get_patients_api():
    """
    This function is an API endpoint that is used to retrieve all patients from the database.

    The function first queries the database for all patients, ordered by their ID in ascending order.
    It then stores the result in a list called 'patients'.

    The function then initializes an empty list called 'patients_data' to store the decrypted
    patient data.

    The function then loops through each patient in the 'patients' list and decrypts the sensitive
    fields of contact number, email, and medical history for each patient. These decrypted values
    are then stored in a dictionary with the keys 'id', 'first_name', 'last_name', 'date_of_birth',
    'contact_number', 'email', and 'medical_history'. The decrypted patient data is then appended
    to the 'patients_data' list.

    Finally, the function returns a JSON response containing the 'patients_data' list.

    The function is protected by the login_required decorator, which will
    redirect to the login page if the user is not logged in.

    The function is also protected by the role_required decorator, which
    will only allow users with the role 'admin' or 'user' to access this
    endpoint.

    The function will return a status code of 200 if the request is successful.
    """
    patients = Patient.query.order_by(Patient.id.asc()).all()

    # Decrypt sensitive fields before sending them in response
    patients_data = []
    for patient in patients:
        # Decrypt contact number
        contact_number_decrypted = decrypt_data(patient.contact_number)

        # Decrypt email
        email_decrypted = decrypt_data(patient.email)

        # Decrypt medical history
        medical_history_decrypted = decrypt_data(patient.medical_history)

        # Store decrypted patient data in a dictionary
        patient_data = {
            'id': patient.id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'date_of_birth': patient.date_of_birth,
            'contact_number': contact_number_decrypted,
            'email': email_decrypted,
            'medical_history': medical_history_decrypted
        }

        # Append decrypted patient data to list
        patients_data.append(patient_data)

    # Return JSON response with decrypted patient data
    return jsonify(patients_data), 200

# RESTful API route to get a single patient by ID
@patients_api_bp.route('/api/patient/<int:id>', methods=['GET'])
@login_required
@role_required('admin', 'user')
def get_patient_api(id):
    """
    This is an API endpoint that returns a single patient by its ID.

    The endpoint requires the user to be logged in and have the role 'admin' or 'user'.
    
    The endpoint returns a JSON object with the following keys:
        id: The ID of the patient (an integer)
        first_name: The first name of the patient (a string)
        last_name: The last name of the patient (a string)
        date_of_birth: The date of birth of the patient as an ISO string (e.g. '2021-01-01')
        contact_number: The contact number of the patient (a string)
        email: The email address of the patient (a string)
        medical_history: The medical history of the patient (a string)
    
    If the patient is not found, the endpoint returns a 404 error.
    """
    # Get the patient from the database that matches the given ID
    patient = Patient.query.get(id)

    # If the patient is not found, return a 404 error
    if not patient:
        # Return a JSON object with an error message
        return jsonify({"error": "Patient not found"}), 404

    # Decrypt the sensitive fields (contact number, email, medical history) before sending them in response
    patient_data = {
        # The ID of the patient (an integer)
        'id': patient.id,
        # The first name of the patient (a string)
        'first_name': patient.first_name,
        # The last name of the patient (a string)
        'last_name': patient.last_name,
        # The date of birth of the patient as an ISO string (e.g. '2021-01-01')
        'date_of_birth': patient.date_of_birth,
        # The contact number of the patient (a string)
        'contact_number': decrypt_data(patient.contact_number),
        # The email address of the patient (a string)
        'email': decrypt_data(patient.email),
        # The medical history of the patient (a string)
        'medical_history': decrypt_data(patient.medical_history)
    }

    # Return a JSON object with the decrypted patient data
    return jsonify(patient_data), 200

# RESTful API route to add a new patient
@patients_api_bp.route('/api/patient', methods=['POST'])
@login_required
@role_required('admin', 'user')
def add_patient_api():
    """
    This is an API endpoint that creates a new patient.

    The endpoint requires the user to be logged in and have the role 'admin' or 'user'.
    
    The endpoint expects a JSON object with the following keys:
        first_name: The first name of the patient (a string)
        last_name: The last name of the patient (a string)
        date_of_birth: The date of birth of the patient as an ISO string (e.g. '2021-01-01')
        contact_number: The contact number of the patient (a string)
        email: The email address of the patient (a string)
        medical_history: The medical history of the patient (a string)
    
    The endpoint will create a new Patient object with the provided data and store it in the
    database. The sensitive fields (contact number, email, medical history) will be encrypted
    before being stored.
    
    If the patient is successfully added, the endpoint will return a JSON object with the
    following keys:
        message: A success message (a string)
        patient_id: The ID of the newly created patient (an integer)

    The endpoint will return a 201 status code on success.
    """
    # Get the JSON data from the request body
    data = request.json  

    # Create a new Patient object with the provided data
    new_patient = Patient(
        first_name=data['first_name'],  # The first name of the patient
        last_name=data['last_name'],  # The last name of the patient
        date_of_birth=data['date_of_birth'],  # The date of birth of the patient as an ISO string
        contact_number=encrypt_data(data['contact_number']),  # The contact number of the patient (encrypted)
        email=encrypt_data(data['email']),  # The email address of the patient (encrypted)
        medical_history=encrypt_data(data.get('medical_history', ''))  # The medical history of the patient (encrypted)
    )

    # Add the new Patient object to the database
    db.session.add(new_patient)

    # Commit the changes to the database
    db.session.commit()

    # Return a JSON response with a success message and the ID of the newly created patient
    return jsonify({"message": "Patient added successfully", "patient_id": new_patient.id}), 201

# RESTful API route to update a patient by ID
@patients_api_bp.route('/api/patient/<int:id>', methods=['PUT'])
@login_required
@role_required('admin', 'user')
def update_patient_api(id):
    """
    This API endpoint updates a patient's information in the database based on the provided JSON data.
    
    Parameters:
        id (int): The ID of the patient to be updated.
    
    JSON Data Format:
        {
            'first_name': str,  # The updated first name of the patient
            'last_name': str,  # The updated last name of the patient
            'date_of_birth': str,  # The updated date of birth of the patient
            'contact_number': str,  # The updated contact number of the patient
            'email': str,  # The updated email address of the patient
            'medical_history': str  # The updated medical history of the patient
        }
    
    Returns:
        A JSON response with a success message if the patient is updated successfully.
        A JSON response with an error message and status code 404 if the patient is not found in the database.
    """

    # Retrieve the patient object from the database based on the provided ID
    patient = Patient.query.get(id)

    # If the patient is not found in the database, return an error message with status code 404
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    # Retrieve the JSON data from the request body
    data = request.json

    # Update the patient object's attributes with the provided JSON data
    patient.first_name = data['first_name']  # The updated first name of the patient
    patient.last_name = data['last_name']  # The updated last name of the patient
    patient.date_of_birth = data['date_of_birth']  # The updated date of birth of the patient

    # Encrypt the contact number, email, and medical history before storing them in the database
    patient.contact_number = encrypt_data(data['contact_number'])  # The updated contact number of the patient
    patient.email = encrypt_data(data['email'])  # The updated email address of the patient
    patient.medical_history = encrypt_data(data['medical_history'])  # The updated medical history of the patient

    # Commit the changes to the database
    db.session.commit()

    # Return a JSON response with a success message
    return jsonify({"message": "Patient updated successfully"}), 200

# RESTful API route to delete a patient by ID
@patients_api_bp.route('/api/patient/<int:id>', methods=['DELETE'])
@login_required
@role_required('admin', 'user')
def delete_patient_api(id):
    """
    Handles DELETE requests to delete a patient by ID.

    The endpoint requires the user to be logged in and have the role 'admin' or 'user'.

    The endpoint expects a URL parameter 'id' which is the ID of the patient to delete.

    If the patient is found in the database, the endpoint deletes the patient record from the database
    and returns a JSON response with a success message and status code 200.

    If the patient is not found in the database, the endpoint returns a JSON response with an error message
    and status code 404.
    """
    # Retrieve the patient object from the database based on the provided ID
    patient = Patient.query.get(id)

    # If the patient is not found in the database, return an error message with status code 404
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    # Delete the patient object from the database
    db.session.delete(patient)

    # Commit the changes to the database
    db.session.commit()

    # Return a JSON response with a success message
    return jsonify({"message": "Patient deleted successfully"}), 200

# RESTful API route to search a patient by name
@patients_api_bp.route('/api/patient/search', methods=['POST'])
@login_required
@role_required('admin', 'user')
def search_patient_api():
    """
    Handles POST requests to search a patient by name.

    The endpoint requires the user to be logged in and have the role 'admin' or 'user'.

    The endpoint expects a JSON payload with a single key-value pair: 'patient_name'.

    If the patient is found in the database, the endpoint returns a JSON response with the patient's details
    and a list of appointments and treatment plans associated with the patient, and status code 200.

    If the patient is not found in the database, the endpoint returns a JSON response with an error message
    and status code 404.
    """
    # Get the JSON payload from the request
    data = request.json

    # Extract the patient name from the payload
    patient_name = data.get('patient_name')

    # Query the database to find a patient with a matching name
    # The query is case-insensitive and will match any part of the first or last name
    # We use the ilike() method to perform a case-insensitive search
    patient = Patient.query.filter(
        (Patient.first_name.ilike(f'%{patient_name}%')) |
        (Patient.last_name.ilike(f'%{patient_name}%'))
    ).first()

    # If no patient was found, return an error message with status code 404
    if not patient:
        return jsonify({"error": f"No patient found with name: {patient_name}"}), 404

    # Create a dictionary to hold the patient's details
    patient_data = {}

    # Populate the patient data dictionary with the patient's details
    patient_data['id'] = patient.id
    patient_data['first_name'] = patient.first_name
    patient_data['last_name'] = patient.last_name
    patient_data['date_of_birth'] = patient.date_of_birth
    # Decrypt the patient's contact number and email
    patient_data['contact_number'] = decrypt_data(patient.contact_number)
    patient_data['email'] = decrypt_data(patient.email)
    # Decrypt the patient's medical history
    patient_data['medical_history'] = decrypt_data(patient.medical_history)

    # Query the database to find all appointments associated with the patient
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()

    # Query the database to find all treatment plans associated with the patient
    treatment_plans = TreatmentPlan.query.filter_by(patient_id=patient.id).all()

    # Create a dictionary to hold the patient's appointments and treatment plans
    patient_data_with_associations = {}

    # Populate the patient data dictionary with the patient's details
    patient_data_with_associations['patient'] = patient_data

    # Populate the patient data dictionary with the patient's appointments
    patient_data_with_associations['appointments'] = [appt.serialize() for appt in appointments]

    # Populate the patient data dictionary with the patient's treatment plans
    patient_data_with_associations['treatment_plans'] = [plan.serialize() for plan in treatment_plans]

    # Return the patient data dictionary as a JSON response with status code 200
    return jsonify(patient_data_with_associations), 200
