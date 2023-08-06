class server:
    def __init__(self):
        self.routes = {}

    def site(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def serve(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')
        func = self.routes.get(path)

        if func:
            response_body = func()
            status = '200 OK'
        else:
            response_body = 'Not Found'
            status = '404 Not Found'

        headers = [('Content-Type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [response_body.encode()]

    def run(self, host='localhost', port=8080):
        from wsgiref.simple_server import make_server
        server = make_server(host, port, self.serve)
        print(f"Serving on {host}:{port}...")
        server.serve_forever()
