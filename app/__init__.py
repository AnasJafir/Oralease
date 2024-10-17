# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

app = Flask(__name__, template_folder='templates')

app.secret_key = os.environ.get('ENCRYPTION_KEY')

app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookie is sent only over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Reduce risk of XSS attacks
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Optional: session duration in seconds

# Set up the database URI
username = os.environ.get('DB_USERNAME') or 'your_username'
password = os.environ.get('DB_PASSWORD') or 'your_password'
dbname = os.environ.get('DB_NAME') or 'your_db_name'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@localhost/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create a test route for database connection
@app.route('/test_db', methods=['GET'])
def test_db_connection():
    """
    A simple test route for verifying database connection.

    This route is for testing only and is not intended to be part of the actual
    application. It is useful for verifying that the database connection is
    successful and that the app is configured correctly.

    The route executes a simple SQL query to check if the database connection is
    successful. The query is: `SELECT current_database();`

    If the connection is successful, the route will return a JSON response with a
    success message and the name of the current database.

    If the connection fails, the route will return a JSON response with an error
    message and the error details.

    Returns:
        dict: A dictionary containing a message and the current database name.
    """

    try:
        # Execute a simple query
        # The query is: SELECT current_database();
        # The result will be the name of the current database
        result = db.session.execute(text("SELECT current_database();")).scalar()
        
        # Return a JSON response with a success message and the current database name
        return {"message": "Database connection successful!", "current_database": result}

    except Exception as e:
        # If there is an error, return a JSON response with an error message and the error details
        return {"error": str(e), "message": "Database connection failed!"}

# Import routes and apis
from app.patients import patients_bp
from app.appointment import appointments_bp
from app.inventory import inventory_bp
from app.users import auth_bp
from app.treatment_plan import treatment_bp
from app.apis.patients_api import patients_api_bp
from app.apis.appointments_api import appointments_api_bp
from app.apis.inventory_api import inventory_api_bp
from app.apis.treatment_plan_api import treatment_api_bp
from app.apis.users_api import auth_api_bp

app.register_blueprint(patients_bp)
app.register_blueprint(appointments_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(treatment_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(patients_api_bp)
app.register_blueprint(appointments_api_bp)
app.register_blueprint(inventory_api_bp)
app.register_blueprint(treatment_api_bp)
app.register_blueprint(auth_api_bp)

# Create the database tables
with app.app_context():
    db.create_all()
