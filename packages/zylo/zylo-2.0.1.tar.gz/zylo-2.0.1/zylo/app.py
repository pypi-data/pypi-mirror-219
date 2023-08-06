import os
import base64
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.debug import DebuggedApplication
from jinja2 import Environment, FileSystemLoader
from .sessions import session_manager
from .blueprint import Blueprint
from werkzeug.urls import url_encode
from itsdangerous import URLSafeTimedSerializer
import json
import mimetypes
from urllib.parse import quote as url_quote, quote_plus as url_quote_plus, urlencode as url_encode, \
    parse_qs as url_decode
from werkzeug.utils import send_from_directory, safe_join

# Create the application
class Zylo:
    def __init__(self, __name__=None):
        self.template_folder='views'
        self.url_map = Map()
        self.static_folder = "static"
        self.error_handlers = {}
        self.middlewares = []
        self.template_env = Environment(loader=FileSystemLoader(self.template_folder))
        self.host = 'localhost'
        self.port = 8000
        self.debug = True
        self.secret_key = os.urandom(24)
        self.serializer = URLSafeTimedSerializer(base64.urlsafe_b64encode(self.secret_key))
        self.blueprints = []
        self.__name__ = __name__
        self.config = {}

    def add_url_rule(self, rule, endpoint, handler, methods=['GET']):
        def view_func(request, **values):
            return handler(request, **values)
        self.url_map.add(Rule(rule, endpoint=endpoint, methods=methods))
        setattr(self, endpoint, view_func)


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

    def use(self, middleware):
        self.middlewares.append(middleware)

    def config(self):
        return self.config

    def url_for_static(self, filename):
        return f'/static/{filename}'

    def serve_static(self, filename):
        static_path = os.path.join(self.static_folder, filename)
        if os.path.isfile(static_path):
            mimetype, _ = mimetypes.guess_type(static_path)
            if mimetype:
                return Response(open(static_path, 'rb').read(), mimetype=mimetype)
        raise NotFound()

    def register_blueprint(self, blueprint):
        self.blueprints.append(blueprint)

    def handle_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(self, endpoint)
            response = handler(request, **values)
        except NotFound as e:
            response = self.handle_error(404, e, request)
        except HTTPException as e:
            response = e
        return response

    def handle_error(self, code, error, request):
        handler = self.error_handlers.get(code)
        if handler:
            return handler(error, request)
        else:
            return error

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        for blueprint in self.blueprints:
            if request.path.startswith(blueprint.url_prefix):
                request.blueprint = blueprint
                response = blueprint.wsgi_app(environ, start_response)
                return response
        session_id = request.cookies.get('session_id')
        session_data = session_manager.load_session(session_id)
        request.session = session_data
        response = self.handle_request(request)
        session_id = session_manager.save_session(request.session)
        response.set_cookie('session_id', session_id, secure=True, httponly=True)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        app = self.wsgi_app
        for middleware in reversed(self.middlewares):
            app = middleware(app)
        return app(environ, start_response)

    def run(self, host=None, port=None, debug=None, secret_key=None):
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if debug is not None:
            self.debug = debug
        if secret_key is not None:
            self.secret_key = secret_key

        if self.debug:
            app = DebuggedApplication(self, evalex=True)
        else:
            app = self

        from werkzeug.serving import run_simple
        run_simple(self.host, self.port, app, use_reloader=True)

app = Zylo()

def render_template(template_name, **kwargs):
    template = app.template_env.get_template(template_name)
    kwargs['url_for_static'] = app.url_for_static
    return Response(template.render(**kwargs), mimetype='text/html')

def jsonify(data):
    json_data = json.dumps(data)
    return Response(json_data, mimetype='application/json')

def redirect(location, code=302):
    return Response('', status=code, headers={'Location': location})

def url_for(endpoint, **values):
    return app.url_map.build(endpoint, values)

def send_file(filename, mimetype):
    with open(filename, 'rb') as f:
        content = f.read()
    headers = {'Content-Type': mimetype, 'Content-Disposition': f'attachment; filename={os.path.basename(filename)}'}
    return Response(content, headers=headers)

def static_engine(static_folder):
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/static': static_folder})

def template_engine(template_folder):
    app.template_env = Environment(loader=FileSystemLoader(template_folder))

def save_json_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def redirect_args(location, **kwargs):
    url = location
    if kwargs:
        query_params = url_encode(kwargs)
        url += f'?{query_params}'
    return Response(status=302, headers={'Location': url})

def send_from_directory(directory, filename, **options):
    return send_from_directory(directory, filename, **options)

def url_map(rules):
    return Map(rules)

def url_encode(obj, charset='utf-8', errors='strict'):
    return url_encode(obj, charset=charset, errors=errors)

def url_decode(query_string, keep_blank_values=False, strict_parsing=False, charset=None, errors=None):
    return url_decode(query_string, keep_blank_values=keep_blank_values, strict_parsing=strict_parsing,
                      charset=charset, errors=errors)

def stream_with_context(generator_or_function):
    return stream_with_context(generator_or_function)

def make_unique_key():
    return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('ascii')

def url_quote(url, safe='/', encoding=None, errors=None):
    return url_quote(url, safe=safe, encoding=encoding, errors=errors)

def url_quote_plus(url, safe='/', encoding=None, errors=None):
    return url_quote_plus(url, safe=safe, encoding=encoding, errors=errors)

def safe_join(directory, *pathnames):
    return safe_join(directory, *pathnames)