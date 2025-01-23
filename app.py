import eventlet
eventlet.monkey_patch() 
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from controllers.KeyController import KeyController
from Scraper import TradingView
from config.config import Config
from Database.connection import Connection
import time
import threading

app = Flask(__name__)
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')  # Use eventlet for async mode


KeyControllers = KeyController()

# Routes
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

# Function to fetch logs from DB
def fetch_logs():
    try:
        logs_col = Connection.get_logs_col()
        result = logs_col.find()
        data_array = []
        for doc in result:
            doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
            data_array.append(doc)
        return data_array
    except Exception as e:
        print(f"Error retrieving logs: {e}")
        return []

# Function to emit data periodically
def send_periodic_data():
    while True:
        data_array = fetch_logs()
        if data_array:
            socketio.emit('data', {'message': 'Data retrieved', 'data': data_array})
        time.sleep(1)  # Emit data every second

# Start a background thread to send data periodically
def start_data_thread():
    thread = threading.Thread(target=send_periodic_data)
    thread.daemon = True
    thread.start()

# SocketIO event for connection
@socketio.on('connect')
def on_connect():
    print("Client connected, starting data emission.")
    start_data_thread()

# Bot function to start scraping
def Bot(Captcha_API, Username, password):
    Bot = TradingView(Captcha_API, Username, password)
    Bot.Login()
    Bot.openChart()

# Run the Flask app and SocketIO with eventlet
def run_flask_and_socketio():
    socketio.run(app, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    # Start bot thread to run scraper
    bot_thread = threading.Thread(target=Bot, args=(Config.Captcha_API, Config.Username, Config.password))
    bot_thread.start()

    run_flask_and_socketio()






