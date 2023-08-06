from werkzeug.routing import Map, Rule
from werkzeug.exceptions import NotFound
from werkzeug.wrappers import Request, Response


class Blueprint:
    def __init__(self, name, import_name, url_prefix=''):
        self.name = name
        self.import_name = import_name
        self.url_prefix = url_prefix
        self.url_map = Map()
        self.error_handlers = {}

    def add_url_rule(self, rule, endpoint, handler, methods=['GET']):
        rule = self.url_prefix + rule
        self.url_map.add(Rule(rule, endpoint=endpoint, methods=methods))
        setattr(self, endpoint, handler)

    def route(self, rule, methods=['GET']):
        def decorator(handler):
            self.add_url_rule(rule, handler.__name__, handler, methods)
            return handler

        return decorator

    def errorhandler(self, code):
        def decorator(handler):
            self.error_handlers[code] = handler
            return handler

        return decorator

    def handle_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(self, endpoint)
            response = handler(request, **values)
        except NotFound as e:
            response = self.handle_error(404, e)
        return response

    def handle_error(self, code, error):
        handler = self.error_handlers.get(code)
        if handler:
            return handler(error)
        else:
            return error

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
