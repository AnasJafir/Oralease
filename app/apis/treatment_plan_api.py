# treatment_plan.py

from flask import Blueprint, request, jsonify, redirect, url_for
from app import db
from app.models import TreatmentPlan, Patient, Appointment
from app.authentication_decorators import login_required, role_required

treatment_api_bp = Blueprint('treatment_plan_api', __name__)

# View all treatment plans (GET)
@treatment_api_bp.route('/api/treatment_plans', methods=['GET'])
@login_required
@role_required('admin', 'user')
def view_treatment_plans():
    """
    This route is responsible for handling GET requests to view all treatment plans.

    It is protected by the login_required decorator to ensure that only authenticated users can access it.
    Additionally, the role_required decorator restricts access to users with 'admin' or 'user' roles.

    The function retrieves all treatment plans from the database using TreatmentPlan.query.all() method.

    Each treatment plan is then transformed into a dictionary format with keys: 'id', 'patient_id', 'diagnosis', 'treatment_details', and 'status'.
    
    These dictionaries are collected into a list called 'result'.

    The list of treatment plans is returned as a JSON response with a 200 status code.

    Returns:
        str: A JSON response containing a list of treatment plans.
    """
    # Retrieve all treatment plans from the database
    treatment_plans = TreatmentPlan.query.all()

    # Transform each treatment plan into a dictionary format
    result = [
        {
            'id': plan.id,
            'patient_id': plan.patient_id,
            'diagnosis': plan.diagnosis,
            'treatment_details': plan.treatment_details,
            'status': plan.status,
        } for plan in treatment_plans
    ]

    # Return the list of treatment plans as a JSON response with a 200 status code
    return jsonify(result), 200

# Add a new treatment plan (POST)
@treatment_api_bp.route('/api/treatment_plans', methods=['POST'])
@login_required  # Decorator to ensure the user is logged in
@role_required('admin', 'user')  # Decorator to restrict access to users with 'admin' or 'user' roles
def add_treatment_plan():
    """
    This route is responsible for handling POST requests to add a new treatment plan.

    It is protected by the login_required decorator to ensure that only authenticated users can access it.
    Additionally, the role_required decorator restricts access to users with 'admin' or 'user' roles.

    The function expects the request body to contain a JSON object with the following keys: 'patient_id', 'diagnosis', and 'treatment_details'.

    A new TreatmentPlan object is created with the provided data and added to the database session.

    The database session is then committed to persist the new treatment plan.

    The function returns a JSON response with a 201 status code, containing a message indicating that the treatment plan was added successfully.

    Returns:
        str: A JSON response containing a message indicating that the treatment plan was added successfully.
    """
    # Extract JSON data from the request body
    data = request.get_json()

    # Create a new instance of TreatmentPlan with data from the request
    new_treatment_plan = TreatmentPlan(
        patient_id=data['patient_id'],  # Set the patient ID from the JSON data
        diagnosis=data['diagnosis'],  # Set the diagnosis from the JSON data
        treatment_details=data['treatment_details'],  # Set the treatment details from the JSON data
    )
    
    # Add the new treatment plan to the database session
    db.session.add(new_treatment_plan)
    
    # Commit the session to save the new treatment plan to the database
    db.session.commit()
    
    # Return a JSON response with a success message and a 201 status code
    return jsonify({'message': 'Treatment plan added successfully'}), 201

# Update a treatment plan (PUT)
@treatment_api_bp.route('/api/treatment_plans/<int:id>', methods=['PUT'])
@login_required
@role_required('admin', 'user')
def update_treatment_plan(id):
    """
    This route is responsible for handling PUT requests to update a treatment plan.

    It is protected by the login_required decorator to ensure that only authenticated users can access it.
    Additionally, the role_required decorator restricts access to users with 'admin' or 'user' roles.

    The function expects the request body to contain a JSON object with one or more of the following keys: 'patient_id', 'diagnosis', 'treatment_details', and 'status'.

    The function first retrieves a treatment plan with the given ID from the database.
    If the treatment plan does not exist, it returns a JSON response with a 404 status code and an error message.

    If the treatment plan exists, it updates the treatment plan with the provided data and commits the changes to the database.

    The function returns a JSON response with a 200 status code, containing a message indicating that the treatment plan was updated successfully.

    Args:
        id (int): The ID of the treatment plan to update.

    Returns:
        str: A JSON response containing a message indicating that the treatment plan was updated successfully.
    """
    treatment_plan = TreatmentPlan.query.get(id)
    
    if not treatment_plan:
        # If the treatment plan does not exist, return a JSON response with a 404 status code and an error message
        return jsonify({"error": "Treatment plan not found"}), 404
    
    # Retrieve the JSON data from the request body
    data = request.get_json()

    # Update the treatment plan with the provided data
    # The get() method is used to retrieve the value of the 'patient_id', 'diagnosis', and 'treatment_details' keys from the JSON data
    # If the key does not exist in the JSON data, it defaults to the current value of the treatment plan attribute
    treatment_plan.patient_id = data.get('patient_id', treatment_plan.patient_id)
    treatment_plan.diagnosis = data.get('diagnosis', treatment_plan.diagnosis)
    treatment_plan.treatment_details = data.get('treatment_details', treatment_plan.treatment_details)
    treatment_plan.status = data.get('status', treatment_plan.status)

    # Commit the changes to the database
    db.session.commit()
    
    # Return a JSON response with a 200 status code, containing a message indicating that the treatment plan was updated successfully
    return jsonify({'message': 'Treatment plan updated successfully'}), 200

# Delete a treatment plan (DELETE)
# Define a route to delete a treatment plan through a DELETE request
@treatment_api_bp.route('/api/treatment_plans/<int:id>', methods=['DELETE'])
@login_required  # Ensure the user is authenticated to access this route
@role_required('admin', 'user')  # Check if the user has the necessary roles to delete a treatment plan
def delete_treatment_plan(id):
    """
    This function handles the deletion of a treatment plan from the database based on the provided ID.

    Parameters:
        id (int): The ID of the treatment plan to be deleted.

    Returns:
        A JSON response with a success message if the treatment plan is deleted successfully.
        A JSON response with an error message and status code 404 if the treatment plan is not found in the database.
    """
    # Retrieve the treatment plan from the database based on the provided ID
    treatment_plan = TreatmentPlan.query.get(id)
    
    # Check if the treatment plan exists
    if not treatment_plan:
        # If the treatment plan is not found, return an error response with status code 404
        return jsonify({"error": "Treatment plan not found"}), 404

    # Delete the treatment plan from the database
    db.session.delete(treatment_plan)
    # Commit the deletion to the database
    db.session.commit()
    
    # Return a success message in a JSON response with status code 200
    return jsonify({'message': 'Treatment plan deleted successfully'}), 200

# View treatment plans by patient ID (GET)
@treatment_api_bp.route('/api/treatment_plans/patient/<int:patient_id>', methods=['GET'])
@login_required
@role_required('admin', 'user')
def view_treatment_plans_by_patient(patient_id):
    """
    This function is an API endpoint that returns a list of treatment plans for a given patient ID.

    Parameters:
        patient_id (int): The ID of the patient for which to retrieve treatment plans.

    Returns:
        A JSON response containing a list of treatment plans for the given patient ID.
        A JSON response with an error message and status code 404 if no treatment plans are found for the given patient ID.
    """
    
    # Query the database for all treatment plans with the given patient ID
    treatment_plans = TreatmentPlan.query.filter_by(patient_id=patient_id).all()
    
    # If no treatment plans are found, return an error response with status code 404
    if not treatment_plans:
        return jsonify({"error": "No treatment plans found for this patient"}), 404
    
    # Otherwise, create a list of dictionaries to represent the treatment plans
    result = []
    
    # Iterate over the treatment plans and create a dictionary for each one
    for plan in treatment_plans:
        # Create a dictionary with the treatment plan's ID, patient ID, diagnosis, treatment details, and status
        treatment_plan = {
            'id': plan.id,
            'patient_id': plan.patient_id,
            'diagnosis': plan.diagnosis,
            'treatment_details': plan.treatment_details,
            'status': plan.status,
        }
        
        # Add the dictionary to the list
        result.append(treatment_plan)
    
    # Return a JSON response with the list of treatment plans
    return jsonify(result), 200
