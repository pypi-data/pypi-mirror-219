from werkzeug.routing import Map, Rule
from werkzeug.exceptions import NotFound
from werkzeug.wrappers import Request, Response
from .sessions import session_manager

class Blueprint:
    def __init__(self, name, import_name, url_prefix=''):
        self.name = name
        self.import_name = import_name
        self.url_prefix = url_prefix
        self.url_map = Map()
        self.error_handlers = {}
        self.session_manager = session_manager

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
            response = Response(str(error), status=code)
            response.set_cookie('session_id', '', expires=0)
            return response


    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        session_id = request.cookies.get('session_id')
        session_data = self.session_manager.load_session(session_id)
        request.session = session_data
        response = self.handle_request(request)
        session_id = self.session_manager.save_session(request.session)
        response.set_cookie('session_id', session_id, secure=True, httponly=True)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
