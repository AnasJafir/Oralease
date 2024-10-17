# auth_decorators.py
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """
    Checks if the user is logged in before allowing access to a route.

    The user is considered "logged in" if their user_id is stored in the session.
    If the user is not logged in, they are redirected to the login page with a warning message.

    :param f: The function that requires login.
    :return: The wrapped function.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in (i.e. if the user_id is stored in the session)
        if 'user_id' not in session:
            # If the user is not logged in, flash a warning message and redirect to the login page
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('auth.login'))
        # If the user is logged in, allow access to the route
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """
    Checks if the user has the specified role(s) before allowing access to a route.

    If the user does not have the specified role(s), they are redirected to the index page with a warning message.

    The roles parameter is a variable argument list, meaning that it can be any number of arguments. This allows the
    programmer to specify multiple roles that are required to access a route.

    :param *roles: The roles that are required to access the route.
    :return: The wrapped function.
    """
    def decorator(f):
        """
        Checks if the user has the specified role(s) before allowing access to a route.

        If the user does not have the specified role(s), they are redirected to the index page with a warning message.

        :param f: The function that requires a role.
        :return: The wrapped function.
        """
        @wraps(f)
        @login_required  # Ensure that the user is logged in before checking roles
        def decorated_function(*args, **kwargs):
            """
            Decorator function that checks if a logged-in user has the required role(s) to access a route.

            This function first ensures that the user is logged in by chaining with the login_required decorator.
            Once confirmed logged in, it checks if the user's role is one of the roles required to access the route.
            If the user does not have any of the required roles, they are shown a warning message and redirected
            to the index page. Otherwise, the user is granted access to the route.

            :param *args: Positional arguments passed to the route.
            :param **kwargs: Keyword arguments passed to the route.
            :return: The result of the original route function if the user has the required role(s).
            """
            # Retrieve the role of the logged-in user from the session
            user_role = session.get('role')

            # Check if the user's role is not in the list of roles required for this route
            if user_role not in roles:
                # Display a warning message to the user indicating insufficient privileges
                flash('Access denied. Insufficient privileges.', 'danger')

                # Redirect the user to the index page as they lack the required role
                return redirect(url_for('auth.index'))

            # If the user's role is in the list, proceed to call the original route function
            return f(*args, **kwargs)
        return decorated_function
    return decorator
