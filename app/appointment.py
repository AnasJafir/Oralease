# app/features/appointments.py

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from app import db
from app.models import Appointment, Patient, InventoryItem
from datetime import datetime, timedelta
from app.authentication_decorators import login_required, role_required

# Create a Blueprint instance
appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/')
@login_required
@role_required('admin', 'user')
def index():
    """
    This route is the root of the appointments blueprint.
    
    It is protected by the login_required decorator, which will redirect to the
    login page if the user is not logged in.
    
    It is also protected by the role_required decorator, which will only allow
    users with the role 'admin' or 'user' to access this route.
    
    The route is a GET request, and it retrieves the upcoming appointments and
    low inventory items to display on the dashboard.
    
    If the user is not logged in, it redirects to the login page.
    
    Returns the rendered dashboard template with upcoming appointments, low 
    inventory items, and the user's role.
    """
    """
    This function retrieves the upcoming appointments and low inventory items for display on the dashboard.
    If the user is not logged in, it redirects to the login page.
    Returns the rendered dashboard template with upcoming appointments, low inventory items, and the user's role.
    """
    today = datetime.utcnow()
    two_days_from_now = today + timedelta(days=2)

    upcoming_appointments = Appointment.query.filter(
        Appointment.appointment_date.between(today, two_days_from_now)
    ).order_by(Appointment.appointment_date.asc()).all()
    
    # Query for items that are low in stock
    low_inventory_items = InventoryItem.query.filter(InventoryItem.quantity < InventoryItem.threshold).all()
    
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_role = session.get('role')
    
    return render_template('dashboard.html', upcoming_appointments=upcoming_appointments, low_inventory_items=low_inventory_items, role=user_role)

# Add Appointment Route (GET for form, POST to submit)
@appointments_bp.route('/add_appointment', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'user')
def add_appointment():
    """
    The add_appointment route handles both GET and POST requests.
    
    GET: Renders a form to add a new appointment.
        The form is rendered with a dropdown menu of all patients in the database.
        The patients are fetched from the database via the Patient model.
        The form is rendered with the add_appointment.html template.
    POST: Adds a new appointment to the database with the submitted form data.
        The form data is retrieved from the request.form object.
        A new Appointment object is created with the form data.
        The new Appointment object is added to the database via the db.session.add() method.
        The database is committed via the db.session.commit() method.
        After adding the appointment, the user is redirected to the appointment list.
    """
    if request.method == 'GET':
        # Fetch all patients for the dropdown menu
        patients = Patient.query.all()
        # Render the form with the patients
        return render_template('add_appointment.html', patients=patients)

    # When the form is submitted via POST
    # Retrieve the form data
    data = request.form
    
    # Create a new Appointment object with the form data
    new_appointment = Appointment(
        # The patient_id is retrieved from the form data
        patient_id=data['patient_id'],
        # The appointment_date is retrieved from the form data
        # Assume it's already a datetime object
        appointment_date=data['appointment_date'],
        # The notes are retrieved from the form data
        # If the notes field is empty, set it to an empty string
        notes=data.get('notes', '')
    )
    
    # Add the new Appointment object to the database
    db.session.add(new_appointment)
    
    # Commit the database
    db.session.commit()
    
    # Redirect to the appointment list after adding
    return redirect(url_for('appointments.get_appointments'))


# List Appointments Route
# Define a route to handle GET requests for '/appointments'
@appointments_bp.route('/appointments', methods=['GET'])
# Ensure the user is logged in before accessing this route
@login_required
# Check if the user has the role of 'admin' or 'user'
@role_required('admin', 'user')
def get_appointments():
    """
    List Appointments Route

    This route retrieves all appointments from the database. It's accessible by both
    admins and users. The appointments are sorted in ascending order based on their ID.

    Returns:
        A rendered template at list_appointments.html containing the list of appointments.
    """
    # Print the session information
    print(session)
    
    # Retrieve all appointments from the database and order them by ID in ascending order
    appointments = Appointment.query.order_by(Appointment.id.asc()).all()
    
    # Render the 'list_appointments.html' template with the retrieved appointments
    return render_template('list_appointments.html', appointments=appointments)

# Update Appointment Route (GET for form, POST to update)
@appointments_bp.route('/update_appointment/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'user')
def update_appointment(id):
    """
    Route to Update an Existing Appointment
    
    This route allows users with 'admin' or 'user' roles to update an existing appointment.
    
    GET Request:
        - Retrieves all patients and the details of the appointment to be updated.
        - Renders the 'update_appointment.html' template with the appointment and list of patients for editing.
    
    POST Request:
        - Receives updated appointment data from the form submission.
        - Updates the appointment's patient ID, appointment date, and notes with the new data.
        - Saves the changes to the database.
        - Redirects the user to the list of appointments after the update.
    
    Parameters:
        id (int): The ID of the appointment to be updated.
    
    Returns:
        - On GET: Renders the 'update_appointment.html' template with the appointment and patients.
        - On POST: Redirects to the list of appointments after successful update.
        - If the appointment is not found, returns a 404 error.
    """
    # Retrieve the appointment with the given ID
    appointment = Appointment.query.get(id)

    # Check if the appointment exists
    if not appointment:
        return {"error": "Appointment not found"}, 404

    # Process GET request
    if request.method == 'GET':
        # Fetch all patients for the dropdown menu
        patients = Patient.query.all()
        # Render the form with the appointment and patients for editing
        return render_template('update_appointment.html', appointment=appointment, patients=patients)

    # Process POST request for updating appointment
    data = request.form
    appointment.patient_id = data['patient_id']
    appointment.appointment_date = data['appointment_date']
    appointment.notes = data.get('notes', '')

    # Commit the changes to the database
    db.session.commit()

    # Redirect to the list of appointments after updating
    return redirect(url_for('appointments.get_appointments'))

# Retrieve a Single Appointment by ID
@appointments_bp.route('/appointment/<int:id>', methods=['GET'])
@login_required
@role_required('admin', 'user')
def get_appointment(id):
    """
    Retrieves an appointment with the given ID and renders the 'view_appointment.html' template
    with the appointment details.

    Parameters:
        id (int): The ID of the appointment to be viewed.

    Returns:
        - On GET: Renders the 'view_appointment.html' template with the appointment.
        - If the appointment is not found, returns a 404 error.
    """
    # Retrieve the appointment with the given ID from the database.
    appointment = Appointment.query.get(id)

    # If the appointment is not found in the database, return a 404 error.
    if not appointment:
        return {"error": "Appointment not found"}, 404

    # Render the 'view_appointment.html' template with the appointment details.
    return render_template('view_appointment.html', appointment=appointment)

# Delete Appointment Route
@appointments_bp.route('/delete_appointment/<int:id>', methods=['POST'])
@login_required
@role_required('admin', 'user')
def delete_appointment(id):
    """
    Deletes an appointment with the specified ID.

    This function handles the deletion of an appointment from the database.
    It checks if the appointment exists and, if found, deletes it. The user
    must be logged in and have the appropriate role to perform this action.

    Parameters:
        id (int): The ID of the appointment to be deleted. This is passed as a
            URL parameter in the route, as defined in the route decorator.

    Returns:
        - If the appointment is found and deleted, redirects to the list
          of appointments. This is done by redirecting to the route for the
          list of appointments, which is defined elsewhere in the code.
        - If the appointment is not found, returns a 404 error. This is done
          by returning a dictionary with a single key-value pair, where the
          key is 'error' and the value is a string describing the error.
    """
    # Retrieve the appointment with the given ID from the database.
    # This is done using the Appointment.query.get() method, which returns
    # an instance of the Appointment class if an appointment with the given
    # ID exists, or None if no such appointment exists.
    appointment = Appointment.query.get(id)

    # Check if the appointment was found in the database.
    # If the appointment was not found, return a 404 error.
    if not appointment:
        return {"error": "Appointment not found"}, 404

    # Delete the appointment from the database.
    # This is done using the db.session.delete() method, which marks the
    # appointment as deleted in the database session.
    db.session.delete(appointment)

    # Commit the changes to the database.
    # This is done using the db.session.commit() method, which writes the
    # changes to the database.
    db.session.commit()

    # Redirect to the list of appointments after deletion.
    # This is done using the redirect() function, which redirects the user
    # to the route for the list of appointments, which is defined elsewhere
    # in the code.
    return redirect(url_for('appointments.get_appointments'))
