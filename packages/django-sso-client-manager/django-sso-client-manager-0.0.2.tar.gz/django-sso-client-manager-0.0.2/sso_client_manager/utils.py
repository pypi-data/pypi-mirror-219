import json
from base64 import b64decode

from cryptography.fernet import Fernet

def decrypt_data(key, ciphertext):
    fernet = Fernet(b64decode(key) )
    data = fernet.decrypt(ciphertext).decode()
    return json.loads(data)
