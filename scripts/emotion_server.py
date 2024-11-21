from flask import Flask, request, jsonify
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Shared variable to store the latest emotion
latest_emotion = None

@app.route('/emotion', methods=['POST'])
def receive_emotion():
    global latest_emotion
    data = request.get_json()
    emotion = data.get('emotion')
    if emotion:
        latest_emotion = emotion
        print(f"Received emotion: {emotion}")
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'No emotion received'}), 400

@app.route('/get_emotion', methods=['GET'])
def get_emotion():
    if latest_emotion:
        return jsonify({'emotion': latest_emotion})
    else:
        return jsonify({'emotion': None})

def run_app():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    threading.Thread(target=run_app).start()
