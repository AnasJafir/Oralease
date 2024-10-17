# users.py

from flask import Blueprint, request, jsonify, session, flash, redirect, url_for
from app.models import User, InventoryItem, Appointment
from app import db
from datetime import datetime, timedelta
from functools import wraps

auth_api_bp = Blueprint('auth_api', __name__)

# Admin decorator for protecting routes
def admin_required(f):
    """
    Decorator to protect routes that require admin privileges.

    This decorator is used to protect routes that can only be accessed by users
    with the admin role. It checks if the user is logged in and if they have the
    admin role. If the user is not logged in or does not have the admin role, it
    returns a JSON response with a 403 status code and an error message
    indicating that admin privileges are required. Otherwise, the user is granted
    access to the route.

    The decorator is used to wrap a function that requires admin privileges. The
    wrapped function is called with the original arguments if the user has the
    required privileges. Otherwise, the wrapped function returns a JSON response
    with a 403 status code and an error message indicating that admin privileges
    are required.

    :param f: The function that requires admin privileges.
    :return: The wrapped function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Decorated function that checks if the user is logged in and has the admin role
        before granting access to the route.

        This function is the result of wrapping a function with the admin_required
        decorator. It checks if the user is logged in and if they have the admin role.
        If the user is not logged in or does not have the admin role, it returns a
        JSON response with a 403 status code and an error message indicating that
        admin privileges are required. Otherwise, the user is granted access to the
        route.

        The decorated function takes the same arguments as the original function, and
        returns the same result as the original function if the user has the required
        role. If the user does not have the required role, it returns a JSON response
        with a 403 status code and an error message indicating that admin privileges
        are required.

        The decorated function is used to protect routes that require admin
        privileges. It is used to wrap functions that require admin privileges,
        and is used to check if the user has the required role before granting
        access to the route.
        """
        # Check if the user is logged in and has the admin role
        if 'role' not in session:
            # If the user is not logged in, return a JSON response with a 403
            # status code and an error message indicating that admin privileges
            # are required
            return jsonify({'error': 'Admin privileges required'}), 403
        elif session['role'] != 'admin':
            # If the user is logged in but does not have the admin role, return a
            # JSON response with a 403 status code and an error message
            # indicating that admin privileges are required
            return jsonify({'error': 'Admin privileges required'}), 403
        else:
            # If the user is logged in and has the admin role, call the original
            # function with the original arguments
            return f(*args, **kwargs)
    return decorated_function

# Register a new user (Admin only) - POST
@auth_api_bp.route('/api/register', methods=['POST'])
@admin_required
def register():
    """
    Register a new user

    This endpoint requires admin privileges and registers a new user with the given
    username, email, role, and password. The user is added to the database and a
    success message is returned if the registration is successful.

    The registration process involves checking if the given username already exists
    in the database. If it does, a JSON response with an error message is returned
    indicating that the username already exists. If the username does not exist, a
    new User object is created with the given information and added to the
    database. The password is hashed before it is stored in the database.

    Parameters:
        username (str): The username of the new user.
        email (str): The email address of the new user.
        role (str): The role of the new user.
        password (str): The password of the new user.

    Returns:
        A JSON response with a success message if the registration is successful,
        or a JSON response with an error message if the registration fails.
    """
    # Get the data from the request body
    data = request.get_json()

    # Check if the given username already exists in the database
    if User.query.filter_by(username=data['username']).first():
        # If the username already exists, return a JSON response with an error
        # message indicating that the username already exists
        return jsonify({'error': 'Username already exists'}), 409

    # Create a new User object with the given information
    new_user = User(
        username=data['username'],  # The username of the new user
        email=data['email'],  # The email address of the new user
        role=data['role']  # The role of the new user
    )

    # Set the password of the new user
    new_user.set_password(data['password'])

    # Add the new user to the database
    db.session.add(new_user)

    # Commit the changes to the database
    db.session.commit()

    # Return a JSON response with a success message if the registration is
    # successful
    return jsonify({'message': f'User {data["username"]} created successfully'}), 201

# Login - POST
@auth_api_bp.route('/api/login', methods=['POST'])
def login():
    """
    Login - POST

    Logs in a user if the given credentials are valid.

    This function expects the request body to contain the following keys:
        username (str): The username of the user to log in.
        password (str): The password of the user to log in.

    The function first queries the database to find a User object with the given
    username. If a User object is found, the function checks if the given password
    matches the password stored in the User object. If the password matches, the
    user is logged in and a JSON response with a success message and the username
    of the user is returned. If the password does not match, a JSON response with
    an error message is returned.

    If no User object is found with the given username, a JSON response with an
    error message is returned.

    The function also sets the session variables user_id, role, and username to
    the corresponding values from the User object. This is done so that the user's
    role and username can be accessed in other parts of the application.
    """

    # Get the data from the request body
    data = request.get_json()

    # Query the database to find a User object with the given username
    user = User.query.filter_by(username=data['username']).first()

    # Check if a User object is found and the password matches
    if user and user.check_password(data['password']):
        # Log the user in by setting the session variables
        session['user_id'] = user.id
        session['role'] = user.role
        session['username'] = user.username

        # Make the session permanent so that the user stays logged in even after
        # closing the browser
        session.permanent = True

        # Return a JSON response with a success message and the username of the user
        return jsonify({'message': 'Logged in successfully', 'user': user.username}), 200
    else:
        # Return a JSON response with an error message if the login fails
        return jsonify({'error': 'Invalid credentials'}), 401

# Logout - GET
@auth_api_bp.route('/api/logout', methods=['GET'])
def logout():
    """
    Logs the user out by clearing the session variables.

    This function defines an API endpoint '/api/logout' with the HTTP method 'GET'.
    It is responsible for logging out the user from the application by clearing the session variables.

    The function does not expect any data in the request body.

    Upon successful logout, it returns a JSON response with a success message and a status code of 200.

    :return: A JSON response indicating successful logout with a status code of 200
    """
    # Clear all session data to log the user out
    session.clear()
    
    # Return a JSON response to inform the user that they have logged out successfully
    return jsonify({'message': 'Logged out successfully'}), 200

# Manage users (Admin only) - GET
# Define the route '/api/users' with the method 'GET' for managing users
@auth_api_bp.route('/api/users', methods=['GET'])
@admin_required
def manage_users():
    """
    Retrieves a list of all users in the system.

    This function defines an API endpoint '/api/users' with the HTTP method 'GET'.
    It is responsible for retrieving a list of all users in the system and returning
    them as a JSON response.

    The function requires the user to be logged in and have the role 'admin'.

    The JSON response will contain a list of dictionaries, each dictionary representing
    a user in the system. The dictionary will have the keys 'id', 'username', 'email',
    and 'role'.

    The function will return a status code of 200 if the request is successful.
    """
    # Query the database to retrieve all users
    users = User.query.all()
    
    # Compose a list of dictionaries representing each user
    result = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        } for user in users
    ]
    
    # Return the list of users as a JSON response with status code 200
    return jsonify(result), 200

# Edit user (Admin only) - PUT
@auth_api_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def edit_user(user_id):
    """
    Edit user (Admin only) - PUT

    This function defines an API endpoint '/api/users/<int:user_id>' with the HTTP method 'PUT'.
    It is responsible for editing a user's information in the system.

    The function requires the user to be logged in and have the role 'admin'.

    The request body should contain the following keys:
        username (str): The new username for the user.
        email (str): The new email for the user.
        role (str): The new role for the user.
        password (str): The new password for the user (optional).

    The function will return a JSON response with a success message and status code 200 if the request is successful.
    """

    # Retrieve the user with the given ID from the database
    user = User.query.get_or_404(user_id)

    # Retrieve the JSON data from the request body
    data = request.get_json()

    # Update the user's username, email, and role in the database
    user.username = data.get('username', user.username)  # If 'username' is not provided, use the current username
    user.email = data.get('email', user.email)  # If 'email' is not provided, use the current email
    user.role = data.get('role', user.role)  # If 'role' is not provided, use the current role

    # If a new password was provided, update the user's password in the database
    if data.get('password'):  # Only update password if provided
        user.set_password(data['password'])

    # Commit the changes to the database
    db.session.commit()

    # Return a JSON response with a success message and status code 200
    return jsonify({'message': f'User {user.username} updated successfully'}), 200

# Delete user (Admin only) - DELETE
@auth_api_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """
    Delete user (Admin only) - DELETE

    This function defines an API endpoint '/api/users/<int:user_id>' with the HTTP method 'DELETE'.
    It is responsible for deleting a user from the system.

    The function requires the user to be logged in and have the role 'admin'.

    The function will return a JSON response with a success message and status code 200 if the request is successful.
    If the user attempts to delete their own account, it will return a JSON response with an error message and status code 403.
    """
    # Check if the admin is trying to delete their own account
    if int(session['user_id']) == user_id:
        # Return an error message as JSON with status code 403 if the user tries to delete their own account
        return jsonify({'error': 'Cannot delete your own account'}), 403

    # Retrieve the user object from the database; if not found, return a 404 error response
    user = User.query.get_or_404(user_id)

    # Delete the user from the database session
    db.session.delete(user)

    # Commit the transaction to make the deletion permanent
    db.session.commit()

    # Return a success message as JSON with status code 200
    return jsonify({'message': f'User {user.username} deleted successfully'}), 200

# Dashboard overview (protected route) - GET
@auth_api_bp.route('/api/dashboard', methods=['GET'])
def index():
    """
    This function serves as the API endpoint for retrieving the dashboard overview.
    It verifies that the user is logged in and has the necessary permissions to access the data.
    If the user is not authorized, an error message is returned with status code 401.
    The function queries and returns the upcoming appointments within the next two days 
    and the low inventory items based on the defined thresholds. 
    The response includes structured JSON data containing upcoming appointments with their IDs, 
    patient IDs, and appointment dates, low inventory items with IDs, names, and quantities, 
    and user details like username and role.
    """
    # Check if the user is logged in
    if 'user_id' not in session:
        # Return an error message if the user is not logged in
        return jsonify({'error': 'Unauthorized access, please log in'}), 401

    # Get today's date
    today = datetime.utcnow()

    # Calculate two days from today's date
    two_days_from_now = today + timedelta(days=2)

    # Query the Appointment table to get all upcoming appointments within the next two days
    # The appointments are sorted by their dates in ascending order
    upcoming_appointments = Appointment.query.filter(
        Appointment.appointment_date.between(today, two_days_from_now)
    ).order_by(Appointment.appointment_date.asc()).all()

    # Query the InventoryItem table to get all items that are low in stock
    # Low in stock means the quantity is less than the threshold
    low_inventory_items = InventoryItem.query.filter(
        InventoryItem.quantity < InventoryItem.threshold
    ).all()

    # Create a dictionary to store the upcoming appointments
    upcoming_appointments_dict = []
    for appt in upcoming_appointments:
        # Create a dictionary to store each appointment's data
        appointment_dict = {
            'id': appt.id,
            'patient_id': appt.patient_id,
            'date': appt.appointment_date
        }
        # Append the appointment dictionary to the list
        upcoming_appointments_dict.append(appointment_dict)

    # Create a dictionary to store the low inventory items
    low_inventory_items_dict = []
    for item in low_inventory_items:
        # Create a dictionary to store each item's data
        item_dict = {
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity
        }
        # Append the item dictionary to the list
        low_inventory_items_dict.append(item_dict)

    # Create a dictionary to store the user's data
    user_dict = {
        'username': session.get('username'),
        'role': session.get('role')
    }

    # Return a JSON response with the structured data
    return jsonify({
        'upcoming_appointments': upcoming_appointments_dict,
        'low_inventory_items': low_inventory_items_dict,
        'user': user_dict
    }), 200
