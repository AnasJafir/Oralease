This HTML template is designed to display detailed information about a patient, including their personal details, appointments, and treatment plans, in your dental clinic management system. The layout uses Bootstrap and includes icons from Bootstrap Icons for a visually appealing, user-friendly design.

Key Features:
Patient Information Section: Displays the patient's name, date of birth, contact details, and medical history. It uses icons for each field for better visualization.
Appointments Section: Shows a list of the patient's appointments, each with a date, time, and description.
Treatment Plans Section: Lists the patient's treatment plans with a diagnosis and treatment details.
Stylish Design: Uses a custom color scheme with CSS variables, providing consistency in the UI. Bootstrap's card component is used to group information neatly.
Code Breakdown:
Bootstrap Integration: The template imports Bootstrap CSS and Bootstrap Icons to provide responsive design and styled components.
Custom CSS: The custom styles are added through a <style> block that defines color variables and enhances the appearance of elements like the patient info, appointment, and treatment plan details.
Data Display: The template uses the Jinja templating engine to dynamically loop through patients_data, displaying relevant information about each patient, their appointments, and their treatment plans.
Fallbacks: If a patient has no appointments or treatment plans, a message is displayed.