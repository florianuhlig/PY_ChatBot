from functools import wraps
from flask import session, redirect, url_for, flash, request
import logging

logger = logging.getLogger(__name__)

def login_required(f):
    """
    Decorator to protect routes that require authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or 'email' not in session:
            flash('Please log in to access this page', 'warning')
            logger.info(f"Unauthorized access attempt to {request.endpoint}")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def logout_required(f):
    """
    Decorator for routes that should only be accessible when NOT logged in
    (e.g., login, register pages)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            flash('You are already logged in', 'info')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """
    Helper function to get current user info from session
    """
    if 'user_id' in session:
        return {
            'id': session['user_id'],
            'username': session['username'],
            'email': session['email']
        }
    return None