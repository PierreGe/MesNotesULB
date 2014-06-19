
import json

class Response(object):
    def __init__(self, code, headers, body):
        self.code, self.headers, self.body = int(code), headers, body

    @property
    def family(self):
        return self.code // 100

    @property
    def ok(self):
        return self.family == 2

    @property
    def redirect(self):
        return self.family == 3

    @property
    def req_error(self):
        return self.family == 4

    @property
    def serv_error(self):
        return self.family == 5

    @property
    def error(self):
        return self.req_error or self.serv_error


class Cache:
    """JSON-based persistent datastore providing context manager"""
    def __init__(self, filename, initial={}):
        self.filename = filename
        self.initial = initial

    def __enter__(self):
        self.cache = self.initial
        try:
            self.cache = json.loads(open(self.filename).read())
        except:
            pass
        return self.cache

    def __exit__(self, exc_type, exc_value, backtrace):
        if exc_type is None:
            try:
                open(self.filename, 'w').write(json.dumps(self.cache))
            except:
                return False
            return True
