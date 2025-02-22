# emotion_server.py

from flask import Flask, request, jsonify
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Configure logging
logging.basicConfig(level=logging.INFO)

# Shared variable to store the latest emotion
latest_emotion = None

@app.route('/emotion', methods=['POST'])

def receive_emotion():
    """Endpoint to receive emotion data from the client."""
    global latest_emotion
    data = request.get_json()
    emotion = data.get('emotion')
    if emotion:
        latest_emotion = emotion
        app.logger.info(f"Received emotion: {emotion}")
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No emotion received'}), 400

@app.route('/get_emotion', methods=['GET'])

def get_emotion():
    """Endpoint to provide the latest emotion to demo1.py."""
    if latest_emotion:
        return jsonify({'emotion': latest_emotion}), 200
    else:
        return jsonify({'emotion': None}), 200

@app.route('/user', methods=['POST'])
def receive_user():
    """Endpoint to receive user data from the client."""
    global latest_user
    data = request.get_json()
    user = data.get('user')
    if user:
        latest_user = user
        app.logger.info(f"Received user: {user}")
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'No user received'}), 400

@app.route('/get_user', methods=['GET'])
def get_user():
    """Endpoint to provide the latest user."""
    return jsonify({'user': latest_user}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

