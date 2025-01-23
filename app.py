from flask import Flask
from flask_cors import CORS
from flask import Flask
from flask_cors import CORS
from config import config
from marshmallow import ValidationError
from marshmallow import Schema, fields, ValidationError, validates
from bson import ObjectId,json_util
from flask import jsonify,request,Response
import requests
import json
import time
import threading
from flask_socketio import SocketIO
from Database.connection import Connection
from controllers.KeyController import KeyController
from Scraper import TradingView
from config.config import Config
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app,supports_credentials=True)
KeyControllers=KeyController()
@app.route('/')
def index():
    return "Flask app is running!"

@app.route('/api/postkey', methods=['POST'])
def post_key():
    return KeyControllers.Postkey()

@app.route('/api/getkeys', methods=['GET'])
def get_key():
    return KeyControllers.get_single_key()

@app.route('/api/updatekey/<id>', methods=['PUT'])
def update_key(id):
    return KeyControllers.UpdateKey(id)


# sockets data

def fetch_logs():
    try:
        logs_col = Connection.get_logs_col()
        result = logs_col.find()
        data_array = []
        for doc in result:
            doc['_id'] = str(doc['_id']) 
            data_array.append(doc)
        return data_array
    except Exception as e:
        print(f"Error retrieving logs: {e}")
        return []
def send_periodic_data():
    while True:
        data_array = fetch_logs() 
        if data_array:
            socketio.emit('data', {'message': 'Data retrieved', 'data': data_array})
        time.sleep(1)
    

def start_data_thread():
    thread = threading.Thread(target=send_periodic_data)
    thread.daemon = True
    thread.start()

@socketio.on('connect')
def on_connect():
    print("Client connected, starting data emission.")
    start_data_thread()



def Bot(Captcha_API, Username, password):
    Bot = TradingView(Captcha_API, Username, password)
    Bot.Login()
    Bot.openChart()



def run_flask_and_socketio():
    socketio.run(app, host="0.0.0.0", port=5000)

if __name__ == "__main__":

    bot_thread = threading.Thread(target=Bot, args=(Config.Captcha_API,Config.Username, Config.password))
    bot_thread.start()
    run_flask_and_socketio()





