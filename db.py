import mysql.connector
con = mysql.connector.connect(host="localhost", user="newuser", password="password", database="pictic")
cur = con.cursor()
images = []
gallery_length = 0
query = "SELECT filename, username, title, tags from upload"
cur.execute(query)
filename_data = cur.fetchall()
print(filename_data)
search = "cardigan"
for file in filename_data:
    if search.lower() in (file[0] + file[1] + file[2] + file[3]).lower():
        print(file)

# for file in filename_data:
#     filename = file[0]
#     if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
#         title, username = filename.split('_')[:-1]
#         images.append({'filename': filename, 'title': title, 'username': username})
#         gallery_length += 1
