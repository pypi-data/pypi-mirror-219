import secrets
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.session_duration = timedelta(minutes=30)

    def generate_session_token(self):
        return secrets.token_hex(16)

    def create_session(self):
        token = self.generate_session_token()
        expires_at = datetime.now() + self.session_duration
        self.sessions[token] = {'expires_at': expires_at, 'data': {}}
        return token

    def get_session(self, token):
        session = self.sessions.get(token)
        if session and session['expires_at'] > datetime.now():
            return session['data']
        return {}

    def update_session(self, token, data):
        if token in self.sessions:
            session = self.sessions[token]
            if session['expires_at'] > datetime.now():
                session['data'] = data
                session['expires_at'] = datetime.now() + self.session_duration
                return session['data']
        return {}

    def delete_session(self, token):
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False
