from cryptography.fernet import Fernet
import base64
import json

# Generate a secret key for encryption
secret_key = Fernet.generate_key()
cipher_suite = Fernet(secret_key)


def encrypt_file(file_name):
    try:
        with open(file_name, 'rb') as file:
            file_data = file.read()
    except FileNotFoundError:
        return None

    # Encrypt the file
    encrypted_data = cipher_suite.encrypt(file_data)
    return encrypted_data


def save_encrypted_file(file_name, encrypted_data):
    with open('shared_' + file_name, 'wb') as shared_file:
        shared_file.write(encrypted_data)

    # Save metadata
    encoded_data = base64.b64encode(encrypted_data).decode('utf-8')
    shared_file_data = {
        'file_name': file_name,
        'shared_file_data': encoded_data
    }
    with open('shared_file_data.json', 'w') as shared_file_data_json:
        json.dump(shared_file_data, shared_file_data_json)
