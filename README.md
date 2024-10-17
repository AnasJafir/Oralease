**OralEase README**
======================

**Introduction**
---------------

OralEase is a web-based application designed to manage dental clinic operations. The application provides features for patient management, appointment scheduling, treatment planning, and inventory management.

**Getting Started**
-------------------

### Prerequisites

* Python 3.9+
* Flask 3.0.3+
* PostgreSQL 13+
* Bootstrap 5.3.0-alpha1+

### Installation

1. Clone the repository: `git clone https://github.com/AnasJafir/oralease.git`
2. Create a new virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment variables:
	* `ENCRYPTION_KEY`: a secret key for encryption
	* `DB_USERNAME`: PostgreSQL username
	* `DB_PASSWORD`: PostgreSQL password
	* `DB_NAME`: PostgreSQL database name
    * `SECRET_KEY`: secret key
6. Initialize the database: `flask db init`
7. Run the application: `flask run`

**Features**
------------

### Authentication

* Login
* Logout
* Registration

### Authorization

* Role-based access control


### Patient Management

* View patient details
* Edit patient information
* Delete patients
* List all patients

### Appointment Scheduling

* Schedule new appointments
* View upcoming appointments
* Edit appointment details
* Cancel appointments

### Treatment Planning

* Create new treatment plans
* View treatment plans
* Edit treatment plan details
* Delete treatment plans

### Inventory Management

* View inventory items
* Edit inventory item details
* Delete inventory items

**API Endpoints**
-----------------

### Appointments API

* `GET /api/appointments`: retrieve all appointments
* `POST /api/appointments`: create a new appointment
* `GET /api/appointments/<int:appointment_id>`: retrieve an appointment by ID
* `PUT /api/appointments/<int:appointment_id>`: update an appointment
* `DELETE /api/appointments/<int:appointment_id>`: delete an appointment

### Patients API

* `GET /api/patients`: retrieve all patients
* `POST /api/patients`: create a new patient
* `GET /api/patients/<int:patient_id>`: retrieve a patient by ID
* `PUT /api/patients/<int:patient_id>`: update a patient
* `DELETE /api/patients/<int:patient_id>`: delete a patient

### Treatment Plans API

* `GET /api/treatment_plans`: retrieve all treatment plans
* `POST /api/treatment_plans`: create a new treatment plan
* `GET /api/treatment_plans/<int:treatment_plan_id>`: retrieve a treatment plan by ID
* `PUT /api/treatment_plans/<int:treatment_plan_id>`: update a treatment plan
* `DELETE /api/treatment_plans/<int:treatment_plan_id>`: delete a treatment plan

### Inventory Items API

* `GET /api/inventory_items`: retrieve all inventory items
* `POST /api/inventory_items`: create a new inventory item
* `GET /api/inventory_items/<int:inventory_item_id>`: retrieve an inventory item by ID
* `PUT /api/inventory_items/<int:inventory_item_id>`: update an inventory item
* `DELETE /api/inventory_items/<int:inventory_item_id>`: delete an inventory item

### Authentication API Endpoints

* `GET /api/users`: retrieve all users
* `POST /api/users`: create a new user
* `GET /api/users/<int:user_id>`: retrieve a user by ID
* `PUT /api/users/<int:user_id>`: update a user
* `DELETE /api/users/<int:user_id>`: delete a user


**Security**
------------

* Encryption: uses the `cryptography` library for encryption and decryption
* Authentication: uses Flask-Login for user authentication
* Authorization: uses role-based access control (RBAC) for authorization

**Database**
------------

* PostgreSQL 13+
* Database schema is defined in `app/models.py`

**Templates**
-------------

* HTML templates are stored in `app/templates`
* Uses Bootstrap 5.3.0-alpha1+ for styling

**Scripts**
------------

* `confirmDelete.js`: a JavaScript function for confirming deletion of patients and appointments

**Contributing**
---------------

Contributions are welcome! Please submit a pull request with a detailed description of the changes.

**License**
----------

OralEase is licensed under the MIT License.

**Acknowledgments**
------------------

* Flask 3.0.3+ for web framework
* PostgreSQL 13+ for database management
* Bootstrap 5.3.0-alpha1+ for styling

**Contact**
----------

For questions or feedback, please contact us at [https://github.com/AnasJafir](https://github.com/AnasJafir).

or via Email: dr.anas.jafir@gmail.com
