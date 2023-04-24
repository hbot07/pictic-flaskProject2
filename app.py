import os

from flask import Flask
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Render the upload form
@app.route('/upload')
def upload_form():
    return render_template('upload.html')


# Handle the image upload
@app.route('/upload', methods=['POST'])
def upload_image():
    # Get the form data
    username = request.form['username']
    title = request.form['title']
    image = request.files['image']

    # Check if the image file is valid
    if image.filename == '':
        return 'No selected file'

    if not allowed_file(image.filename):
        return 'Invalid file extension'

    # Save the image to the upload folder
    image.save(app.config['UPLOAD_FOLDER'] + image.filename)

    # Render a success message
    return 'Image successfully uploaded!'


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
    for filename in os.listdir('static/uploads'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            title, username = filename.split('_')[:-1]
            images.append({'filename': filename, 'title': title, 'username': username})
    return render_template('gallery.html', images=images)



if __name__ == '__main__':
    app.run()
