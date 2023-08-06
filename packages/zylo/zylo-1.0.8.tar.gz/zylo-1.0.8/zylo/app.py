import json
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, default_exceptions, NotFound, MethodNotAllowed
from jinja2 import Environment, FileSystemLoader
from .sessions import SessionManager
from werkzeug.urls import url_encode
from .limiter import Limiter
import os
import mimetypes

class Zylo:
    def __init__(self, __name__={} ):
        self.url_map = Map()
        self.routes = {}
        self.template_env = Environment(loader=FileSystemLoader('views'))
        self.static_folder = 'static'
        self.session_manager = SessionManager()
        self.blueprints = []
        self.template_folder = None
        self.limiter = Limiter()
        self.before_request_funcs = []
        self.after_request_funcs = []
        self.__name__ = __name__

    def route(self, rule, methods=['GET'], endpoint=None,):
        def decorator(func):
            self.routes[endpoint or func.__name__] = (rule, methods, func)
            return func
        return decorator

    def register_blueprint(self, blueprint):
        self.blueprints.append(blueprint)
        blueprint.register(self)
        
    def url_for_static(self, filename):
        return f'/static/{filename}'
    
    def serve_static(self, filename):
        static_path = os.path.join(self.static_folder, filename)
        if os.path.isfile(static_path):
            mimetype, _ = mimetypes.guess_type(static_path)
            if mimetype:
                return Response(open(static_path, 'rb').read(), mimetype=mimetype)
        raise NotFound()
    
    def before_request(self, func):
        self.before_request_funcs.append(func)
        return func

    def after_request(self, func):
        self.after_request_funcs.append(func)
        return func

    def run(self, host='localhost', port=8000, debug=True):
        app = self
        host = host
        port = port
        debug = debug

        @Request.application
        def application(request):
            try:
                session_token = request.cookies.get('session_token')
                session_data = app.session_manager.get_session(session_token)
                request.session = session_data

                adapter = app.url_map.bind_to_environ(request.environ)
                try:
                    endpoint, values = adapter.match()
                except NotFound:
                    for blueprint in app.blueprints:
                        adapter = blueprint.url_map.bind_to_environ(request.environ)
                        try:
                            endpoint, values = adapter.match()
                            break
                        except NotFound:
                            pass
                    else:
                        raise
                rule, methods, func = app.routes[endpoint]
                if request.method not in methods:
                    raise MethodNotAllowed(valid_methods=methods)

                if hasattr(request, 'session'):
                    if not session_token or not session_data:
                        session_token = app.session_manager.create_session()
                        session_data = {}
                        request.session = session_data
                        response = func(request, **values)
                        response.set_cookie('session_token', session_token)
                    else:
                        response = func(request, **values)

                    app.session_manager.update_session(session_token, request.session)

                return response

            except HTTPException as e:
                return e

        if debug:
            from werkzeug.debug import DebuggedApplication
            application = DebuggedApplication(application, evalex=True)

        for endpoint, (rule, _, _) in self.routes.items():
            self.url_map.add(Rule(rule, endpoint=endpoint))
            print(f"Registered route: {rule} --> {endpoint}")

        for blueprint in self.blueprints:
            blueprint.register(self)

        from werkzeug.serving import run_simple
        run_simple(host, port, application, use_reloader=debug)

app = Zylo()

def render_template(template_name, **kwargs):
    template = app.template_env.get_template(template_name)
    kwargs['url_for_static'] = app.url_for_static
    return Response(template.render(**kwargs), mimetype='text/html')

def jsonify(data):
    response = Response()
    response.headers['Content-Type'] = 'application/json'
    response.data = json.dumps(data)
    return response

def redirect(location):
    response = Response()
    response.status_code = 302
    response.headers['Location'] = location
    return response

def url_for(endpoint):
    rule, _, _ = app.routes[endpoint]
    url_map = app.url_map.bind(app.host, app.port)
    return url_map.build(rule, force_external=True)

def redirect_args(location, **kwargs):
    url = location
    if kwargs:
        query_params = url_encode(kwargs)
        url += f'?{query_params}'
    return Response(status=302, headers={'Location': url})

def send_file(filename, mimetype=None, as_attachment=False):
    response = Response()
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"' if as_attachment else f'inline; filename="{filename}"'
    if mimetype is not None:
        response.headers['Content-Type'] = mimetype
    return response

def static_engine(static_folder):
    app.static_folder = static_folder


def template_engine(template_folder):
    app.template_folder = template_folder
    app.template_env = Environment(loader=FileSystemLoader(template_folder))

# Add Werkzeug's default error handlers
for code in default_exceptions:
    handler = default_exceptions[code]

    def error_handler(error):
        response = Response()
        response.status_code = error.code
        response.data = f'{error.code} {error.name}'
        return response

    handler = error_handler

