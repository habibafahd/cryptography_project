from crypto import des
def main():
    hex_msg = "0123456789ABCDEF"  
    hex_key = "163457799BBCDFF1"    

    msg_bytes = bytes.fromhex(hex_msg)
    key_bytes = bytes.fromhex(hex_key)

    key_int = int.from_bytes(key_bytes, byteorder='big')

    cipher_bytes = des.encrypt(msg_bytes, key_int)

    decrypted_bytes = des.decrypt(cipher_bytes, key_int)

    print("Original:       ", msg_bytes.hex())
    print("Encrypted hex:  ", cipher_bytes.hex())
    print("Decrypted:      ", decrypted_bytes.hex())
    print("Match?          ", msg_bytes == decrypted_bytes)

if __name__ == "__main__":
    main()