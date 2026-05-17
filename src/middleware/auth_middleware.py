# Preserves original route function metadata/name
from functools import wraps

# Flask utilities used for session handling and redirects
from flask import session, redirect, url_for, flash

def login_required(route_function):
    # Ensures only logged-in user can access a route.

    @wraps(route_function)
    def wrapper(*args, **kwargs):

        # Retrieve logged-in user from session
        current_user = session.get("current_user")

        # Redirect to login page if no user session exists
        if not current_user:
            flash("Please log in first.")
            return redirect(url_for("login"))
        
        # Continue the original route if authenticated
        return route_function(*args, **kwargs)
    
    return wrapper

def coach_required(route_function):
    # Ensures only logged-in coaches can access a route.

    @wraps(route_function)
    def wrapper(*args, **kwargs):

        # Retrieve logged-in user from session
        current_user = session.get("current_user")

        # Block access if user is not logged in
        if not current_user:
            flash("Please log in.")
            return redirect(url_for("login"))
        
        # Block access if logged-in user is not a coach
        if current_user.get("role") != "Coach":
            flash("You are not authorized to access this page.")
            return redirect(url_for("login"))
        
        # Continue the original route if authorized
        return route_function(*args, **kwargs)
    
    return wrapper

def agent_required(route_function):
    # Ensures only logged-in agents can access a route.

    @wraps(route_function)
    def wrapper(*args, **kwargs):

        # Retrieve logged in user from session
        current_user = session.get("current_user")

        # Block access if user is not logged in
        if not current_user:
            flash("Please log in.")
            return redirect(url_for("login"))
        
        # Block if logged-in user is not an agent
        if current_user.get("role") != "Agent":
            flash("You are not authorized to access this page.")
            return redirect(url_for("login"))
        
        # Continue the original route if authorized
        return route_function(*args, **kwargs)
    
    return wrapper