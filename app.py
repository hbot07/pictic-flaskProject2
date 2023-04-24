import os
import random

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


@app.route('/gallery')
def gallery():
    images = []
    gallery_length = 0
    for filename in os.listdir('static/uploads'):
        if gallery_length > 49:
            break
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
            title, username = filename.split('_')[:-1]
            images.append({'filename': filename, 'title': title, 'username': username})
            gallery_length += 1
    return render_template('gallery.html', images=images)


app.config['UPLOAD_FOLDER'] = 'static/uploads/'


@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    image = request.files['image']
    username = request.form['username']
    title = request.form['title']
    ext = os.path.splitext(image.filename)[1]
    filename = f"{title}_{username}_{random.randint(0, 100000)}{ext}"
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('view_image', filename=filename))


@app.route('/images/<filename>')
def view_image(filename):
    title, username = filename.split('_')[:-1]
    return render_template('image.html', title=title, filename=filename, username=username)


if __name__ == '__main__':
    app.run(debug=True)
