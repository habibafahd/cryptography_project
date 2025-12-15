from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

peer_public = None
messages = []
callbacks = []
disconnect_callbacks = []  

@app.route("/key", methods=["POST"])
def receive_key():
    global peer_public
    data = request.json
    peer_public = int(data["public"])
    return jsonify({"status": "ok"})

@app.route("/message", methods=["POST"])
def receive_message():
    data = request.json
    ciphertext = bytes.fromhex(data["cipher"])
    messages.append(ciphertext)
    for cb in callbacks:
        cb(ciphertext)
    return jsonify({"status": "ok"})

@app.route("/disconnect", methods=["POST"])
def receive_disconnect():
    for cb in disconnect_callbacks:
        cb()
    return jsonify({"status": "disconnected"})

def start_server(port):
    threading.Thread(
        target=lambda: app.run(
            port=port,
            debug=False,
            use_reloader=False
        ),
        daemon=True
    ).start()

def register_callback(func):
    callbacks.append(func)

def register_disconnect_callback(func):
    disconnect_callbacks.append(func)
