import argparse
import threading
import queue
import time
import os
import json
import atexit
import logging

from network import server, client
from crypto import diffie_hellman as dh
from crypto import des
from gui.app_gui import ChatApp
from first_dh_params import generate_dh_params
from debug_logger import log_encryption, log_decryption

logging.getLogger('werkzeug').setLevel(logging.ERROR)

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, required=True)
parser.add_argument("--peer", type=str, required=True)
args = parser.parse_args()

LOCAL_PORT = args.port
PEER_URL = args.peer

DH_FILE = "dh_params.json"
created_file = False

while True:
    if os.path.exists(DH_FILE):
        with open(DH_FILE, "r") as f:
            dh_data = json.load(f)
            p = dh_data["p"]
            g = dh_data["g"]
        break
    else:
        try:
            p, g = generate_dh_params(bits=16)
            with open(DH_FILE, "x") as f:
                json.dump({"p": p, "g": g}, f)
            created_file = True
            break
        except FileExistsError:
            time.sleep(0.1)

def cleanup_dh_file():
    if created_file and os.path.exists(DH_FILE):
        os.remove(DH_FILE)
        print("DH params file removed.")

atexit.register(cleanup_dh_file)

# diffie hellman
private_key = dh.generate_private_key(p)
public_key = dh.generate_public_key(private_key, g, p)

msg_queue = queue.Queue()

def gui_callback(ciphertext):
    msg_queue.put(ciphertext)

server.register_callback(gui_callback)

des_key = None
chat_active = True

threading.Thread(
    target=lambda: server.start_server(LOCAL_PORT),
    daemon=True
).start()

def set_des_parity(key64):
    key_bytes = key64.to_bytes(8, byteorder='big')
    result = bytearray()
    for b in key_bytes:
        bits = b & 0xFE
        ones = bin(bits).count("1")
        # ensure odd parity
        if ones % 2 == 0:
            b |= 0x01
        else:
            b &= 0xFE
        result.append(b)
    return int.from_bytes(result, byteorder='big')

# encryption and decryption
def send_func(msg_bytes):
    if not chat_active or des_key is None:
        return
    ciphertext = des.encrypt(msg_bytes, des_key)
    log_encryption(msg_bytes, ciphertext, des_key)
    client.send_message(PEER_URL, ciphertext)
    return ciphertext

def decrypt_func(ciphertext):
    if not chat_active or des_key is None:
        return b""
    plaintext = des.decrypt(ciphertext, des_key)
    log_decryption(ciphertext, plaintext, des_key)
    return plaintext

#gui
app = ChatApp(send_func, decrypt_func)
app.send_button.config(state="disabled")
app.entry.config(state="disabled")
app.append_message("Establishing secure connection… Please wait", tag="system")

def end_chat():
    global chat_active
    chat_active = False
    client.send_disconnect(PEER_URL)
    app.append_message("Connection lost. Closing window…", tag="system")
    app.send_button.config(state="disabled")
    app.entry.config(state="disabled")
    app.end_button.config(state="disabled")
    app.root.after(1500, app.root.destroy)
app.set_disconnect_callback(end_chat)

def peer_disconnected():
    global chat_active
    chat_active = False

    app.append_message("Connection lost. Closing window…", tag="system")
    app.send_button.config(state="disabled")
    app.entry.config(state="disabled")
    app.end_button.config(state="disabled")
    app.root.after(1500, app.root.destroy)

server.register_disconnect_callback(peer_disconnected)

def poll_messages():
    while not msg_queue.empty():
        app.receive_message(msg_queue.get())
    app.root.after(100, poll_messages)

poll_messages()

def exchange_keys():
    global des_key
    while True:
        try:
            client.send_key(PEER_URL, public_key)
            break
        except:
            time.sleep(0.5)
    while server.peer_public is None:
        time.sleep(0.1)
    shared_secret = dh.compute_shared_secret(
        server.peer_public, private_key, p
    )

    des_key = set_des_parity(shared_secret & 0xFFFFFFFFFFFFFFFF)

    print("\n===== Diffie-Hellman Info =====")
    print(f"Prime p: {p}")
    print(f"Generator g: {g}")
    print(f"My private key: {private_key}")
    print(f"My public key: {public_key}")
    print(f"Peer public key: {server.peer_public}")
    print(f"Shared secret: {shared_secret}")
    print(f"Derived DES key: {hex(des_key)}")
    print("================================\n")

    app.send_button.config(state="normal")
    app.entry.config(state="normal")
    app.append_message(
        "Secure connection established! You can start chatting now.",
        tag="system"
    )

threading.Thread(target=exchange_keys, daemon=True).start()

app.run()
