from apispec import APISpec
from functools import wraps
from marshmallow import fields, Schema
from six import iteritems


# TODO: Metaclass to add path/definition/parameter helpers
    
class ChaliceAPISpec(APISpec):
    def __init__(self, app, version):
        super(ChaliceAPISpec, self).__init__(title=app.app_name, version=version)
        self.app = app

    
    def model(self, model_class, validate=True):
        app = self.app
        def foobar(endpoint_func):
            for uri, route in iteritems(app.routes):
                for method, route_entry in iteritems(route):
                    if route_entry.view_function == endpoint_func:
                        self.definition(model_class.__name__, schema=model_class)
                        # self.add_path(path=uri, operations={method: })
                        self.app.routes[uri][method].view_function = self.add_options(endpoint_func, uri, model_class)
                        
            return endpoint_func
        return foobar

    def add_options(self, endpoint_func, uri, model_class):
        @wraps(endpoint_func)
        def wrapper(*args, **kwargs):
            if self.app.current_request.method == 'OPTIONS':
                return self.to_dict()['paths'][uri]
        return wrapper
