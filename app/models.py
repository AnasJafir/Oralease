# app/models.py

from app import db
from datetime import datetime, timedelta
from sqlalchemy import LargeBinary
from app.utils.encryption import encrypt_data, decrypt_data
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """
        Set the password for the user.

        :param password: the password to set

        Note: We use Werkzeug's generate_password_hash function to hash the password.
        The hashed password is then stored in the database.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verify a password against the stored hash.

        This function takes a password as an argument,
        hashes it using the same algorithm used to hash the password
        when it was first created (Werkzeug's generate_password_hash),
        and then compares the resulting hash with the stored hash
        to see if they match.

        If the two hashes match, then the password is correct,
        and the function returns True. Otherwise, it returns False.

        :param password: password to check
        :return: True if the password matches the stored hash, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        """
        Return a string representation of the User object.

        This method returns a string that represents the User object.
        This string is used when the User object is printed out,
        such as when it is included in a list comprehension.

        The string is formatted as "<User username>",
        where 'username' is the username of the User object.

        This method is useful for debugging,
        as it allows us to easily see the contents of the User object.

        :return: A formatted string with the user's username
        """
        return f"<User {self.username}>"

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False, index=True)
    contact_number = db.Column(db.LargeBinary, nullable=False)  # Store encrypted data as LargeBinary
    email = db.Column(db.LargeBinary, unique=True, nullable=False, index=True)  # Store encrypted data as LargeBinary
    medical_history = db.Column(db.LargeBinary, nullable=True)  # Store encrypted data as LargeBinary
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, first_name, last_name, date_of_birth, contact_number, email, medical_history):
        """
        Initialize a Patient object with the given data.

        :param first_name: The first name of the patient
        :param last_name: The last name of the patient
        :param date_of_birth: The date of birth of the patient
        :param contact_number: The contact number of the patient
        :param email: The email address of the patient
        :param medical_history: The medical history of the patient

        This function first sets the first name, last name, date of birth,
        contact number, email address, and medical history of the patient
        to the given values. It then encrypts the contact number, email address,
        and medical history using the provided encryption function, and
        sets the encrypted values as the contact number, email, and medical
        history of the patient.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth

        # Encrypt contact number
        self.contact_number = encrypt_data(contact_number)  # Ensure this is a string

        # Encrypt email address
        self.email = encrypt_data(email)  # Ensure this is a string

        # Encrypt medical history
        self.medical_history = encrypt_data(medical_history)  # Ensure this is a string

    @property
    def decrypted_contact_number(self):
        """
        Return the decrypted contact number of the patient.

        This property is a getter that decrypts the contact number
        that was previously encrypted and stored in the database.

        The contact number is stored as a LargeBinary in the database.
        When we retrieve it, we need to decrypt it using the
        decrypt_data function from the encryption module.

        The decrypt_data function takes in the encrypted contact number
        as a bytes object and returns the decrypted contact number
        as a string.

        We return the decrypted contact number as a string.

        :return: The decrypted contact number of the patient as a string
        """
        return decrypt_data(self.contact_number)  # Decrypt contact number

    @property
    def decrypted_email(self):
        """
        This property is a getter that decrypts the email address
        of the patient that was previously encrypted and stored in the database.

        The email address is stored as a LargeBinary in the database,
        which is a type that can store binary data, such as encrypted strings.

        When we retrieve the email address from the database,
        it is in its encrypted form, which is a bytes object.
        To decrypt it, we use the decrypt_data function from the encryption module.

        The decrypt_data function takes in the encrypted email address
        as a bytes object and returns the decrypted email address
        as a string.

        We return the decrypted email address as a string,
        which can then be used in our application.

        :return: The decrypted email address of the patient as a string
        """
        # Retrieve the encrypted email address from the database
        encrypted_email = self.email

        # Decrypt the email address using the decrypt_data function
        decrypted_email = decrypt_data(encrypted_email)

        # Return the decrypted email address as a string
        return decrypted_email

    @property
    def decrypted_medical_history(self):
        """
        This property is a getter that decrypts the medical history of the patient
        that was previously encrypted and stored in the database.

        The medical history is stored as a LargeBinary in the database, which is a
        type that can store binary data, such as encrypted strings.

        When we retrieve the medical history from the database, it is in its
        encrypted form, which is a bytes object. To decrypt it, we use the
        decrypt_data function from the encryption module.

        The decrypt_data function takes in the encrypted medical history as a
        bytes object and returns the decrypted medical history as a string.

        We return the decrypted medical history as a string, which can then be
        used in our application.

        :return: The decrypted medical history of the patient as a string
        """
        # Retrieve the encrypted medical history from the database
        encrypted_medical_history = self.medical_history

        # Decrypt the medical history using the decrypt_data function
        decrypted_medical_history = decrypt_data(encrypted_medical_history)

        # Return the decrypted medical history as a string
        return decrypted_medical_history

    def __repr__(self):
        """
        The repr method returns a string representation of the object.

        This method is a special method in Python that returns a string
        representation of the object. It is typically used for debugging
        purposes.

        The string representation of the object will include the name of the
        class and the values of the objects' key attributes. In this case,
        the string representation will include the first name, last name,
        and ID of the patient.

        :return: A string representation of the object
        """
        return f"<Patient {self.first_name} {self.last_name} (id={self.id})>"



class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    appointment_date = db.Column(db.DateTime, nullable=False, index=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    patient = db.relationship('Patient', backref='appointments')

    def __repr__(self):
        """
        The repr method returns a string representation of the object.

        This method is a special method in Python that returns a string
        representation of the object. It is typically used for debugging
        purposes.

        The string representation of the object will include the ID of the
        appointment and the ID of the patient it is associated with.

        In this case, the string representation will be in the format:
            <Appointment <appointment_id> for Patient <patient_id>>

        For example, if the appointment ID is 123 and the patient ID is 456,
        the string representation will be:
            <Appointment 123 for Patient 456>

        :return: A string representation of the object
        """
        return f"<Appointment {self.id} for Patient {self.patient_id}>"

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    threshold = db.Column(db.Integer, default=25)  # Default threshold for reminders
    unit = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        """
        The repr method is a special method in Python that returns a string
        representation of the object. It is typically used for debugging
        purposes.

        In this case, the repr method returns a string representation of the
        InventoryItem object. The string representation will include the name
        of the inventory item.

        The string representation will be in the format:
            <InventoryItem <inventory_item_name>>

        For example, if the inventory item name is "Dental Floss", the string
        representation will be:
            <InventoryItem Dental Floss>

        The purpose of the repr method is to provide a string representation of
        the object that is useful for debugging. It is typically used to print
        the object to the console or to include it in a log message.

        The repr method should return a string that is a valid Python expression.
        This allows the string representation of the object to be used to create
        a new object that is equivalent to the original object.

        The repr method is also used to create a string representation of the
        object that can be used in a dictionary or set.

        :return: A string representation of the object
        """
        return f"<InventoryItem {self.name}>"



# models.py

class TreatmentPlan(db.Model):
    __tablename__ = 'treatment_plans'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, index=True)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment_details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending', index=True)  # Status could be Pending, Ongoing, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    patient = db.relationship('Patient', backref='treatment_plans')

    def __repr__(self):
        """
        The repr method is a special method in Python that returns a string
        representation of the object. It is typically used for debugging
        purposes.

        In this case, the repr method returns a string representation of the
        TreatmentPlan object. The string representation will include the ID
        of the patient associated with this treatment plan.

        The string representation will be in the format:
            <TreatmentPlan for Patient <patient_id>>

        For example, if the patient ID is 123, the string representation will be:
            <TreatmentPlan for Patient 123>

        The purpose of the repr method is to provide a string representation of
        the object that is useful for debugging. It is typically used to print
        the object to the console or to include it in a log message.

        The repr method should return a string that is a valid Python expression.
        This allows the string representation of the object to be used to create
        a new object that is equivalent to the original object.

        The repr method is also used to create a string representation of the
        object that can be used in a dictionary or set.

        :return: A string representation of the object
        """
        # The return statement constructs a string using an f-string. The f-string
        # allows for the inclusion of the patient_id attribute directly within the
        # string by placing it inside curly braces. This dynamically inserts the value
        # of patient_id into the string at runtime.
        return f"<TreatmentPlan for Patient {self.patient_id}>"
