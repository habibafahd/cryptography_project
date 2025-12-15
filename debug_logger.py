def log_encryption(message_bytes, ciphertext, key):
    print("\n=== Encryption Debug ===")
    print(f"Original message: {message_bytes.hex()}")
    print(f"DES key: {key:016x}") 
    print(f"Encrypted message: {ciphertext.hex()}")


def log_decryption(ciphertext, plaintext, key):
    print("\n=== Decryption Debug ===")
    print(f"Ciphertext: {ciphertext.hex()}")
    print(f"DES key: {key:016x}")
    print(f"Decrypted message: {plaintext.hex()}")
