import requests
import time

def send_key(peer_url, public_key):
    while True:
        try:
            requests.post(f"{peer_url}/key", json={"public": str(public_key)})
            break
        except requests.exceptions.RequestException:
            time.sleep(1)

def send_message(peer_url, ciphertext):
    while True:
        try:
            requests.post(
                f"{peer_url}/message",
                json={"cipher": ciphertext.hex()}
            )
            break
        except requests.exceptions.RequestException:
            time.sleep(1)

def send_disconnect(peer_url):
    try:
        requests.post(f"{peer_url}/disconnect", timeout=2)
    except requests.exceptions.RequestException:
        pass
