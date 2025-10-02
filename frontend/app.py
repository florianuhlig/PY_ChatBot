from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        enter_email = request.form.get('email')
        enter_password = request.form.get('password')
        import sqlLite.get as getter
        import useful.hash as hasher
        pwd = getter.get_password_by_email(enter_email)
        password = hasher.get_password_hash(enter_password)
        if password == pwd:
            return redirect(url_for('dashboard'))
        elif password == None:
            flash("User not found!")
            return redirect(url_for("login"))
        elif pwd == None:
            flash("Password not found!")
            return redirect(url_for("login"))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard! Login successful."
