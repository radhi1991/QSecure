from flask import Flask, request, jsonify
import os
from email_service import send_email_confirmation
from encryption_service import encrypt_file, save_encrypted_file, decrypt_file

app = Flask(__name__)

# Email configuration
SMTP_SERVER = 'smtp.example.com'  # Replace with your SMTP server
SMTP_PORT = 587  # Replace with your SMTP port
SMTP_USERNAME = 'your_email@example.com'  # Replace with your email
SMTP_PASSWORD = 'your_password'  # Replace with your email password

@app.route('/create-folder', methods=['POST'])
def create_folder():
    folder_name = request.json.get('folder_name')
    if folder_name:
        os.makedirs(folder_name, exist_ok=True)
        return jsonify({'message': 'Folder created successfully!'}), 201
    return jsonify({'message': 'Folder name is required!'}), 400

@app.route('/share-file', methods=['POST'])
def share_file():
    file_name = request.json.get('file_name')
    recipient_email = request.json.get('recipient_email')  # Get recipient email from request
    if file_name:
        # Encrypt the file
        encrypted_data = encrypt_file(file_name)
        if encrypted_data is None:
            return jsonify({'message': 'File not found!'}), 404

        # Save the encrypted file and metadata
        save_encrypted_file(file_name, encrypted_data)

        # Send email confirmation
        send_email_confirmation(recipient_email, file_name)

        return jsonify({'message': 'File shared successfully!'}), 200
    return jsonify({'message': 'File name is required!'}), 400

@app.route('/download-shared-file', methods=['POST'])
def download_shared_file():
    shared_file_name = request.json.get('shared_file_name')
    if shared_file_name:
        try:
            with open('shared_file_data.json', 'r') as shared_file_data_json:
                shared_file_data = json.load(shared_file_data_json)
                if shared_file_name == shared_file_data['file_name']:
                    encoded_data = shared_file_data['shared_file_data']
                    decoded_data = base64.b64decode(encoded_data)
                    decrypted_data = decrypt_file(decoded_data)

                    with open('downloaded_' + shared_file_name, 'wb') as downloaded_file:
                        downloaded_file.write(decrypted_data)

                    return jsonify({'message': 'File downloaded successfully!'}), 200
                else:
                    return jsonify({'message': 'Shared file not found!'}), 404
        except FileNotFoundError:
            return jsonify({'message': 'Shared file data not found!'}), 404
    return jsonify({'message': 'Shared file name is required!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
