from flask import Flask
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/profile')
def login_success():
    return render_template('mainhome.html')


username_password = {('admin', 'admin')}
user_info = []


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'], request.form['password']) not in username_password:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('login_success'))
    return render_template('Desktop2.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        user_info.append((request.form['username'], request.form['password'],
                          request.form['email'], request.form['name']))
        username_password.add((request.form['username'], request.form['password']))
        return redirect(url_for('login'))
    return render_template('Desktop3.html', error=error)


if __name__ == '__main__':
    app.run()
