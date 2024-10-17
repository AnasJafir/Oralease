# treatment_plan.py

from flask import Blueprint, request, render_template, redirect, url_for
from app import db
from app.models import TreatmentPlan, Patient, Appointment
from app.authentication_decorators import login_required, role_required

treatment_bp = Blueprint('treatment_plan', __name__, template_folder='templates')

# View all treatment plans
@treatment_bp.route('/treatment_plans', methods=['GET'])
@login_required
@role_required('admin', 'user')
def view_treatment_plans():
    """
    This route is used to view all the treatment plans in the database.

    It is protected by the login_required decorator, which means that the user must be logged in before they can access this route.
    Additionally, the route is protected by the role_required decorator, which means that the user must have either the 'admin' or 'user' role to access this route.

    The route returns a rendered template of 'treatment_plans.html' with a list of all treatment plans.

    The treatment plans are retrieved from the database using the TreatmentPlan.query.all() method.

    The treatment plans are passed to the template as a variable called 'treatment_plans'.

    The template will loop over the treatment plans and display them in a table.

    The user can click on a treatment plan to view its details.

    The user can also delete a treatment plan by clicking on the 'Delete' button.

    The user can also update a treatment plan by clicking on the 'Update' button.

    """

    # Retrieve all treatment plans from the database
    treatment_plans = TreatmentPlan.query.all()

    # Render the 'treatment_plans.html' template with the list of treatment plans
    return render_template('treatment_plans.html', treatment_plans=treatment_plans)

# Add a new treatment plan
@treatment_bp.route('/add_treatment_plan', methods=['GET', 'POST'])
@login_required  # Ensures the user is logged in to access this route
@role_required('admin', 'user')  # Ensures the user has either 'admin' or 'user' role
def add_treatment_plan():
    """
    This route is used to add a new treatment plan to the database.

    It is protected by the login_required decorator, which means that the user must be logged in before they can access this route.
    Additionally, the route is protected by the role_required decorator, which means that the user must have either the 'admin' or 'user' role to access this route.

    The route will first retrieve all patients and appointments from the database.

    If the request method is GET, it will render the 'add_treatment_plan.html' template with the list of patients and appointments.

    If the request method is POST, it will retrieve the data from the form and add a new treatment plan to the database.
    The user will be redirected to the 'view_treatment_plans' route after the treatment plan has been added.

    """
    # Retrieve all patients from the database to populate the dropdown menu
    patients = Patient.query.all()
    # Retrieve all appointments from the database (if needed for the form)
    appointments = Appointment.query.all()
    
    # If the request method is GET, render the form to add a treatment plan
    if request.method == 'GET':
        # Render the 'add_treatment_plan.html' template with patients and appointments data
        return render_template('add_treatment_plan.html', patients=patients, appointments=appointments)

    # If the request method is POST, handle the form submission
    data = request.form  # Retrieve form data from the request
    # Create a new TreatmentPlan object with data from the form
    new_treatment_plan = TreatmentPlan(
        patient_id=data['patient_id'],  # Set the patient_id from the form
        diagnosis=data['diagnosis'],  # Set the diagnosis from the form
        treatment_details=data['treatment_details'],  # Set the treatment details from the form
    )
    # Add the new treatment plan to the database session
    db.session.add(new_treatment_plan)
    # Commit the session to save the new treatment plan to the database
    db.session.commit()
    # Redirect the user to the view_treatment_plans route after adding the treatment plan
    return redirect(url_for('treatment_plan.view_treatment_plans'))

# Update a treatment plan
@treatment_bp.route('/update_treatment_plan/<int:id>', methods=['GET', 'POST'])
@login_required  # Ensures the user is logged in to access this route
@role_required('admin', 'user')  # Ensures the user has either the 'admin' or 'user' role to access this route
def update_treatment_plan(id):
    """
    This route is used to update a treatment plan in the database.

    It is protected by the login_required decorator, which means that the user must be logged in before they can access this route.
    Additionally, the route is protected by the role_required decorator, which means that the user must have either the 'admin' or 'user' role to access this route.

    The route will first retrieve the treatment plan with the id from the database.

    If the request method is GET, it will render the 'update_treatment_plan.html' template with the treatment plan data and a list of all patients and appointments.

    If the request method is POST, it will retrieve the data from the form and update the treatment plan in the database.
    The user will be redirected to the 'view_treatment_plans' route after the treatment plan has been updated.
    """
    # Retrieve the treatment plan with the given ID from the database
    treatment_plan = TreatmentPlan.query.get(id)
    
    # Check if the treatment plan exists
    if not treatment_plan:
        # If the treatment plan does not exist, return a 404 error
        return {"error": "Treatment Plan not found"}, 404
    
    # Retrieve all patients from the database to populate the dropdown menu
    patients = Patient.query.all()
    # Retrieve all appointments from the database (if needed for the form)
    appointments = Appointment.query.all()

    # If the request method is GET, render the form to update the treatment plan
    if request.method == 'GET':
        # Render the 'update_treatment_plan.html' template with patients and appointments data
        return render_template('update_treatment_plan.html', treatment_plan=treatment_plan, patients=patients, appointments=appointments)

    # If the request method is POST, handle the form submission
    data = request.form  # Retrieve form data from the request

    # Update the treatment plan with the form data
    treatment_plan.patient_id = data['patient_id']  # Update the patient ID
    treatment_plan.diagnosis = data['diagnosis']  # Update the diagnosis
    treatment_plan.treatment_details = data['treatment_details']  # Update the treatment details
    treatment_plan.status = data['status']  # Update the status

    # Commit the session to save the updated treatment plan to the database
    db.session.commit()

    # Redirect the user to the view_treatment_plans route after updating the treatment plan
    return redirect(url_for('treatment_plan.view_treatment_plans'))

# Delete a treatment plan
@treatment_bp.route('/delete_treatment_plan/<int:id>', methods=['POST'])
@login_required
@role_required('admin', 'user')
def delete_treatment_plan(id):
    """
    This route is used to delete a treatment plan from the database.

    It is protected by the login_required decorator, which means that the user must be logged in before they can access this route.
    Additionally, the route is protected by the role_required decorator, which means that the user must have either the 'admin' or 'user' role to access this route.

    The route will first retrieve the treatment plan with the given ID from the database and delete it.
    If the treatment plan does not exist, it will return a 404 error.
    If the treatment plan exists, it will delete the treatment plan and redirect the user to the 'view_treatment_plans' route.

    This route is only accessible via a POST request, which is what the web form in the 'update_treatment_plan.html' template will send.
    """
    # Retrieve the treatment plan with the given ID from the database
    treatment_plan = TreatmentPlan.query.get(id)

    # Check if the treatment plan exists
    if not treatment_plan:
        # If the treatment plan does not exist, return a 404 error
        return {"error": "Treatment Plan not found"}, 404

    # Delete the treatment plan from the database
    db.session.delete(treatment_plan)

    # Commit the session to save the changes to the database
    db.session.commit()

    # Redirect the user to the 'view_treatment_plans' route after deleting the treatment plan
    return redirect(url_for('treatment_plan.view_treatment_plans'))

@treatment_bp.route('/treatment_plans/patient/<int:patient_id>', methods=['GET'])
@login_required
@role_required('admin', 'user')
def view_treatment_plans_by_patient(patient_id):
    """
    This route is used to view all treatment plans for a given patient.

    It is protected by the login_required decorator, which means that the user must be logged in before they can access this route.
    Additionally, the route is protected by the role_required decorator, which means that the user must have either the 'admin' or 'user' role to access this route.

    The route will first retrieve all treatment plans for the given patient ID from the database.
    If the treatment plans do not exist, it will return a 404 error.
    If the treatment plans exist, it will render the 'treatment_plans.html' template with the treatment plans data.

    This route is only accessible via a GET request.

    Args:
        patient_id (int): The ID of the patient to view the treatment plans for.

    Returns:
        str: The rendered 'treatment_plans.html' template with the treatment plans data.
    """

    # Retrieve all treatment plans for the given patient ID from the database
    treatment_plans = TreatmentPlan.query.filter_by(patient_id=patient_id).all()

    # Check if the treatment plans exist
    if not treatment_plans:
        # If the treatment plans do not exist, return a 404 error
        return {"error": "Treatment Plans not found"}, 404

    # If the treatment plans exist, render the 'treatment_plans.html' template with the treatment plans data
    return render_template('treatment_plans.html', treatment_plans=treatment_plans)
