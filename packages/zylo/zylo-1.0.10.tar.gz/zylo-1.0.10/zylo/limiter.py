from werkzeug.wrappers import Response, request
from functools import wraps
from datetime import datetime, timedelta

class Limiter:
    def __init__(self, app=None):
        self.app = app
        self.cache = {}
        self.default_limits = []
        self.headers_enabled = True

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.limiter = self
        app.before_request(self.before_request)
        if self.headers_enabled:
            app.after_request(self.after_request)

    def before_request(self):
        rule = self.get_rule(request.url_rule)
        if rule is None:
            return None

        key = self.get_storage_key(rule.endpoint)
        limit = self.get_view_rate_limit(rule)

        if self.is_rate_limited(key, limit):
            return self.handle_rate_limit_exceeded(limit)

        self.increment_counter(key, limit)

    def after_request(self, response):
        response.headers.add('X-RateLimit-Limit', str(response.limit))
        response.headers.add('X-RateLimit-Remaining', str(response.remaining))
        reset_time = datetime.utcnow() + timedelta(seconds=response.reset)
        response.headers.add('X-RateLimit-Reset', reset_time.strftime('%Y-%m-%d %H:%M:%S'))
        return response

    def get_storage_key(self, endpoint):
        return f'limiter:{endpoint}:{request.remote_addr}'

    def get_view_rate_limit(self, rule):
        endpoint = rule.endpoint
        for limit, endpoint_func in self.default_limits:
            if endpoint_func is None or endpoint_func == endpoint:
                return limit

    def is_rate_limited(self, key, limit):
        counter = self.cache.get(key, 0)
        return counter >= limit

    def handle_rate_limit_exceeded(self, limit):
        response = Response()
        response.status_code = 429
        response.data = f'Rate limit exceeded. Limit: {limit}'
        return response

    def increment_counter(self, key, limit):
        self.cache.setdefault(key, 0)
        self.cache[key] += 1

    def limit(self, limit_value, key_func=None):
        def decorator(f):
            self.default_limits.append((limit_value, f.__name__))
            @wraps(f)
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapped
        return decorator
