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
        'profile':save_profile,
        'img':save_to,
        'title':title_receive,
        'content':content_receive,
        'date':thisdate
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)