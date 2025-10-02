from flask import Flask, render_template, request, redirect, url_for, flash

import hashlib

def hash_password(password):
    return hashlib.sha512(password.strip().encode('utf-8')).hexdigest()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    import sqlLite.get as getter
    import sqlLite.set as setter
    import useful.hash as hasher
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form.get('email').strip()
        password = request.form.get('password').strip()
        pwd_confirm = request.form.get('confirm_password').strip()

        if not email or not password or not pwd_confirm or not username:
            flash('Please fill out all fields', 'error')
            return redirect(url_for('register'))

        if password != pwd_confirm:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
        # Hash the password
        hashed_password = hasher.sha512(password.encode('utf-8')).hexdigest()
        try:
            # Call your setter function to add user to DB
            setter.set_login(username, email, hashed_password)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        enter_email = request.form.get('email')
        enter_password = request.form.get('password')
        import hashlib
        import sqlLite.get as getter

        stored_hash = getter.get_password_by_email(enter_email)  # use email here

        if stored_hash is None:
            flash("User not found!")
            return redirect(url_for("login"))

        hash_entered = hashlib.sha512(enter_password.encode('utf-8')).hexdigest()

        if hash_entered == stored_hash:
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
            print("Stored hash:", stored_hash)
            print("Entered hash:", hash_entered)
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard! Login successful."
