# inventory.py

from flask import Blueprint, request, render_template, redirect, url_for, session
from app import db
from app.models import InventoryItem, Appointment, Patient
from datetime import datetime, timedelta
from app.authentication_decorators import login_required, role_required

inventory_bp = Blueprint('inventory', __name__, template_folder='templates')

# Define a route function for the root of the inventory blueprint
@inventory_bp.route('/')
@login_required  # Ensures that the user is logged in before accessing this route
@role_required('admin', 'user')  # Restricts access to users with the roles 'admin' or 'user'
def index():
    """
    This route is the root of the inventory blueprint.
    
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
    # Get the current date and time
    today = datetime.utcnow()
    # Calculate the date two days from now
    two_days_from_now = today + timedelta(days=2)

    # Query upcoming appointments within the next two days
    upcoming_appointments = Appointment.query.filter(
        Appointment.appointment_date.between(today, two_days_from_now)
    ).order_by(Appointment.appointment_date.asc()).all()
    
    # Query for items that are low in stock based on the threshold
    low_inventory_items = InventoryItem.query.filter(InventoryItem.quantity < InventoryItem.threshold).all()
    
    # Redirect to the login page if the user is not logged in
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get the role of the user from the session
    user_role = session.get('role')
    
    # Render the dashboard template with upcoming appointments, low inventory items, and the user's role
    return render_template('dashboard.html', upcoming_appointments=upcoming_appointments, low_inventory_items=low_inventory_items, role=user_role)

# Route to display all inventory items
@inventory_bp.route('/inventory', methods=['GET'])
@login_required  # Ensures that the user is logged in before accessing this route
@role_required('admin', 'user')  # Restricts access to users with the roles 'admin' or 'user'
def view_inventory():
    """
    This route displays all inventory items in the database.
    
    It is protected by the login_required decorator, which will redirect to the
    login page if the user is not logged in.
    
    It is also protected by the role_required decorator, which will only allow
    users with the role 'admin' or 'user' to access this route.
    
    The route is a GET request, and it retrieves all inventory items from the 
    database and renders the inventory template with the list of items.
    
    The route uses the query method all() on the InventoryItem class to retrieve
    all inventory items from the database. The result is a list of InventoryItem
    objects, which is passed to the rendered template as the 'items' variable.
    """
    # Retrieve all inventory items from the database
    items = InventoryItem.query.all()
    # Render the inventory template with the list of items
    return render_template('inventory.html', items=items)

# Route to add a new inventory item
@inventory_bp.route('/add_inventory_item', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'user')
def add_inventory_item():
    """
    This route handles the addition of a new inventory item to the database.
    
    For the GET request:
        - Renders the 'add_inventory_item.html' template, which contains a form for adding a new item.
    
    For the POST request:
        - Retrieves the form data.
        - Creates a new InventoryItem object with the provided name, description, quantity, threshold, and unit.
        - Adds the new item to the database.
        - Commits the session changes.
        - Redirects the user to the inventory list page.
    
    :return: GET request renders the template, POST request redirects to the inventory list
    """
    if request.method == 'GET':
        return render_template('add_inventory_item.html')

    # POST request: Add a new item
    data = request.form
    new_item = InventoryItem(
        name=data['name'],
        description=data.get('description', ''),
        quantity=int(data['quantity']),
        threshold=int(data.get('threshold', 25)),
        unit=data.get('unit', '')
    )
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('inventory.view_inventory'))

# Route to update an inventory item
@inventory_bp.route('/update_inventory_item/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'user')
def update_inventory_item(id):
    """
    This route handles the updating of an inventory item in the database.
    
    For the GET request:
        - Retrieves an inventory item by its ID from the database.
        - Renders the 'update_inventory_item.html' template, which contains a form for updating an item.
    
    For the POST request:
        - Retrieves the form data.
        - Updates the item in the database with the provided name, description, quantity, threshold, and unit.
        - Commits the session changes.
        - Redirects the user to the inventory list page.
    
    :param id: The ID of the item to be updated
    :return: GET request renders the template, POST request redirects to the inventory list
    """
    # Retrieve the inventory item from the database using its ID
    item = InventoryItem.query.get(id)
    
    # If the item is not found, return an error response
    if not item:
        return {"error": "Item not found"}, 404

    # Handle GET request: render the update form with the item data
    if request.method == 'GET':
        return render_template('update_inventory_item.html', item=item)

    # Handle POST request: update the item with form data
    data = request.form
    item.name = data['name']  # Update name
    item.description = data.get('description', '')  # Update description, default to empty string if not provided
    item.quantity = int(data['quantity'])  # Update quantity, convert to integer
    item.threshold = int(data['threshold'])  # Update threshold, convert to integer
    item.unit = data.get('unit', '')  # Update unit, default to empty string if not provided

    # Commit the changes to the database
    db.session.commit()
    
    # Redirect to the inventory list page after successful update
    return redirect(url_for('inventory.view_inventory'))

# Route to delete an inventory item
@inventory_bp.route('/delete_inventory_item/<int:id>', methods=['POST'])
@login_required  # Ensure the user is logged in before performing this action
@role_required('admin', 'user')  # Restrict access to users with the roles 'admin' or 'user'
def delete_inventory_item(id):
    """
    This route handles the deletion of an inventory item from the database.
    
    It is protected by the login_required decorator, which will redirect to the
    login page if the user is not logged in.
    
    It is also protected by the role_required decorator, which will only allow
    users with the role 'admin' or 'user' to access this route.
    
    The route is a POST request, and it retrieves the inventory item from the 
    database using the provided ID. If the item is not found, it returns an 
    error response with a 404 status code.
    
    If the item is found, it deletes the item from the database and commits the
    changes. It then redirects the user to the inventory list page.
    
    :param id: The ID of the item to be deleted
    :return: Redirects to the inventory list page after successful deletion
    """
    # Retrieve the inventory item from the database using its ID
    item = InventoryItem.query.get(id)
    
    # If the item is not found, return an error response
    if not item:
        return {"error": "Item not found"}, 404
    
    # Delete the item from the database
    db.session.delete(item)
    
    # Commit the changes to the database
    db.session.commit()
    
    # Redirect to the inventory list page after successful deletion
    return redirect(url_for('inventory.view_inventory'))
