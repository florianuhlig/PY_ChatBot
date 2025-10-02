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
    import standard.getter as st_getter
    import sqlLite.set as setter

    if request.method == 'POST':
        username = request.form['username']
        email = request.form.get('email')
        password = request.form.get('password')
        pwd_confirm = request.form.get('confirm_password')

        if not email or not password or not pwd_confirm or not username:
            flash('Please fill out all fields', 'error')
            return redirect(url_for('register'))

        if password != pwd_confirm:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        try:
            if st_getter.get_validate_email(email):
                setter.set_login(username, email, password)
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Invalid email format', 'error')
                return redirect(url_for('register'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('register'))
    # For GET-requests:
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        enter_email = request.form.get('email')
        enter_password = request.form.get('password')
        import hashlib
        import sqlLite.get as getter
        import standard.getter as st_getter

        stored_hash = getter.get_password_by_email(enter_email)  # use email here

        if stored_hash is None:
            flash("User not found!")
            return redirect(url_for("login"))

        hash_entered = st_getter.get_password_hash(enter_password)

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
    #return "Welcome to the dashboard! Login successful."
    return render_template('dashboard.html')
