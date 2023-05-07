import hashlib
import os
import random

import mysql.connector
import tensorflow as tf
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from tensorflow.keras.applications.inception_v3 import decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from flask import Flask, flash, session

app = Flask(__name__)
app.secret_key = 'replace this with a more secure key'

con = mysql.connector.connect(host="localhost", user="newuser", password="password", database="pictic")
cur = con.cursor()
# cur.execute('SET global max_allowed_packet=67108864')
cur.execute('SET session wait_timeout=30000000;')

cur.execute("""CREATE TABLE IF NOT EXISTS `User` (
`User_ID` int NOT NULL AUTO_INCREMENT,
`username` varchar(225),
`Email` varchar(225) DEFAULT NULL,
`password` varchar(225),
`name` varchar(225),
PRIMARY KEY (`User_ID`))""")

cur.execute("""CREATE TABLE IF NOT EXISTS `upload` (
`username` varchar(225) NOT NULL,
`filename` varchar(225),
`title` varchar(225) NOT NULL,
`tags` varchar(225))""")

cur.execute("""CREATE TABLE IF NOT EXISTS `comments` (
                `username` VARCHAR(225) NOT NULL,
                `filename` VARCHAR(225) NOT NULL,
                `comment` VARCHAR(500) NOT NULL)""")


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/profile')
def login_success():
    return redirect(url_for('gallery'))


username_password = {('admin', 'admin')}
user_info = []


class User(UserMixin):
    pass


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # sql_query = "SELECT username FROM User"
    # cur.execute(sql_query)
    # data = cur.fetchall()
    # if user_id in data:
    user = User()
    user.id = user_id
    return user
    # else:
    #     print("load user failed")
    #     print(data)


def hashing(string):
    hash_object = hashlib.sha256(string.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


# Route for handling the login page logic

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        x = request.form['username']
        y = "username"
        sql = f"SELECT COUNT(*) FROM User WHERE {y} = '{x}'"
        cur.execute(sql)
        result1 = cur.fetchone()
        if result1[0] > 0:
            sql = "SELECT password FROM User WHERE username = %s"
            cur.execute(sql, (request.form['username'],))
            result = cur.fetchone()
            if (result[0]) != hashing(request.form['password']):
                error = 'Invalid Credentials. Please try again.'
            else:
                user = User()
                user.id = request.form['username']
                login_user(user)
                return redirect(url_for('login_success'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('Desktop2.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    uid = 0
    if request.method == 'POST':
        x = request.form['username']
        y = "username"
        sql = f"SELECT COUNT(*) FROM User WHERE {y} = '{x}'"
        cur.execute(sql)
        result1 = cur.fetchone()
        if result1[0] > 0:
            error = 'Username already taken.'
        else:
            h = hashing(request.form['password'])
            sql = f"INSERT INTO User (User_ID,username,password,email,name) VALUES " \
                  f"(%s,%s,%s,%s,%s)"
            cur.execute(sql, (uid, request.form['username'], h, request.form['email'], request.form['name']))
            con.commit()
            uid = uid + 1
            return redirect(url_for('login'))
    return render_template('Desktop3.html', error=error)


@app.route('/gallery')
@login_required
def gallery():
    images = []
    gallery_length = 0
    query = "SELECT filename from upload"
    cur.execute(query)
    filename_data = cur.fetchall()
    for file in filename_data:
        filename = file[0]
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.png') or filename.lower().endswith('.jpeg'):
            title, username = filename.split('_')[:-1]
            images.append({'filename': filename, 'title': title, 'username': username})
            gallery_length += 1
    return render_template('gallery.html', images=images)


app.config['UPLOAD_FOLDER'] = 'static/uploads/'


@app.route('/upload', methods=['GET'])
@login_required
def upload():
    return render_template('upload.html')


model = tf.keras.applications.InceptionV3(include_top=True, weights='imagenet')


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    image = request.files['image']
    username = current_user.id
    title = request.form['title']
    ext = os.path.splitext(image.filename)[1]
    ext = ext.lower()

    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    if ext not in image_extensions:
        return 'Invalid image', 400

    filename = f"{title}_{username}_{random.randint(0, 100000)}{ext}"
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # ML TAGS

    # InceptionV3 model trained on ImageNet dataset

    f = "static/uploads/" + filename
    img = load_img(f, target_size=(299, 299))

    img_array = img_to_array(img)
    img_array = tf.keras.applications.inception_v3.preprocess_input(img_array)

    predictions = model.predict(img_array.reshape(1, 299, 299, 3))

    decoded_predictions = decode_predictions(predictions, top=10)[0]
    # checking for inappropiate tags
    for pred in decoded_predictions:
        if pred[1] in ['pornographic', 'vibrator', 'sex_toy', 'condom', 'handcuffs', 'bondage', 'nipple', 'stripper',
                       'striptease', 'orgy', 'sex', 'bikini']:
            flash("Please do not upload inappropriate content!")
            return redirect(url_for(upload))
    tags = [tag[1] for tag in decoded_predictions]
    stags = ", ".join(tags)
    ##########

    sql = f"INSERT INTO upload (username,filename,title,tags) VALUES " \
          f"(%s,%s,%s,%s)"
    cur.execute(sql, (username, filename, title, stags))
    con.commit()
    return redirect(url_for('view_image', filename=filename))


@app.route('/images/<filename>')
def view_image(filename):
    sql_query = "Select filename, title, username, tags from upload where filename = " + "'" + filename + "';"
    title, username = filename.split('_')[:-1]
    cur.execute(sql_query)
    filename_data = cur.fetchall()

    # Get comments for this image
    cur.execute("SELECT filename, username, comment FROM comments WHERE filename=" + "'" + filename + "';")
    comments = cur.fetchall()

    return render_template('image.html', title=title, filename=filename, username=username,
                           tags=filename_data[0][3].split(","), comments=comments)


@app.route('/add_comment/<filename>', methods=['POST'])
@login_required
def add_comment(filename):
    comment_text = request.form.get('comment')
    if comment_text:
        username = current_user.id
        cur.execute("INSERT INTO comments (filename, username, comment) VALUES (%s, %s, %s)",
                    (filename, username, comment_text))
        con.commit()
        flash("Comment added successfully!", "success")
    else:
        flash("Please enter a comment first.", "error")
    return redirect(url_for('view_image', filename=filename))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['search']
        images = []
        sql_query = "SELECT filename, username, title, tags from upload"
        cur.execute(sql_query)
        filename_data = cur.fetchall()
        for file in filename_data:
            if query.lower() in (file[0] + file[1] + file[2] + file[3]).lower():
                images.append({'filename': file[0], 'title': file[2]})
        return render_template('search.html', query=query, images=images)
    else:
        return render_template('search.html')


@app.route('/tag', methods=['GET', 'POST'])
def tag():
    query = request.args.get('query')
    images = []
    sql_query = "SELECT filename, username, title, tags from upload"
    cur.execute(sql_query)
    filename_data = cur.fetchall()
    for file in filename_data:
        if query.lower() in (file[0] + file[1] + file[2] + file[3]).lower():
            images.append({'filename': file[0], 'title': file[2]})
    return render_template('tag.html', query=query, images=images)


@app.route('/user_images/', methods=['GET', 'POST'])
def user_images():
    query = request.args.get('query')
    username = query
    images = []
    sql_query = "SELECT filename, username, title, tags from upload WHERE username = " + "'" + username + "';"
    cur.execute(sql_query)
    filename_data = cur.fetchall()
    for file in filename_data:
        images.append({'filename': file[0], 'title': file[2]})
    return render_template('user_images.html', query=query, images=images)


@app.route('/users')
def users():
    # Get the list of users from the database
    cur.execute("SELECT username FROM User")
    users_data = cur.fetchall()

    return render_template('users.html', users=users_data)


@app.template_filter('generate_random_color')
def generate_random_color(value):
    while True:
        color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
        # Calculate the brightness of the color
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        # Ensure the color has sufficient contrast with white (brightness difference >= 125)
        if abs(brightness - 255) >= 125:
            break
    return color



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized():
    # Redirect the user to the login page
    return redirect(url_for('login'))


# @app.route('/myprofile')
# def myprofile():
#     return render_template('myprofile.html')


if __name__ == '__main__':
    app.run(debug=True)
