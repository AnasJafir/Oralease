

Based on the provided code snippet from `app/templates/add_patient.html`, there are two JavaScript scripts present:

### 1. Bootstrap Bundle Script

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
```

This script includes the Bootstrap JavaScript bundle, which provides functionality for various Bootstrap components, such as dropdowns, modals, and tooltips. The `.bundle` version includes Popper.js, which is a dependency for some Bootstrap components.

### 2. Form Validation Script

```javascript
// Bootstrap validation example
(function () {
    'use strict'
    const forms = document.querySelectorAll('.needs-validation')
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }
            form.classList.add('was-validated')
        }, false)
    })
})();
```

This script is an example of Bootstrap's form validation. It selects all forms with the class `.needs-validation` and adds an event listener to each form's submit event. When a form is submitted, the script checks if the form is valid using the `checkValidity()` method. If the form is not valid, it prevents the default form submission behavior and stops the event propagation. Additionally, it adds the class `was-validated` to the form, which can be used to style the form and provide visual feedback to the user.

In the context of the `add_patient.html` file, this script is used to validate the patient form before submitting it. The form has the class `.needs-validation`, and the script will check the form's validity when the "Add Patient" button is clicked.