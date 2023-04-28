from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
app.secret_key = 'replace this with a more secure key'

login_manager = LoginManager()
login_manager.init_app(app)

# Example user database
USERS = {
    'john': {'username': 'john', 'password': 'password', 'name': 'John Doe'},
    'jane': {'username': 'jane', 'password': 'password', 'name': 'Jane Doe'}
}


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    if user_id in USERS:
        user = User()
        user.id = user_id
        return user


@app.route('/')
def index():
    return 'Hello, world!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username]['password'] == password:
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    return 'Welcome to the dashboard, {}!'.format(USERS[current_user.id]['name'])
