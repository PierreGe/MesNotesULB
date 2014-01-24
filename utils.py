import tempfile
import os
import subprocess

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

class CURLSession(object):
    """Wrapper for curl command-line tool"""
    def __init__(self, *curl_opts):
        fd, self.headers = tempfile.mkstemp(suffix='.headers')
        fd, self.cookies = tempfile.mkstemp(suffix='.cookies')
        self.BASECMD = ['curl', '-s']
        self.BASECMD += ['-c', self.cookies, '-b', self.cookies]
        self.BASECMD += ['-D', self.headers]
        self.BASECMD += list(curl_opts)

    def __del__(self):
        os.unlink(self.cookies)
        os.unlink(self.headers)

    def __parse_headers(self):
        res = {}
        code = None
        with open(self.headers) as f:
            for line in f:
                if line[:5] == "HTTP/":
                    code = line.split(' ')[1]
                else:
                    l = line.split(':')
                    if len(l) > 1:
                        res[l[0].strip()] = (':'.join(l[1:])).strip()
        return code, res

    def __request(self, *cmd):
        body = subprocess.check_output(self.BASECMD+list(cmd))
        code, headers = self.__parse_headers()
        return Response(code, headers, body)

    def get(self, url, maxfollows=10):
        response = self.__request(url)
        if maxfollows > 0 and response.redirect and 'Location' in response.headers:
            response = self.get(response.headers['Location'], maxfollows-1)
        return response

    def post(self, url, data={}, maxfollows=10):
        payload = '&'.join('%s=%s'%(key, data[key]) for key in data)
        response = self.__request('-X', 'POST', '-d', payload, url)
        if maxfollows > 0 and response.redirect and 'Location' in response.headers:
            response = self.get(response.headers['Location'], maxfollows-1)
        return response
