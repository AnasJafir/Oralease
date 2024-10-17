# cli_console.py
import cmd
from app import app, db
from app.models import User, Appointment, InventoryItem, TreatmentPlan, Patient
from app.utils.encryption import decrypt_data


class CrudConsole(cmd.Cmd):
    prompt = 'crud> '  # This is what will show as the prompt in the console

    def do_create_user(self, arg):
        """Create a new user. Usage: create_user <username> <email> <role> <password>"""
        
        # Split the input arguments by spaces
        args = arg.split()
        
        # Check if the number of arguments provided is exactly 4
        if len(args) != 4:
            # Print an error message if the number of arguments is incorrect
            print("Invalid number of arguments. Usage: create_user <username> <email> <role> <password>")
            return
        
        # Unpack the arguments into respective variables
        username, email, role, password = args
        
        # Create a new User object with the provided username, email, and role
        new_user = User(username=username, email=email, role=role)
        
        # Set the password for the new user (assumed to be hashed within this method)
        new_user.set_password(password)
        
        # Add the new User object to the database session
        db.session.add(new_user)
        
        # Commit the session to save the new user to the database
        db.session.commit()
        
        # Print a success message indicating the user was created
        print(f"User {username} created successfully!")

    def do_list_users(self, arg):
        """List all users. Usage: list_users
        
        This method retrieves all users from the database and prints out their
        IDs, usernames, emails, and roles. It doesn't take any arguments.
        
        The User.query.all() is a SQLAlchemy ORM query that retrieves all User
        objects from the database. The for loop iterates over the results and
        prints out each user's details.
        """
        users = User.query.all()
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {user.role}")

    def do_update_user(self, arg):
        """Update a user's email or role. Usage: update_user <id> <email> <role>
        
        This method takes in the user ID, new email, and new role as arguments.
        It first splits the input arguments by spaces into a list and checks
        if the length of the list is exactly 3. If not, an error message is
        printed indicating that the number of arguments provided is incorrect.
        
        If the number of arguments is correct, the method then unpacks the
        arguments into respective variables. The User object with the given
        ID is retrieved from the database using the User.query.get() method.
        If the user is not found, an error message is printed indicating that
        the User with the given ID does not exist.
        
        The email and role of the retrieved User object are then updated with
        the new values provided in the arguments. The db.session.commit()
        method is then called to save the changes to the database.
        
        Finally, a success message is printed to indicate that the User was
        updated successfully.
        """
        args = arg.split()
        if len(args) != 3:
            print("Invalid number of arguments. Usage: update_user <id> <email> <role>")
            return
        user_id, email, role = args
        user = User.query.get(user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return
        user.email = email
        user.role = role
        db.session.commit()
        print(f"User {user_id} updated successfully!")

    def do_delete_user(self, arg):
        """Delete a user. Usage: delete_user <id>

        This method takes in one argument, the ID of the user to be deleted.
        It first strips any leading or trailing whitespace from the argument
        and then uses the User.query.get() method to retrieve a User object
        with the given ID from the database. If the User object is not found,
        an error message is printed indicating that the User with the given
        ID does not exist.

        If the User object is found, the db.session.delete() method is called
        with the User object as argument to mark the User object as deleted in
        the database session. The db.session.commit() method is then called to
        save the changes to the database.

        Finally, a success message is printed to indicate that the User was
        deleted successfully.
        """
        user_id = arg.strip()
        user = User.query.get(user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return
        db.session.delete(user)
        db.session.commit()
        print(f"User {user_id} deleted successfully!")

    def do_exit(self, arg):
        """Exit the CRUD console

        This method is a special method in Python that is automatically called
        when the user types 'exit' in the console. The method takes one argument,
        which is the argument passed to the method when it is called.

        The method does not use the argument passed to it, so it is ignored.

        The method first prints a message to the console to indicate that the
        user is exiting the CRUD console. It then returns a boolean value of
        True to indicate that the console should exit.

        This method is a special method in Python and is not explicitly called
        by the user. It is called automatically when the user types the 'exit'
        command in the console.
        """
        print("Exiting CRUD console.")
        return True

    def do_list_appointments(self, arg):
        """List all appointments. Usage: list_appointments

        This method is a special method in Python that is automatically called
        when the user types 'list_appointments' in the console. The method takes
        one argument, which is the argument passed to the method when it is
        called.

        The method does not use the argument passed to it, so it is ignored.

        The method first retrieves all Appointment objects from the database
        using the Appointment.query.all() method. This method returns a list of
        all Appointment objects in the database.

        The method then iterates over the list of Appointment objects and prints
        out the ID, patient ID, and date of each appointment to the console.

        The print statement uses Python's f-string formatting to format the
        output string. The f-string formatting is a special syntax in Python
        that allows variables to be inserted into strings. The syntax is of the
        form f"{variable_name}" and replaces the variable_name with the value of
        the variable when the string is formatted.

        The f-string formatting is used here to insert the values of the
        appointment ID, patient ID, and date into the output string.

        The final output string is of the form:
            ID: <appointment_id>, Patient ID: <patient_id>, Date: <appointment_date>

        This string is then printed to the console to indicate the list of
        appointments.
        """
        appointments = Appointment.query.all()
        for appt in appointments:
            print(f"ID: {appt.id}, Patient ID: {appt.patient_id}, Date: {appt.appointment_date}")

    def do_create_appointment(self, arg):
        """Create an appointment. Usage: create_appointment <patient_id> <date>

        This method is a special method in Python that is automatically called
        when the user types 'create_appointment' in the console. The method takes
        one argument, which is a string containing two space-separated values:
        the ID of the patient to create an appointment for and the date of the
        appointment.

        The method first splits the argument string into two separate values
        using the split() method. This method splits the string into a list of
        substrings separated by whitespace.

        The method then checks if the length of the list of substrings is not
        equal to 2. If it is not equal to 2, the method prints an error message
        indicating that the number of arguments is invalid. The method then
        returns without doing anything else.

        If the length of the list of substrings is equal to 2, the method
        unpacks the list of substrings into two separate variables: patient_id
        and appointment_date. The patient_id variable is assigned the first
        element of the list and the appointment_date variable is assigned the
        second element of the list.

        The method then creates a new Appointment object with the patient_id and
        appointment_date variables. The Appointment object is created using the
        Appointment() constructor.

        The method then adds the Appointment object to the database using the
        db.session.add() method. This method adds the object to the database
        session.

        Finally, the method commits the database session using the
        db.session.commit() method. This method saves the changes made to the
        database session.

        The final output string is of the form:
            Appointment created successfully!

        This string is then printed to the console to indicate that the
        appointment was created successfully.
        """
        args = arg.split()
        if len(args) != 2:
            print("Invalid number of arguments. Usage: create_appointment <patient_id> <date>")
            return
        patient_id, appointment_date = args
        new_appointment = Appointment(patient_id=patient_id, appointment_date=appointment_date)
        db.session.add(new_appointment)
        db.session.commit()
        print(f"Appointment created successfully!")

    def do_delete_appointment(self, arg):
        """Delete an appointment. Usage: delete_appointment <id>

        This method is a special method in Python that is automatically called
        when the user types 'delete_appointment' in the console. The method takes
        one argument, which is a string containing the ID of the appointment to
        delete.

        The method first strips the argument string of any leading or trailing
        whitespace using the strip() method. This is done to ensure that the ID
        is not accidentally prefixed or suffixed with whitespace.

        The method then retrieves the Appointment object from the database with
        the matching ID using the Appointment.query.get() method. This method
        returns the Appointment object if it is found or None if it is not found.

        If the Appointment object is not found, the method prints an error
        message indicating that the appointment with the given ID was not found.
        The method then returns without doing anything else.

        If the Appointment object is found, the method deletes the appointment
        from the database using the db.session.delete() method. This method
        marks the object as deleted in the database session.

        Finally, the method commits the database session using the
        db.session.commit() method. This method saves the changes made to the
        database session.

        The final output string is of the form:
            Appointment <appointment_id> deleted successfully!

        This string is then printed to the console to indicate that the
        appointment was deleted successfully.
        """
        appointment_id = arg.strip()
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            print(f"Appointment with ID {appointment_id} not found.")
            return
        db.session.delete(appointment)
        db.session.commit()
        print(f"Appointment {appointment_id} deleted successfully!")
    
    # Patient Handling
    def do_create_patient(self, arg):
        """
        Create a new patient. This method takes a single argument which is a
        string of the form '<name>,<dob>,<medical_history>'. The argument is
        split into three parts which are then used to create a new Patient
        object.

        If the argument is invalid or the wrong number of arguments are
        provided, the method prints an error message and returns without
        doing anything else.

        The method first splits the argument string into three parts using the
        split() method. This method splits the string into a list of strings
        using the given separator. The separator in this case is a comma.

        The method then unpacks the list of strings into three variables:
        first_name, last_name, and medical_history. This is done to make the
        code more readable and easier to understand.

        The method then creates a new Patient object with the given data.
        The Patient object's first_name, last_name, and medical_history
        attributes are set to the given values. The medical_history attribute
        is encrypted using the encrypt_data() function before it is stored in
        the database.

        The method then adds the new Patient object to the database session
        using the db.session.add() method. This method adds the object to the
        session so that it can be saved to the database.

        Finally, the method commits the database session using the
        db.session.commit() method. This method saves the changes made to the
        database session.

        The final output string is of the form:
            Patient <name> created successfully!

        This string is then printed to the console to indicate that the
        patient was created successfully.
        """
        args = arg.split(',')
        if len(args) != 3:
            print("Invalid number of arguments. Usage: create_patient <name> <dob> <medical_history>")
            return
        first_name, last_name, medical_history = args
        new_patient = Patient(first_name=first_name.strip(), last_name=last_name.strip(), medical_history=medical_history.strip())
        db.session.add(new_patient)
        db.session.commit()
        print(f"Patient {first_name} created successfully!")

    def do_list_patients(self, arg):
        """List all patients. Usage: list_patients

        This method is a special method in Python that is automatically called
        when the user types 'list_patients' in the console. The method takes no
        arguments.

        The method first queries the database for all Patient objects using the
        Patient.query.all() method. This method returns a list of Patient
        objects.

        The method then loops over each Patient object in the list and prints a
        string containing the patient's ID, first name, last name, and medical
        history. The medical history is decrypted using the decrypt_data()
        function before it is printed.

        The final output string is of the form:
            ID: <patient_id>, Name: <first_name>, Surname: <last_name>, Medical History: <medical_history>

        This string is then printed to the console to indicate that the
        appointment was created successfully.
        """
        patients = Patient.query.all()
        for patient in patients:
            print(f"ID: {patient.id}, Name: {patient.first_name}, Surname: {patient.last_name}, Medical History: {decrypt_data(patient.medical_history)}")

    def do_update_patient(self, arg):
        """Update a patient's information. Usage: update_patient <id> <name> <dob> <medical_history>

        This method is a special method in Python that is automatically called
        when the user types 'update_patient' in the console. The method takes a
        single argument, a string containing the patient's ID, name, date of
        birth, and medical history separated by commas.

        The method first splits the argument string into a list of four strings
        using the split() method with a comma as the separator. If the length of
        the list is not four, the method prints an error message and returns.

        The method then unpacks the list into four variables: patient_id, name,
        dob, and medical_history.

        The method then queries the database for a Patient object with the
        given ID using the Patient.query.get() method. If the patient is not
        found, the method prints an error message and returns.

        The method then updates the patient's name, date of birth, and medical
        history attributes with the provided values, stripping any whitespace
        from the strings using the strip() method.

        The method then commits the changes to the database using the
        db.session.commit() method.

        The method then prints a success message to the console to indicate
        that the patient was updated successfully.
        """
        args = arg.split(',')
        if len(args) != 4:
            print("Invalid number of arguments. Usage: update_patient <id> <name> <dob> <medical_history>")
            return
        patient_id, name, dob, medical_history = args
        patient = Patient.query.get(patient_id)
        if not patient:
            print(f"Patient with ID {patient_id} not found.")
            return
        patient.name = name.strip()
        patient.dob = dob.strip()
        patient.medical_history = medical_history.strip()
        db.session.commit()
        print(f"Patient {patient_id} updated successfully!")

    def do_delete_patient(self, arg):
        """Delete a patient. Usage: delete_patient <id>

        This method is a special method in Python that is automatically called
        when the user types 'delete_patient' in the console. The method takes a
        single argument, a string containing the patient's ID.

        The method first strips any leading or trailing whitespace from the
        argument string using the strip() method. This is done to ensure that the
        ID is not accidentally prefixed or suffixed with whitespace.

        The method then retrieves the Patient object from the database with the
        matching ID using the Patient.query.get() method. This method returns the
        Patient object if it is found or None if it is not found.

        If the Patient object is not found, the method prints an error message
        indicating that the patient with the given ID was not found. The method
        then returns without doing anything else.

        If the Patient object is found, the method deletes the patient from the
        database using the db.session.delete() method. This method marks the
        object as deleted in the database session.

        Finally, the method commits the database session using the
        db.session.commit() method. This method saves the changes made to the
        database session.

        The final output string is of the form:
            Patient <patient_id> deleted successfully!

        This string is then printed to the console to indicate that the patient
        was deleted successfully.
        """
        patient_id = arg.strip()
        patient = Patient.query.get(patient_id)
        if not patient:
            print(f"Patient with ID {patient_id} not found.")
            return
        db.session.delete(patient)
        db.session.commit()
        print(f"Patient {patient_id} deleted successfully!")

    # Inventory Handling
    def do_create_inventory_item(self, arg):
        """
        Create a new inventory item. Usage: create_inventory_item <name> <quantity> <description>

        This method is a special method in Python that is automatically called
        when the user types 'create_inventory_item' in the console. The method
        takes a single argument, a string containing the name, quantity, and
        description of the inventory item to be created.

        The method first splits the argument string into three parts using the
        split() method. This method splits the string into a list of strings
        using the given separator. The separator in this case is a comma.

        The method then unpacks the list of strings into three variables:
        name, quantity, and description. This is done to make the code more
        readable and easier to understand.

        The method then creates a new InventoryItem object with the given data.
        The InventoryItem object's name, quantity, and description attributes
        are set to the given values. The quantity attribute is converted to an
        integer using the int() function before it is stored in the database.

        The method then adds the new InventoryItem object to the database
        session using the db.session.add() method. This method adds the object
        to the session so that it can be saved to the database.

        Finally, the method commits the database session using the
        db.session.commit() method. This method saves the changes made to the
        database session.

        The final output string is of the form:
            Inventory item <name> created successfully!

        This string is then printed to the console to indicate that the
        inventory item was created successfully.
        """
        args = arg.split(',')
        if len(args) != 3:
            print("Invalid number of arguments. Usage: create_inventory_item <name> <quantity> <description>")
            return
        name, quantity, description = args
        new_item = InventoryItem(name=name.strip(), quantity=int(quantity.strip()), description=description.strip())
        db.session.add(new_item)
        db.session.commit()
        print(f"Inventory item {name} created successfully!")

    def do_list_inventory(self, arg):
        """List all inventory items. Usage: list_inventory

        This method prints out all the inventory items in the database.
        
        It first queries the database for all InventoryItem objects using the
        InventoryItem.query.all() method. This method returns a list of all
        InventoryItem objects in the database.

        It then loops over this list of InventoryItem objects and prints out
        the ID, name, quantity, and description of each item using the print()
        method.

        The output string is of the form:
            ID: <id>, Name: <name>, Quantity: <quantity>, Description: <description>

        This string is then printed to the console to indicate that the
        inventory item was listed successfully.
        """
        items = InventoryItem.query.all()
        for item in items:
            print(f"ID: {item.id}, Name: {item.name}, Quantity: {item.quantity}, Description: {item.description}")

    def do_update_inventory_item(self, arg):
        """
        Update an inventory item. Usage: update_inventory_item <id> <name> <quantity> <description>

        This method updates an existing inventory item in the database.

        It takes a string argument of the form:
            <id>, <name>, <quantity>, <description>

        It first splits this string into its constituent parts using the
        split() method.

        If the resulting list does not have exactly 4 elements, it prints an
        error message to the console and returns.

        Otherwise, it retrieves an InventoryItem object from the database
        using the InventoryItem.query.get() method, passing the ID as the
        argument.

        If the object is not found, it prints an error message to the console
        and returns.

        It then updates the name, quantity, and description of the item using
        the setattr() method.

        Finally, it commits the session changes to the database using the
        db.session.commit() method.

        The final output string is of the form:
            Inventory item <id> updated successfully!

        This string is then printed to the console to indicate that the
        inventory item was updated successfully.
        """
        args = arg.split(',')
        if len(args) != 4:
            print("Invalid number of arguments. Usage: update_inventory_item <id> <name> <quantity> <description>")
            return
        item_id, name, quantity, description = args
        item = InventoryItem.query.get(item_id)
        if not item:
            print(f"Inventory item with ID {item_id} not found.")
            return
        setattr(item, 'name', name.strip())
        setattr(item, 'quantity', int(quantity.strip()))
        setattr(item, 'description', description.strip())
        db.session.commit()
        print(f"Inventory item {item_id} updated successfully!")

    def do_delete_inventory_item(self, arg):
        """
        Delete an inventory item. Usage: delete_inventory_item <id>

        This method is a special method in Python that is automatically called
        when the user types 'delete_inventory_item' in the console. The method
        takes a single argument, a string containing the ID of the inventory
        item to delete.

        The method first strips any leading or trailing whitespace from the
        argument string using the strip() method. This is done to ensure that the
        ID is not accidentally prefixed or suffixed with whitespace.

        The method then retrieves an InventoryItem object from the database with
        the matching ID using the InventoryItem.query.get() method. This method
        returns the InventoryItem object if it is found or None if it is not
        found.

        If the InventoryItem object is not found, the method prints an error
        message to the console indicating that the inventory item with the given
        ID was not found. The method then returns without doing anything else.

        If the InventoryItem object is found, the method deletes the item from
        the database using the db.session.delete() method. This method marks the
        object as deleted in the database session.

        Finally, the method commits the database session using the
        db.session.commit() method. This method saves the changes made to the
        database session.

        The final output string is of the form:
            Inventory item <id> deleted successfully!

        This string is then printed to the console to indicate that the
        inventory item was deleted successfully.
        """
        item_id = arg.strip()
        item = InventoryItem.query.get(item_id)
        if not item:
            print(f"Inventory item with ID {item_id} not found.")
            return
        db.session.delete(item)
        db.session.commit()
        print(f"Inventory item {item_id} deleted successfully!")

    # Treatment Plan Handling
    def do_create_treatment_plan(self, arg):
        """
        This method creates a new treatment plan for a patient.
        The argument should be in the format: <patient_id>, <status>
        """
        # Split the argument string into a list of substrings separated by commas
        args = arg.split(',')
        
        # Check if the number of arguments is not equal to 2
        if len(args) != 2:
            print("Invalid number of arguments. Usage: create_treatment_plan <patient_id> <status>")
            return
        
        # Unpack the arguments into patient_id and status
        # The strip() method is used to remove any leading or trailing whitespace from the strings
        patient_id, status = args
        
        # Create a new TreatmentPlan object with the provided patient_id and status
        # The patient_id is set to the provided patient_id, stripped of any leading or trailing whitespace
        # The status is set to the provided status, stripped of any leading or trailing whitespace
        new_plan = TreatmentPlan(patient_id=patient_id.strip(), status=status.strip())
        
        # Add the new treatment plan to the database session
        # The db.session.add() method adds the object to the database session
        db.session.add(new_plan)
        
        # Commit the session to save the new treatment plan to the database
        # The db.session.commit() method saves the changes made to the database session
        db.session.commit()
        
        # Print a success message indicating that the treatment plan was created
        # The message includes the patient_id of the treatment plan
        print(f"Treatment plan for patient ID {patient_id} created successfully!")

    def do_list_treatment_plans(self, arg):
        """
        List all treatment plans. Usage: list_treatment_plans

        This method retrieves all treatment plans from the database and prints
        their details in a formatted manner. The details include the treatment
        plan's ID, the associated patient ID, and the current status of the treatment plan.
        """

        # Query the database to retrieve all treatment plans
        plans = TreatmentPlan.query.all()

        # Loop through each treatment plan in the retrieved list
        for plan in plans:
            # Print the details of the treatment plan
            # The details include the treatment plan's ID, patient ID, and status
            print(f"ID: {plan.id}, Patient ID: {plan.patient_id}, Status: {plan.status}")

    def do_update_treatment_plan(self, arg):
        """
        Update a treatment plan. Usage: update_treatment_plan <id> <details> <date>

        This method updates the status of an existing treatment plan in the database.
        It expects a single argument, a string that contains the treatment plan ID,
        the new details, and the date, separated by commas.
        """
        # Split the argument string into a list of strings using the comma as a separator
        args = arg.split(',')
        
        # Check if the number of arguments is exactly 3 (id, details, date)
        if len(args) != 3:
            # If not, print an error message and return from the method
            print("Invalid number of arguments. Usage: update_treatment_plan <id> <details> <date>")
            return
        
        # Unpack the arguments into plan_id and status
        plan_id, status = args

        # Query the database for a TreatmentPlan object with the given ID
        plan = TreatmentPlan.query.get(plan_id)
        
        # Check if the treatment plan exists
        if not plan:
            # If the treatment plan does not exist, print an error message and return
            print(f"Treatment plan with ID {plan_id} not found.")
            return
        
        # Update the status of the treatment plan with the provided status, removing any leading or trailing whitespace
        plan.status = status.strip()
        
        # Commit the changes to the database to save the updated status
        db.session.commit()
        
        # Print a success message to indicate that the treatment plan was updated successfully
        print(f"Treatment plan {plan_id} updated successfully!")

    def do_delete_treatment_plan(self, arg):
        """
        Delete a treatment plan. Usage: delete_treatment_plan <id>

        This method takes a single argument, the ID of the treatment plan to be
        deleted. It retrieves the treatment plan with the given ID from the
        database and deletes it if it exists. If the treatment plan does not
        exist, it prints an error message and returns.

        The method first strips any leading or trailing whitespace from the
        argument to ensure that it is a valid ID.

        It then queries the database using the query.get() method to retrieve
        the treatment plan with the given ID. If the treatment plan does not
        exist, the query.get() method returns None, and the method prints an error
        message and returns.

        If the treatment plan exists, the method uses the db.session.delete()
        method to delete the treatment plan from the database. The
        db.session.commit() method is then used to commit the changes to the
        database and save the deletion.

        Finally, the method prints a success message to indicate that the
        treatment plan was deleted successfully.
        """
        # Strip any leading or trailing whitespace from the argument
        plan_id = arg.strip()
        
        # Query the database for a TreatmentPlan object with the given ID
        plan = TreatmentPlan.query.get(plan_id)
        
        # Check if the treatment plan exists
        if not plan:
            # If the treatment plan does not exist, print an error message and return
            print(f"Treatment plan with ID {plan_id} not found.")
            return
        
        # Delete the treatment plan from the database
        db.session.delete(plan)
        
        # Commit the changes to the database to save the deletion
        db.session.commit()
        
        # Print a success message to indicate that the treatment plan was deleted successfully
        print(f"Treatment plan {plan_id} deleted successfully!")
        

    def do_exit(self, arg):
        """
        Exit the CRUD console

        This method is a special method in Python that is automatically called
        when the user types 'exit' in the console. The method takes one argument,
        which is the argument passed to the method when it is called.

        The method does not use the argument passed to it, so it is ignored.

        The method first prints a message to the console to indicate that the
        user is exiting the CRUD console. It then returns a boolean value of
        True to indicate that the console should exit.

        This method is a special method in Python and is not explicitly called
        by the user. It is called automatically when the user types the 'exit'
        command in the console.
        """
        # Print a message to the console indicating that the user is exiting
        print("Exiting CRUD console.")
        
        # Return True to signal that the console should exit
        return True

    def default(self, line):
        """
        Handle unknown commands.

        This method is a special method in Python that is called when the user
        enters a command that does not match any of the commands defined in the
        class. The method takes one argument, which is the line of text entered
        by the user.

        The method prints a message to the console indicating that the command
        is unknown, and does not return a value.

        The purpose of this method is to provide a way for the class to handle
        commands that are not explicitly defined in the class. This allows the
        class to handle a wider range of commands than it would otherwise be
        able to.

        This method is a special method in Python and is not explicitly called
        by the user. It is called automatically when the user types a command
        that is not recognized by the class.
        """
        # Print a message to the console indicating that the command is unknown
        print(f"Unknown command: {line}")
    
    def do_help(self, arg):
        """
        List available commands or provide help on a specific command.
        
        Usage: help <command>
        
        If the user provides an argument, this method will attempt to provide
        help on the specified command by printing the docstring for the
        corresponding method. If the user does not provide an argument, the
        method will print a list of all available commands.
        
        The method first checks if the user provided an argument. If they did,
        the method attempts to find a method in the class whose name matches
        the argument. If such a method exists, the method prints the docstring
        for the method. If such a method does not exist, the method prints a
        message indicating that no help is available for the command.
        
        If the user did not provide an argument, the method prints a list of all
        available commands. The list of commands is stored in the 'commands'
        list, which is a list of strings. Each string in the list is the name of
        a command without the 'do_' prefix. For example, the command 'exit' is
        represented in the list as 'exit', not 'do_exit'.
        
        The method then prints a message to the console indicating that the
        list of commands is available, and prints each command in the list
        individually.
        """
        if arg:
            # Attempt to find a method in the class whose name matches the
            # argument
            cmd = 'do_' + arg.strip()
            if hasattr(self, cmd):
                # If such a method exists, print the docstring for the method
                print(getattr(self, cmd).__doc__)
            else:
                # If such a method does not exist, print a message indicating
                # that no help is available for the command
                print(f"No help available for command: {arg}")
        else:
            # List of commands without the 'do_' prefix
            commands = [
                'create_user',
                'list_users',
                'update_user',
                'delete_user',
                'exit',
                'list_appointments',
                'create_appointment',
                'delete_appointment',
                'create_patient',
                'list_patients',
                'update_patient',
                'delete_patient',
                'create_inventory_item',
                'list_inventory',
                'update_inventory_item',
                'delete_inventory_item',
                'create_treatment_plan',
                'list_treatment_plans',
                'update_treatment_plan',
                'delete_treatment_plan',
            ]
            # Print a message to the console indicating that the list of commands
            # is available
            print("Available commands:")
            # Print each command in the list individually
            for command in commands:
                print(f" - {command}")

if __name__ == '__main__':
    with app.app_context():
        CrudConsole().cmdloop()
