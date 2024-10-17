from flask import Blueprint, request, jsonify
from app import db
from app.models import InventoryItem
from app.authentication_decorators import login_required, role_required

inventory_api_bp = Blueprint('inventory_api', __name__)

# API to get all inventory items
@inventory_api_bp.route('/api/inventory', methods=['GET'])
@login_required
@role_required('admin', 'user')
def get_all_inventory_items():
    """
    This API endpoint returns a list of all inventory items in the database.

    It is protected by the login_required decorator, which will redirect to the
    login page if the user is not logged in.

    It is also protected by the role_required decorator, which will only allow
    users with the role 'admin' or 'user' to access this endpoint.

    The API endpoint is a GET request, and it retrieves all inventory items from
    the database using the InventoryItem.query.all() method.

    The list of inventory items is then converted into a list of dictionaries,
    where each dictionary represents an inventory item. The dictionary contains
    the following keys:

    - id: The ID of the inventory item
    - name: The name of the inventory item
    - description: The description of the inventory item
    - quantity: The current quantity of the inventory item
    - threshold: The threshold quantity for the inventory item
    - unit: The unit of measurement for the inventory item

    The list of dictionaries is then returned as a JSON response, with a status
    code of 200.
    """
    # Retrieve all inventory items from the database
    items = InventoryItem.query.all()

    # Convert the list of InventoryItem objects into a list of dictionaries
    items_list = [
        {
            # The ID of the inventory item
            'id': item.id,
            # The name of the inventory item
            'name': item.name,
            # The description of the inventory item
            'description': item.description,
            # The current quantity of the inventory item
            'quantity': item.quantity,
            # The threshold quantity for the inventory item
            'threshold': item.threshold,
            # The unit of measurement for the inventory item
            'unit': item.unit
        }
        # Iterate over each item in the list of items
        for item in items
    ]

    # Return the list of dictionaries as a JSON response, with a status code of 200
    return jsonify(items_list), 200

# API to get a single inventory item by ID
@inventory_api_bp.route('/api/inventory/<int:id>', methods=['GET'])
@login_required
@role_required('admin', 'user')
def get_inventory_item_by_id(id):
    """
    This API endpoint is used to retrieve a single inventory item from the
    database by its ID.

    The API endpoint is a GET request, and it retrieves a single inventory item
    from the database using the InventoryItem.query.get() method.

    The InventoryItem object is then converted into a dictionary, which is
    returned as a JSON response, with a status code of 200.

    The dictionary contains the following keys:

    - id: The ID of the inventory item
    - name: The name of the inventory item
    - description: The description of the inventory item
    - quantity: The current quantity of the inventory item
    - threshold: The threshold quantity for the inventory item
    - unit: The unit of measurement for the inventory item

    The API endpoint is protected by the login_required decorator, which will
    redirect to the login page if the user is not logged in.

    The API endpoint is also protected by the role_required decorator, which
    will only allow users with the role 'admin' or 'user' to access this
    endpoint.

    If the item is not found in the database, the API endpoint will return a
    JSON response with an error message, and a status code of 404.
    """
    # Retrieve the inventory item with the given ID from the database
    item = InventoryItem.query.get(id)

    # If the item is not found in the database, return a JSON response with an
    # error message, and a status code of 404
    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Convert the InventoryItem object into a dictionary
    item_data = {
        # The ID of the inventory item
        'id': item.id,
        # The name of the inventory item
        'name': item.name,
        # The description of the inventory item
        'description': item.description,
        # The current quantity of the inventory item
        'quantity': item.quantity,
        # The threshold quantity for the inventory item
        'threshold': item.threshold,
        # The unit of measurement for the inventory item
        'unit': item.unit
    }

    # Return the dictionary as a JSON response, with a status code of 200
    return jsonify(item_data), 200

# API to add a new inventory item
@inventory_api_bp.route('/api/inventory', methods=['POST'])
@login_required
@role_required('admin', 'user')
def add_inventory_item():
    """
    This API endpoint is used to add a new inventory item to the database.

    The API endpoint is a POST request, which means that it will send a JSON
    object to the server with the data for the new inventory item.

    The API endpoint requires the user to be logged in and have the role 'admin'
    or 'user', which is enforced by the login_required and role_required
    decorators.

    The API endpoint expects a JSON object with the following keys:

    - name (str): The name of the inventory item. This is a required field.
    - quantity (int): The current quantity of the inventory item. This is a
      required field.
    - description (str, optional): The description of the inventory item.
      This is an optional field, and it can be left blank.
    - threshold (int, optional): The threshold quantity for the inventory
      item. This is an optional field, and it can be left blank. If it is left
      blank, the default value of 25 will be used.
    - unit (str, optional): The unit of measurement for the inventory item.
      This is an optional field, and it can be left blank. If it is left blank,
      the default value of an empty string will be used.

    If any of the required fields are missing in the data, the API endpoint will
    return a JSON response with an error message, and a status code of 400.

    If the item is successfully added to the database, the API endpoint will
    return a JSON response with a success message and the ID of the new item,
    and a status code of 201.
    """
    # Get the JSON data from the POST request
    data = request.json

    # Check that the required fields are present in the data
    if not data.get('name') or not data.get('quantity'):
        # If the required fields are missing, return an error message and status code 400
        return jsonify({"error": "Name and quantity are required"}), 400

    # Create a new InventoryItem object with the data
    new_item = InventoryItem(
        name=data['name'],
        description=data.get('description', ''),
        quantity=int(data['quantity']),
        threshold=int(data.get('threshold', 25)),
        unit=data.get('unit', '')
    )

    # Add the new item to the database
    db.session.add(new_item)

    # Commit the database changes
    db.session.commit()

    # Return a JSON response with a success message and the ID of the new item, and a status code of 201
    return jsonify({"message": "Inventory item added successfully", "item_id": new_item.id}), 201

# API to update an inventory item
@inventory_api_bp.route('/api/inventory/<int:id>', methods=['PUT'])
@login_required
@role_required('admin', 'user')
def update_inventory_item(id):
    """
    API endpoint to update an inventory item by ID.

    This function updates an existing inventory item in the database based on the provided data.
    It retrieves the item by its ID from the database, checks if the item exists,
    and then updates the name, description, quantity, threshold, and unit fields with the new data.
    Finally, it commits the changes to the database.

    Parameters:
        id (int): The ID of the inventory item to be updated. This is passed as a URL parameter in the route.

    Returns:
        - If the item is found and updated successfully, returns a JSON response with a success message and a status code of 200.
        - If the item is not found, returns a JSON response with an error message and a status code of 404.
    """
    # Retrieve the inventory item from the database using its ID
    item = InventoryItem.query.get(id)

    # Check if the item exists
    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Get the JSON data from the PUT request
    data = request.json

    # Update the item with the new data
    item.name = data.get('name', item.name)  # Update name
    item.description = data.get('description', item.description)  # Update description
    item.quantity = int(data.get('quantity', item.quantity))  # Update quantity
    item.threshold = int(data.get('threshold', item.threshold))  # Update threshold
    item.unit = data.get('unit', item.unit)  # Update unit

    # Commit the changes to the database
    db.session.commit()

    # Return a JSON response with a success message and status code
    return jsonify({"message": "Inventory item updated successfully"}), 200

# API to delete an inventory item
@inventory_api_bp.route('/api/inventory/<int:id>', methods=['DELETE'])
@login_required
@role_required('admin', 'user')
def delete_inventory_item(id):
    """
    API endpoint to delete an inventory item by ID.

    This function takes an ID as a URL parameter and deletes the corresponding
    inventory item from the database.

    Parameters:
        id (int): The ID of the inventory item to be deleted. This is passed as a URL parameter in the route.

    Returns:
        - If the item is found and deleted successfully, returns a JSON response with a success message and a status code of 200.
        - If the item is not found, returns a JSON response with an error message and a status code of 404.

    This function is decorated with the login_required and role_required decorators,
    which ensure that the user is logged in and has the required role to access this
    route. The required roles are 'admin' and 'user'.
    """
    # Retrieve the inventory item from the database using its ID
    # We use the InventoryItem.query.get() method to retrieve the item
    # This method returns an instance of the InventoryItem class if an item
    # with the given ID exists, or None if no such item exists
    item = InventoryItem.query.get(id)

    # Check if the item exists
    # If the item does not exist, return a JSON response with an error message
    # and a status code of 404
    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Delete the item from the database
    # We use the db.session.delete() method to mark the item as deleted
    # This will delete the item from the database when the changes are committed
    db.session.delete(item)

    # Commit the changes to the database
    # We use the db.session.commit() method to commit the changes to the database
    # This will write the changes to the database and make them persistent
    db.session.commit()

    # Return a JSON response with a success message and a status code of 200
    # This indicates that the item was deleted successfully
    return jsonify({"message": "Inventory item deleted successfully"}), 200
