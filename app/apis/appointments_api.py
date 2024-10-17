from flask import Blueprint, request, jsonify
from app import db
from app.models import Appointment, Patient
from app.authentication_decorators import login_required, role_required
from datetime import datetime, timedelta

appointments_api_bp = Blueprint('appointments_api', __name__)

# API to get all appointments
@appointments_api_bp.route('/api/appointments', methods=['GET'])
@login_required
@role_required('admin', 'user')
def get_all_appointments():
    """
    This is an API endpoint that returns a list of all appointments in the database.
    
    The endpoint requires the user to be logged in and have the role 'admin' or 'user'.
    
    The endpoint returns a JSON object with a key of 'appointments' and a value of a list of dictionaries.
    Each dictionary in the list represents an appointment and has the following keys:
        id: The ID of the appointment (an integer)
        patient_id: The ID of the related patient (an integer)
        appointment_date: The date of the appointment as an ISO string (e.g. '2021-01-01T00:00:00')
        notes: The notes associated with the appointment (a string)
    
    The list of appointments is sorted in ascending order by their ID.
    """
    # Get all appointments from the database
    appointments = Appointment.query.order_by(Appointment.id.asc()).all()
    
    # Create a list of dictionaries to represent the appointments
    appointments_list = []
    for a in appointments:
        appointment_dict = {}
        # The ID of the appointment
        appointment_dict['id'] = a.id
        # The ID of the related patient
        appointment_dict['patient_id'] = a.patient_id
        # The date of the appointment as an ISO string
        appointment_dict['appointment_date'] = a.appointment_date.isoformat()
        # The notes associated with the appointment
        appointment_dict['notes'] = a.notes
        
        # Add the appointment dictionary to the list
        appointments_list.append(appointment_dict)
    
    # Return the list of appointments as a JSON object
    return jsonify({'appointments': appointments_list}), 200

# API to get a single appointment by ID
@appointments_api_bp.route('/api/appointment/<int:id>', methods=['GET'])
@login_required
@role_required('admin', 'user')
def get_appointment_by_id(id):
    """
    This is an API endpoint that returns a single appointment by its ID.
    
    The endpoint requires the user to be logged in and have the role 'admin' or 'user'.
    
    The endpoint returns a JSON object with the following keys:
        id: The ID of the appointment (an integer)
        patient_id: The ID of the related patient (an integer)
        appointment_date: The date of the appointment as an ISO string (e.g. '2021-01-01T00:00:00')
        notes: The notes associated with the appointment (a string)
    
    If the appointment is not found, the endpoint returns a 404 error.
    """
    # Get the appointment from the database
    appointment = Appointment.query.get(id)
    
    # Check if the appointment was found
    if not appointment:
        # If the appointment was not found, return a 404 error
        return jsonify({"error": "Appointment not found"}), 404
    
    # Create a dictionary to represent the appointment
    appointment_data = {
        # The ID of the appointment
        'id': appointment.id,
        # The ID of the related patient
        'patient_id': appointment.patient_id,
        # The date of the appointment as an ISO string
        'appointment_date': appointment.appointment_date.isoformat(),
        # The notes associated with the appointment
        'notes': appointment.notes
    }
    
    # Return the appointment dictionary as a JSON object
    return jsonify(appointment_data), 200

# API to add a new appointment
@appointments_api_bp.route('/api/appointments', methods=['POST'])
@login_required
@role_required('admin', 'user')
def create_appointment():
    """
    This API endpoint creates a new appointment in the database.

    The endpoint requires the user to be logged in and have the role 'admin' or 'user'.

    Parameters:
        - data (dict): JSON data containing the following keys:
            - patient_id (int): The ID of the patient for the appointment.
            - appointment_date (str): The date and time of the appointment in ISO format.
            - notes (str, optional): Additional notes for the appointment.

    Returns:
        - If successful, returns a JSON object with a success message and the ID of the new appointment.
        - If 'patient_id' or 'appointment_date' is missing in the data, returns an error message and status code 400.
        - If an error occurs during appointment creation, returns an error message and status code 500.
    """
    # Get the JSON data from the POST request
    data = request.json
    
    # Check that the required fields are present in the data
    if not data.get('patient_id') or not data.get('appointment_date'):
        # If the required fields are missing, return an error message and status code 400
        return jsonify({"error": "Patient ID and appointment date are required"}), 400
    
    try:
        # Create a new Appointment object with the data
        new_appointment = Appointment(
            patient_id=data['patient_id'],
            appointment_date=datetime.fromisoformat(data['appointment_date']),
            notes=data.get('notes', '')
        )
        
        # Add the new appointment to the database
        db.session.add(new_appointment)
        
        # Commit the database changes
        db.session.commit()
        
        # Return a JSON object with a success message and the ID of the new appointment
        return jsonify({"message": "Appointment created successfully", "appointment_id": new_appointment.id}), 201
    except Exception as e:
        # If an error occurs during appointment creation, return an error message and status code 500
        return jsonify({"error": str(e)}), 500

# API to update an appointment
@appointments_api_bp.route('/api/appointments/<int:id>', methods=['PUT'])
@login_required
@role_required('admin', 'user')
def update_appointment(id):
    """
    Updates an appointment with the specified ID.

    This function handles the updating of an appointment from the database.
    It checks if the appointment exists and, if found, updates the appointment's
    patient ID, appointment date, and notes. The user must be logged in and
    have the appropriate role to perform this action.

    Parameters:
        id (int): The ID of the appointment to be updated. This is passed as a
            URL parameter in the route, as defined in the route decorator.
    """
    # Retrieve the appointment from the database by its ID
    appointment = Appointment.query.get(id)

    # Check if the appointment was found
    if not appointment:
        # If the appointment was not found, return a 404 error
        return jsonify({"error": "Appointment not found"}), 404

    # Get the JSON data from the PUT request
    data = request.json

    try:
        # Update the appointment's patient ID if it was provided
        appointment.patient_id = data.get('patient_id', appointment.patient_id)

        # Update the appointment's date if it was provided
        if data.get('appointment_date'):
            appointment.appointment_date = datetime.fromisoformat(data['appointment_date'])

        # Update the appointment's notes if they were provided
        appointment.notes = data.get('notes', appointment.notes)

        # Commit the changes to the database
        db.session.commit()

        # Return a JSON object with a success message and the ID of the updated appointment
        return jsonify({"message": "Appointment updated successfully", "appointment_id": appointment.id}), 200
    except Exception as e:
        # If an error occurs during appointment update, return an error message and status code 500
        return jsonify({"error": str(e)}), 500

# API to delete an appointment
@appointments_api_bp.route('/api/appointments/<int:id>', methods=['DELETE'])
@login_required
@role_required('admin', 'user')
def delete_appointment(id):
    """
    Deletes an appointment with the specified ID.

    This function handles the deletion of an appointment from the database.
    It checks if the appointment exists and, if found, deletes the appointment.
    The user must be logged in and have the appropriate role to perform this action.

    Parameters:
        id (int): The ID of the appointment to be deleted. This is passed as a
            URL parameter in the route, as defined in the route decorator.
    """
    # Retrieve the appointment from the database by its ID
    appointment = Appointment.query.get(id)

    # Check if the appointment was found
    if not appointment:
        # If the appointment was not found, return a 404 error
        return jsonify({"error": "Appointment not found"}), 404

    try:
        # Delete the appointment from the database
        db.session.delete(appointment)

        # Commit the changes to the database
        db.session.commit()

        # Return a JSON object with a success message
        return jsonify({"message": "Appointment deleted successfully"}), 200
    except Exception as e:
        # If an error occurs during appointment deletion, return an error message and status code 500
        return jsonify({"error": str(e)}), 500
