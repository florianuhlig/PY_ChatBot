from datetime import datetime, timedelta # Add this line at the top
from flask import Flask, render_template, request, redirect, url_for, flash, session
import logging
from config.database import DatabaseConfig
from database import DatabaseFactory
from database.flask_integration import FlaskDatabaseManager
from services.user_service import UserService
from services.auth_service import AuthService
from utils.auth_decorators import login_required, logout_required, get_current_user


# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Session-Konfiguration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # Session läuft nach 24h ab
app.config['SESSION_COOKIE_SECURE'] = False  # Für Development - in Production auf True setzen
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Verhindert XSS-Angriffe


# Database Manager initialisieren
db_config = DatabaseConfig()
db_type, config = db_config.get_database_config()


def create_database():
    """Factory-Funktion für Datenbank-Instanzen"""
    return DatabaseFactory.create_database(db_type, config)


db_manager = FlaskDatabaseManager(create_database)
db_manager.init_app(app)


# Template-Context für alle Templates
@app.context_processor
def inject_user():
    """Macht User-Daten in allen Templates verfügbar"""
    return {'current_user': get_current_user()}


@app.route('/')
def home():
    """Startseite - Weiterleitung je nach Login-Status"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
    """Registrierung - nur für nicht eingeloggte User"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Basis-Validierung
        if not username or not email or not password or not confirm_password:
            flash('Please fill out all fields', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        # Services mit request-lokaler DB-Instanz
        database = db_manager.get_db()
        user_service = UserService(database)

        # User erstellen
        success, errors = user_service.create_user(username, email, password)

        if success:
            flash('Registration successful! Please log in.', 'success')
            logger.info(f"New user registered: {email}")
            return redirect(url_for('login'))
        else:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    """Login - nur für nicht eingeloggte User"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember_me = request.form.get('remember_me')  # Checkbox für "Remember Me"

        if not email or not password:
            flash('Please enter email and password', 'error')
            return redirect(url_for('login'))

        # Services mit request-lokaler DB-Instanz
        database = db_manager.get_db()
        auth_service = AuthService(database)

        # Authentifizierung
        success, user_data, message = auth_service.authenticate(email, password)

        if success:
            # Session setzen
            session['user_id'] = user_data['id']
            session['username'] = user_data['username']
            session['email'] = user_data['email']
            session['login_time'] = datetime.utcnow().isoformat()

            # Permanent session wenn "Remember Me" aktiviert
            if remember_me:
                session.permanent = True

            flash(f'Welcome back, {user_data["username"]}!', 'success')
            logger.info(f"User logged in: {email}")

            # Weiterleitung zu ursprünglich angeforderte Seite (falls vorhanden)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            return redirect(url_for('dashboard'))
        else:
            flash(message, 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Logout - nur für eingeloggte User"""
    user_email = session.get('email')
    username = session.get('username')

    # Session komplett löschen
    session.clear()

    flash(f'Goodbye, {username}! You have been logged out successfully.', 'info')

    if user_email:
        logger.info(f"User logged out: {user_email}")

    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard - nur für eingeloggte User"""
    user = get_current_user()

    # Zusätzliche Dashboard-Daten (optional)
    dashboard_data = {
        'total_users': 'N/A',  # Könnte aus DB geholt werden
        'last_login': session.get('login_time', 'Unknown'),
        'session_expires': 'Never' if session.permanent else '24 hours'
    }

    logger.debug(f"Dashboard accessed by user: {user['email']}")

    return render_template('dashboard.html',
                           user=user,
                           dashboard_data=dashboard_data)


@app.route('/profile')
@login_required
def profile():
    """User Profile - nur für eingeloggte User"""
    user = get_current_user()

    # Hier könnten zusätzliche User-Daten aus der DB geholt werden
    database = db_manager.get_db()
    full_user_data = database.get_user_by_email(user['email'])

    return render_template('profile.html', user=full_user_data)


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Passwort ändern - nur für eingeloggte User"""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not current_password or not new_password or not confirm_password:
            flash('Please fill out all fields', 'error')
            return redirect(url_for('change_password'))

        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(url_for('change_password'))

        # Aktuelles Passwort verifizieren
        user = get_current_user()
        database = db_manager.get_db()
        auth_service = AuthService(database)

        success, _, message = auth_service.authenticate(user['email'], current_password)

        if not success:
            flash('Current password is incorrect', 'error')
            return redirect(url_for('change_password'))

        # Neues Passwort setzen
        from utils.password_utils import PasswordUtils
        new_password_hash = PasswordUtils.hash_password_simple(new_password)

        if database.update_user_password(user['email'], new_password_hash):
            flash('Password changed successfully', 'success')
            logger.info(f"Password changed for user: {user['email']}")
            return redirect(url_for('dashboard'))
        else:
            flash('Failed to change password', 'error')
            return redirect(url_for('change_password'))

    return render_template('change_password.html')


# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    flash('An internal error occurred. Please try again.', 'error')
    return redirect(url_for('home'))


# Session Timeout Check
@app.before_request
def check_session_timeout():
    """Prüft ob Session abgelaufen ist"""
    from datetime import datetime

    if 'user_id' in session:
        # Prüfe ob Session zu alt ist (optional)
        login_time = session.get('login_time')
        if login_time:
            try:
                login_datetime = datetime.fromisoformat(login_time)
                now = datetime.utcnow()

                # Session nach 24h abgelaufen (falls nicht permanent)
                if not session.permanent and (now - login_datetime).total_seconds() > 86400:
                    session.clear()
                    flash('Your session has expired. Please log in again.', 'warning')
                    return redirect(url_for('login'))
            except (ValueError, TypeError):
                # Ungültiger Zeitstempel - Session löschen
                session.clear()
                flash('Invalid session. Please log in again.', 'warning')
                return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)