import base64
import json
import os
import platform
import secrets
from datetime import datetime, timedelta
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)
from cryptography.hazmat.primitives.serialization.pkcs12 import (
    serialize_key_and_certificates,
)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class JwT:
    def __init__(self, public_key=None, private_key=None):
        self.public_key = public_key
        self.private_key = private_key

        if not self.public_key or not self.private_key:
            self._load_keys()

    def encode(self, payload, algorithm='HS256', time_limit_hours=24):
        header = {'alg': algorithm, 'typ': 'JWT'}
        encoded_header = self._base64_encode(header)
        encoded_payload = self._base64_encode(payload)
        signature = self._generate_signature(encoded_header, encoded_payload)

        token = '{}.{}.{}'.format(encoded_header, encoded_payload, signature)
        return token

    def create_access_token(self, payload, algorithm='HS256', time_limit_hours=24):
        now = datetime.utcnow()
        payload['iat'] = now
        payload['exp'] = now + timedelta(hours=time_limit_hours)
        return self.encode(payload, algorithm, time_limit_hours)

    def verify_access_token(self, access_token):
        return self.verify_token(access_token)

    def retrieve_access_token(self, refresh_token, algorithm='HS256', time_limit_hours=24):
        try:
            payload = self.verify_token(refresh_token)
            if 'exp' in payload:
                del payload['exp']
            if 'iat' in payload:
                del payload['iat']
            return self.create_access_token(payload, algorithm, time_limit_hours)
        except Exception as e:
            raise ValueError('Invalid refresh token') from e
        
    def create_payload(self, payload, algorithm='HS256', time_limit_hours=24):
        now = datetime.utcnow()
        payload['iat'] = now
        payload['exp'] = now + timedelta(hours=time_limit_hours)
        return self.encode(payload, algorithm, time_limit_hours)

    def verify_payload(self, token):
        return self.verify_token(token)

    def decode_payload(self, refresh_token, algorithm='HS256', time_limit_hours=24):
        try:
            payload = self.verify_token(refresh_token)
            if 'exp' in payload:
                del payload['exp']
            if 'iat' in payload:
                del payload['iat']
            return self.create_payload(payload, algorithm, time_limit_hours)
        except Exception as e:
            raise ValueError('Invalid token') from e

    def _base64_encode(self, data):
        json_data = json.dumps(data, cls=CustomJSONEncoder).encode('utf-8')
        encoded_data = base64.urlsafe_b64encode(json_data).decode('utf-8')
        return encoded_data

    def _base64_decode(self, encoded_data):
        data = base64.urlsafe_b64decode(encoded_data.encode('utf-8')).decode('utf-8')
        return data

    def _load_keys(self):
        system = platform.system()
        if system == 'Windows':
            key_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'zylo')
        elif system == 'Darwin':
            key_dir = os.path.join(os.path.expanduser("~"), 'Library', 'zylo')
        else:
            key_dir = os.path.join(os.path.expanduser("~"), '.zylo')
        os.makedirs(key_dir, exist_ok=True)

        private_key_path = os.path.join(key_dir, 'id_jit')
        public_key_path = os.path.join(key_dir, 'id_jit.pub')

        if os.path.isfile(private_key_path) and os.path.isfile(public_key_path):
            with open(private_key_path, 'rb') as f:
                private_pem = f.read()

            with open(public_key_path, 'rb') as f:
                public_pem = f.read()

            self.private_key = private_pem
            self.public_key = public_pem
        else:
            self._generate_keys()

    def _generate_keys(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption()
        )

        public_pem = public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        )

        system = platform.system()
        if system == 'Windows':
            key_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'zylo')
        elif system == 'Darwin':
            key_dir = os.path.join(os.path.expanduser("~"), 'Library', 'zylo')
        else:
            key_dir = os.path.join(os.path.expanduser("~"), '.zylo')
        os.makedirs(key_dir, exist_ok=True)

        private_key_path = os.path.join(key_dir, 'id_jit')
        public_key_path = os.path.join(key_dir, 'id_jit.pub')

        with open(private_key_path, 'wb') as f:
            f.write(private_pem)

        with open(public_key_path, 'wb') as f:
            f.write(public_pem)

        self.private_key = private_pem
        self.public_key = public_pem

    def _generate_signature(self, encoded_header, encoded_payload):
        data = encoded_header.encode('utf-8') + b'.' + encoded_payload.encode('utf-8')
        key = self.private_key
        h = HMAC(key, hashes.SHA256(), backend=default_backend())
        h.update(data)
        signature = h.finalize()
        encoded_signature = base64.urlsafe_b64encode(signature).decode('utf-8')
        return encoded_signature

    def verify_token(self, token):
        try:
            encoded_header, encoded_payload, signature = token.split('.')
            header = self._base64_decode(encoded_header)
            payload = self._base64_decode(encoded_payload)

            expected_signature = self._generate_signature(encoded_header, encoded_payload)
            if signature != expected_signature:
                raise ValueError('Invalid token signature')

            decoded_payload = json.loads(payload)
            now = datetime.utcnow()
            if 'exp' in decoded_payload and now >= datetime.fromisoformat(decoded_payload['exp']):
                raise ValueError('Expired token')

            return decoded_payload
        except Exception as e:
            raise ValueError('Invalid token') from e

def error_handler(error):
    error_message = str(error)
    if isinstance(error, ValueError):
        if 'Invalid token signature' in error_message:
            return 'Invalid token signature.'
        elif 'Expired token' in error_message:
            return 'Token has expired.'
        elif 'Invalid token' in error_message:
            return 'Invalid token format.'
        elif 'Invalid refresh token' in error_message:
            return 'Invalid refresh token.'
    return 'An error occurred.'
