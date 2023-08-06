from werkzeug.routing import Rule
from werkzeug.wrappers import Response, request
from functools import wraps
from werkzeug.exceptions import HTTPException, MethodNotAllowed

class Blueprint:
    def __init__(self, name, import_name, url_prefix=''):
        self.name = name
        self.import_name = import_name
        self.url_prefix = url_prefix
        self.url_map = []

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', f.__name__)
            methods = options.pop('methods', ['GET'])
            secure = options.pop('secure', False)
            self.url_map.append((rule, endpoint, f, methods, secure))
            return f
        return decorator

    def register(self, zylo_app):
        for rule, endpoint, f, methods, secure in self.url_map:
            full_rule = f'{self.url_prefix}{rule}'
            zylo_app.url_map.add(Rule(full_rule, endpoint=endpoint))
            zylo_app.routes[endpoint] = (full_rule, methods, f)

            if secure:
                zylo_app.before_request_funcs.append(self._enforce_https(f))

    def _enforce_https(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if not request.is_secure:
                response = Response()
                response.status_code = 301
                response.headers['Location'] = request.url.replace('http://', 'https://')
                return response
            return f(*args, **kwargs)
        return decorator


def blueprint_route(rule, **options):
    def decorator(f):
        endpoint = options.pop('endpoint', f.__name__)
        f.blueprint_rule = (rule, endpoint)
        return f
    return decorator

def register_blueprint(app, blueprint):
    blueprint.register(app)
