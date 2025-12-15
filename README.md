"""
# Secure Chat Application

## Overview
This project implements a **secure peer-to-peer chat application** with end-to-end encryption. The security is provided by:

- **Diffie-Hellman key exchange**: securely derives a shared secret between two peers.
- **DES encryption**: encrypts and decrypts messages using the shared secret key.
- **Graphical interface** built with Tkinter.
- **Peer-to-peer communication** over HTTP using Flask.

> ⚠️ **Note:** For demonstration and learning purposes, the application uses **16-bit Diffie-Hellman primes** and **64-bit DES keys**, which are **not secure for real-world applications**.

---

## Features

- **Instance-to-Instance Messaging**: Two peers can securely exchange messages.
- **Key Exchange**: Diffie-Hellman algorithm is implemented from scratch.
- **Message Encryption**: DES is used for message encryption/decryption.
- **Graphical Interface**: Easy-to-use chat window built with Tkinter.
- **Logging**: Optional debug logging for encryption/decryption events.

---

## Requirements

- Python 3.8+
- Packages:  
  pip install flask requests

---

## Running the Application

1. Open two terminal windows (one for each peer).  
2. Start each chat instance on different ports:
   python main_instance.py --port 5000 --peer http://127.0.0.1:5001
   python main_instance.py --port 5001 --peer http://127.0.0.1:5000
3. The application will automatically:
   - Perform Diffie-Hellman key exchange
   - Derive the DES key
   - Activate the GUI once the secure connection is established

---

## Usage

### Sending Messages

1. Type a message in the input field.  
2. Press **Enter** or click **Send**.  
3. The message is encrypted with DES and sent to the peer.

### Receiving Messages

1. Incoming messages are decrypted in real-time.  
2. Messages appear under **Peer** in the chat window.

### Ending Chat

- Click **End Chat** to disconnect.  
- GUI disables inputs and closes automatically after notification.

---

## File Structure

.
├── crypto/
│   ├── des.py
│   └── diffie_hellman.py
├── gui/
│   └── app_gui.py
├── network/
│   ├── server.py
│   └── client.py
├── first_dh_params.py
├── debug_logger.py
├── main_instance.py
└── dh_params.json (generated at runtime)

---

## Cryptography Implementation

- **Diffie-Hellman**:
  - Generates prime `p` and generator `g`.
  - Computes private/public keys.
  - Computes shared secret and derives DES key.

- **DES Encryption**:
  - 64-bit key split into 16 round subkeys.
  - Messages split into 8-byte blocks.
  - 16 Feistel rounds applied for encryption/decryption.
  - Initial and final permutations applied.

---

## Limitations

- 16-bit DH primes and 64-bit DES keys are **not secure**.  
- Implementation is for **learning and demonstration only**.  

---

## Optional

- Debug logs can be enabled via `debug_logger.py`.  
- Diffie-Hellman parameters are temporarily saved in `dh_params.json` and deleted on exit.
"""
