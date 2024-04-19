from http import client
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from os.path import join, dirname

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    
    highest_num_doc = db.diary.find_one(sort=[("id", -1)])

    if highest_num_doc:
        highest_num = highest_num_doc["id"]
    else:
         highest_num = 0

# Tentukan nomor baru yang unik
    new_num = highest_num + 1
    
    today = datetime.now()
    date_time = today.strftime("%Y-%m-%d-%H-%M-%S")
    
    profilephoto = request.files["profile_give"]
    extensionprofile = profilephoto.filename.split('.')[-1]
    save_profile = f'static/profile/profile{date_time}.{extensionprofile}'
    profilephoto.save(save_profile)
    
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    save_to = f'static/post{date_time}.{extension}'
    file.save(save_to)
    
    
    thisdate = today.strftime("%Y-%m-%d")
    
  

    doc = {
        'id':new_num,
        'profile':save_profile,
        'img':save_to,
        'title':title_receive,
        'content':content_receive,
        'date':thisdate
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})



@app.route('/diary/random', methods=['POST'])
def random_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    profilephoto = request.form["profile_give"]
    file = request.form["file_give"]
    today = datetime.now()  
    thisdate = today.strftime("%Y-%m-%d")
    information = request.form["info"]
    
    highest_num_doc = db.diary.find_one(sort=[("id", -1)])

    if highest_num_doc:
        highest_num = highest_num_doc["id"]
    else:
         highest_num = 0

# Tentukan nomor baru yang unik
    new_num = highest_num + 1
   

    doc = {
        'id':new_num,
        'profile':profilephoto,
        'img':file,
        'title':title_receive,
        'content':content_receive,
        'date':thisdate,
        'info':information
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})


@app.route('/diary/delete', methods=['POST'])
def deletedata():
    id_receive = request.form["id_give"]
    file_img = db.diary.find_one({'id':int(id_receive)})['img']
    file_profile = db.diary.find_one({'id':int(id_receive)})['profile']
    if os.path.exists(file_img):
        os.remove(file_img)
    else:
        print('The file Image does not exist')
    
    if os.path.exists(file_profile):
        os.remove(file_profile)
    else:
        print('The file Profile does not exist')
    db.diary.delete_one({'id':int(id_receive)})
    return jsonify({'msg':'Delete complete!'})


@app.route('/diary/edit', methods=['POST'])
def edit_data():
    id_receive = request.form['id_give']
    newTitle_receive = request.form['newTitle_give']
    newContent_receive = request.form['newContent_give']
    newFile_receive = request.files.get('newFile_give')  # Menggunakan get() untuk menghindari KeyError jika tidak ada file_receive yang diberikan
    newProfile_receive = request.files.get('newProfile_give')  # Menggunakan get() untuk menghindari KeyError jika tidak ada profile_receive yang diberikan
    
    file_img = db.diary.find_one({'id': int(id_receive)})['img']
    file_profile = db.diary.find_one({'id': int(id_receive)})['profile']

    if newFile_receive and os.path.exists(file_img):
        os.remove(file_img)
    else:
        print('The file Image does not exist or no new file provided')

    if newProfile_receive and os.path.exists(file_profile):
        os.remove(file_profile)
    else:
        print('The file Profile does not exist or no new profile provided')

    update_data = {'title': newTitle_receive, 'content': newContent_receive, 'date-updated':"Edited at : "+datetime.now().strftime("%Y-%m-%d (%H.%M)")}
    
    if newFile_receive:
        today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        extensionprofile = newFile_receive.filename.split('.')[-1]
        save_profile = f'static/profile/profile{today}.{extensionprofile}'
        newFile_receive.save(save_profile)  
        update_data['img'] = save_profile
        
    if newProfile_receive:
        today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        extension = newProfile_receive.filename.split('.')[-1]
        save_to = f'static/post{today}.{extension}'
        newProfile_receive.save(save_to)
        update_data['profile'] = save_to

    db.diary.update_one({'id': int(id_receive)},
                        {'$set': update_data})
    
    return jsonify({'msg': 'SUCCESS UPDATE!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)