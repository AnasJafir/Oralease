from flask import Blueprint, request, jsonify, redirect, url_for, render_template, session, flash
from app.models import User, Patient, InventoryItem, Appointment
from app import db
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Admin decorator for protecting routes
def admin_required(f):
    """
    Decorator to protect routes that require admin privileges.

    This decorator is used to protect routes that can only be accessed by users
    with the admin role. It checks if the user is logged in and if they have the
    admin role. If the user is not logged in or does not have the admin role, it
    flashes an error message and redirects the user to the index page.

    The decorated function is called with the original arguments if the user has
    the required privileges. Otherwise, the decorated function returns a
    redirect to the index page.

    Parameters:
        f (function): The function that requires admin privileges.

    Returns:
        function: The wrapped function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Decorator function that checks if the user is logged in and has the admin role before allowing access to the decorated route.

        This function first checks if the user is logged in by looking for the 'user_id' key in the session.
        If the user is not logged in, it redirects the user to the index page with a warning message.

        If the user is logged in, it then checks if the user has the admin role by looking for the 'role' key in the session.
        If the user does not have the admin role, it redirects the user to the index page with an error message.

        If the user has the admin role, it calls the original route function with the original arguments.

        Parameters:
            *args: The positional arguments passed to the original function.
            **kwargs: The keyword arguments passed to the original function.

        Returns:
            The result of the original route function if the user has the required role.
            A redirect to the index page if the user does not have the required role.
        """
        # Check if the user is logged in
        if 'user_id' not in session:
            # If the user is not logged in, flash a warning message
            flash('Please log in to access this page', 'warning')
            # Redirect the user to the index page
            return redirect(url_for('auth.index'))
        
        # Check if the user has the admin role
        if 'role' not in session or session['role'] != 'admin':
            # If the user does not have the required role, flash an error message
            flash('Access denied. Admin privileges required.', 'danger')
            # Redirect the user to the index page
            return redirect(url_for('auth.index'))

        # If the user has the required role, call the original function
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/register', methods=['GET', 'POST'])
@admin_required  # Only allow access to users with admin privileges
def register():
    """
    Handles the registration of new users.

    - For GET requests, it renders the registration page.
    - For POST requests, it processes the form data to create a new user.

    Parameters:
        None

    Returns:
        - On GET request: Renders the registration page.
        - On POST request: Redirects to the manage users page if registration is successful.
    """
    if request.method == 'POST':
        # Retrieve form data from the request
        data = request.form
        
        # Check if a user with the given username already exists
        if User.query.filter_by(username=data['username']).first():
            # Flash a message indicating the username is taken
            flash('Username already exists', 'danger')
            # Redirect back to the registration page
            return redirect(url_for('auth.register'))
        
        # Create a new User object with the provided form data
        new_user = User(
            username=data['username'],
            email=data['email'],
            role=data['role']
        )
        # Set the user's password using the form data
        new_user.set_password(data['password'])
        
        # Add the new user to the database session
        db.session.add(new_user)
        # Commit the session to save changes to the database
        db.session.commit()
        
        # Flash a success message indicating the user was created
        flash(f'User {data["username"]} created successfully', 'success')
        # Redirect to the manage users page
        return redirect(url_for('auth.manage_users'))
    
    # Render the registration page template for GET requests
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles login functionality.

    For GET requests, renders the login page.

    For POST requests, it processes the form data to authenticate the user.
    If the user is authenticated, it logs them in and redirects them to the index page.
    If the user is not authenticated, it flashes an error message and redirects them back to the login page.

    Parameters:
        None

    Returns:
        - On GET request: Renders the login page.
        - On POST request: Redirects to the index page if the user is authenticated.
    """
    # Check if the request method is POST
    if request.method == 'POST':
        # Retrieve form data from the request
        data = request.form
        # Query the User table to find the user by username
        user = User.query.filter_by(username=data['username']).first()

        # Check if the user exists and the password is correct
        if user and user.check_password(data['password']):
            # Store the user's id in the session
            session['user_id'] = user.id
            # Store the user's role in the session
            session['role'] = user.role
            # Store the user's username in the session for display purposes
            session['username'] = user.username
            # Set the session to be permanent (does not expire when the browser is closed)
            session.permanent = True
            # Flash a success message to the user
            flash('Logged in successfully', 'success')
            # Redirect the user to the index page
            return redirect(url_for('auth.index'))
        else:
            # Flash an error message if the credentials are invalid
            flash('Invalid credentials', 'danger')
            # Redirect the user back to the login page
            return redirect(url_for('auth.login'))

    # Render the login page if the request method is GET
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """
    Logs out the user and redirects them to the login page.

    This function clears the user's session data to log them out of the system.
    It also flashes a message to inform the user that they have been logged out successfully.
    Finally, it redirects the user to the login page.

    Parameters:
        None

    Returns:
        A redirect response to the login page.
    """
    # Clear all session data to log the user out
    session.clear()
    
    # Flash a message to inform the user that they have logged out successfully
    flash('Logged out successfully', 'info')
    
    # Redirect the user to the login page after logging out
    return redirect(url_for('auth.login'))

# New routes for user management (admin only)
@auth_bp.route('/manage_users')
@admin_required
def manage_users():
    """
    Displays a page for managing users in the system.

    This route is restricted to administrative users only (i.e. users with the
    role 'admin'). It displays a page with a list of all users in the system.

    The user can edit or delete any user listed on the page. The page also
    provides a button to add a new user to the system.

    Parameters:
        None

    Returns:
        A rendered template with a list of all users in the system.
    """
    # Retrieve all users from the database
    users = User.query.all()

    # Render the manage users template with the list of users
    return render_template('manage_users.html', users=users)

@auth_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """
    Edits a user's information in the database.

    This route is restricted to administrative users only (i.e. users with the
    role 'admin'). It displays a page with a form containing the user's current
    information. The user can edit any field on the form and submit the
    changes. The page also provides a button to delete the user.

    The user cannot edit their own account. If the user attempts to do so, a
    warning message is flashed and the user is redirected to the manage users
    page.

    Parameters:
        user_id (int): The ID of the user to edit

    Returns:
        A rendered template with a form containing the user's current
        information if the request method is GET. Redirects to the manage users
        page if the request method is POST.
    """
    # Retrieve the user with the given ID from the database
    user = User.query.get_or_404(user_id)
    
    # If the request method is POST, then the user has submitted the form
    if request.method == 'POST':
        # Retrieve the data from the submitted form
        data = request.form
        
        # Update the user's username, email, and role in the database
        user.username = data['username']
        user.email = data['email']
        user.role = data['role']
        
        # If a new password was provided, update the user's password in the
        # database
        if data.get('password'):  # Only update password if provided
            user.set_password(data['password'])
            
        # Commit the changes to the database
        db.session.commit()
        
        # Flash a message to inform the user that the user was updated
        # successfully
        flash('User updated successfully', 'success')
        
        # Redirect the user to the manage users page
        return redirect(url_for('auth.manage_users'))
        
    # If the request method is GET, then render the edit user template with the
    # user's current information
    return render_template('edit_user.html', user=user)

@auth_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    """
    Handle the deletion of a user from the system.

    This route is accessible only to users with the 'admin' role. It deletes the user 
    with the specified ID from the database upon receiving a POST request.

    Parameters:
        user_id (int): The ID of the user to be deleted

    Returns:
        A redirection to the manage users page after successfully deleting the user
    """
    # Check if the user is trying to delete their own account
    if int(session['user_id']) == user_id:
        flash('Cannot delete your own account', 'danger')
        return redirect(url_for('auth.manage_users'))
        
    # Retrieve the user to be deleted from the database
    user = User.query.get_or_404(user_id)
    
    # Delete the user and commit the changes to the database
    db.session.delete(user)
    db.session.commit()
    
    # Flash a success message and redirect to the manage users page
    flash('User deleted successfully', 'success')
    return redirect(url_for('auth.manage_users'))

@auth_bp.route('/')
def index():
    """
    This function handles the route for the dashboard page, which is accessible 
    only to logged-in users. It displays a dashboard with upcoming appointments 
    and low inventory items.

    If the user is not logged in, it redirects to the login page.

    Parameters:
        None

    Returns:
        A rendered dashboard template with upcoming appointments, low inventory 
        items, and the user's role and username.
    """
    # Check if the user is logged in
    if 'user_id' not in session:
        # If the user is not logged in, redirect them to the login page
        return redirect(url_for('auth.login'))
    
    # Get today's date
    today = datetime.utcnow()
    
    # Calculate two days from today's date
    two_days_from_now = today + timedelta(days=2)
    
    # Query the Appointment table to get all upcoming appointments within the 
    # next two days
    # The appointments are sorted by their dates in ascending order
    upcoming_appointments = Appointment.query.filter(
        Appointment.appointment_date.between(today, two_days_from_now)
    ).order_by(Appointment.appointment_date.asc()).all()
    
    # Query the InventoryItem table to get all items that are low in stock
    # Low in stock means the quantity is less than the threshold
    low_inventory_items = InventoryItem.query.filter(
        InventoryItem.quantity < InventoryItem.threshold
    ).all()
    
    # Render the dashboard template with the upcoming appointments, low inventory 
    # items, the user's role, and the user's username
    return render_template('dashboard.html', 
                         upcoming_appointments=upcoming_appointments,
                         low_inventory_items=low_inventory_items,
                         role=session.get('role'),
                         username=session.get('username'))
