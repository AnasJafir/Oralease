Let’s break down the HTML code for the "View Patient" page and explain each section:

1. Document Structure
html
Copier le code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>View Patient</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<!DOCTYPE html>: Declares the document type and version (HTML5).
<html lang="en">: The root element of the HTML document, with the language set to English.
<head>: Contains meta-information about the document.
<meta charset="UTF-8">: Sets the character encoding to UTF-8, supporting a wide range of characters.
<meta name="viewport": Ensures the page is responsive and displays correctly on various devices.
<title>: The title of the web page that appears in the browser tab.
Bootstrap CSS: Links to the Bootstrap framework for styling.
2. Body Section
html
Copier le code
<body>
    <div class="container mt-5">
        <h1 class="mb-4">Patient Details</h1>
        <table class="table table-bordered">
<body>: Contains the content of the page.
<div class="container mt-5">: A Bootstrap container that centers the content and adds margin at the top (mt-5).
<h1>: A heading for the page, displaying "Patient Details."
<table class="table table-bordered">: Creates a table with Bootstrap styling, making it look clean and organized. The table-bordered class adds borders around the table cells.
3. Table Structure
html
Copier le code
<tbody>
    <tr>
        <th>ID</th>
        <td>{{ patient.id }}</td>
    </tr>
    ...
</tbody>
<tbody>: Wraps the body of the table.
<tr>: Defines a table row.
<th>: A header cell that provides a label for the data. In this case, the first row has a header "ID."
<td>: A data cell that contains the actual patient information, represented by {{ patient.id }} (this is a placeholder for a templating engine like Jinja2, which renders data from a server).
4. Actions for Patient Management
html
Copier le code
<div class="d-flex justify-content-between mt-3">
    <a href="/patients" class="btn btn-secondary">Back to Patients List</a>
    <div>
        <a href="/update_patient/{{ patient.id }}" class="btn btn-primary">Edit Patient</a>
        <form action="/delete_patient/{{ patient.id }}" method="POST" style="display:inline;" onsubmit="return confirmDelete()">
            <button type="submit" class="btn btn-danger">Delete Patient</button>
        </form>
    </div>
</div>
Action Buttons: This section provides navigation and management actions for the patient.
<div class="d-flex justify-content-between mt-3">: Uses Bootstrap's Flexbox utilities to create a responsive layout.
<a>: Links to the patients list and edit page.
<form>: Contains a delete button. When clicked, it triggers a POST request to delete the patient. The onsubmit attribute calls the confirmDelete function to ensure the user confirms the action.
5. Scripts
html
Copier le code
<!-- Bootstrap JS + Popper.js -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>

<!-- Delete Confirmation Script -->
<script>
    function confirmDelete() {
        return confirm('Are you sure you want to delete this patient? This action cannot be undone.');
    }
</script>
</body>
</html>
Bootstrap JavaScript: Includes the Bootstrap JavaScript library, enabling interactive components.
Delete Confirmation Script: The confirmDelete function displays a confirmation dialog when the delete button is clicked. If the user confirms, the form submission proceeds; if not, it cancels the submission.
Summary
This HTML code constructs a user-friendly interface for viewing and managing patient details. It leverages Bootstrap for responsive design and styling, making the interface visually appealing. The structure allows for easy display of patient information and provides actions for editing or deleting patient records, all while ensuring that actions are confirmed to prevent accidental deletions.