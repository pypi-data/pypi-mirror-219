from functools import wraps
from datetime import datetime, timedelta
from werkzeug.wrappers import Response


class Limiter:
    def __init__(self, app=None):
        self.limit_value = 100
        self.period = 60
        self.cache = {}
        self.app = app

    def limit(self, limit=100, period=60):
        def decorator(handler):
            @wraps(handler)
            def wrapped_handler(request, *args, **kwargs):
                key = request.remote_addr
                now = datetime.now()
                if key in self.cache:
                    requests = self.cache[key]
                    valid_requests = [
                        req for req in requests if (now - req) <= timedelta(seconds=period)
                    ]
                    if len(valid_requests) >= limit:
                        return Response('Rate limit exceeded', status=429)
                    valid_requests.append(now)
                    self.cache[key] = valid_requests
                else:
                    self.cache[key] = [now]
                return handler(request, *args, **kwargs)

            return wrapped_handler

        return decorator

