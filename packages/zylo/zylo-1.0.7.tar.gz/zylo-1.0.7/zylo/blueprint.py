from werkzeug.routing import Rule
from functools import wraps

class Blueprint:
    def __init__(self, name, import_name, url_prefix=''):
        self.name = name
        self.import_name = import_name
        self.url_prefix = url_prefix
        self.url_map = []

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', f.__name__)
            self.url_map.append((rule, endpoint, f))
            return f
        return decorator

    def register(self, zylo_app):
        for rule, endpoint, f in self.url_map:
            full_rule = f'{self.url_prefix}{rule}'
            zylo_app.url_map.add(Rule(full_rule, endpoint=endpoint))
            zylo_app.routes[endpoint] = (full_rule, ['GET', 'POST'], f)


def blueprint_route(rule, **options):
    def decorator(f):
        endpoint = options.pop('endpoint', f.__name__)
        f.blueprint_rule = (rule, endpoint)
        return f
    return decorator

def register_blueprint(app, blueprint):
    blueprint.register(app)
