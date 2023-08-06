import os
import base64
from cryptography.fernet import Fernet
from itsdangerous import URLSafeTimedSerializer


class SessionManager:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.serializer = URLSafeTimedSerializer(secret_key)
        self.cipher_suite = Fernet(base64.urlsafe_b64encode(secret_key))

    def encode_data(self, data):
        serialized_data = self.serializer.dumps(data)
        encrypted_data = self.cipher_suite.encrypt(serialized_data.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

    def decode_data(self, data):
        encrypted_data = base64.urlsafe_b64decode(data.encode('utf-8'))
        decrypted_data = self.cipher_suite.decrypt(encrypted_data).decode('utf-8')
        return self.serializer.loads(decrypted_data)

    def save_session(self, session_data):
        session_id = self.encode_data(session_data)
        return session_id

    def load_session(self, session_id):
        try:
            session_data = self.decode_data(session_id)
        except Exception:
            session_data = {}
        return session_data


# Create a global instance of the session manager
secret_key = os.urandom(32)
session_manager = SessionManager(secret_key)
