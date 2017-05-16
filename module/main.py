__author__ = "Misha Gavela"

import socket
import webbrowser
import re
import os


__all__ = ["BaseHTTPStatus", "status", ]


HOST, PORT = "0.0.0.0", 8000
LISTEN_LIMIT = 1


ECHO_MESSAGES_TEMPLATE = "\nServing HTTP \
on %(host)s port %(port)s (http://%(host)s:%(port)s) ...\n"

RESPONSE_HEADER_TEMPLATE = """HTTP/1.1 %(status)s
    Content-Length: %(length)s
    Keep-Alive: timeout=5, max=100
    Connection: Keep-Alive
    Content-Type: text/html

    %(body)s
"""

NOT_FOUND_TEMPLATE = """\
<h3>Not Found 404</h3>
"""

RESPONSE_BODY_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
<head>
    <meta charset="UTF-8">
    <title>%(title)s</title>
</head>
<body class="row">
    <div class="col-lg-12">
        <h2>Directory listing for <mark>%(path)s</mark></h1>
        <ul>
            %(content)s
        </ul>
    </div>
</body>
</html>
"""

RESPONSE_BODY_FILE_TEMPLATE = """%(content)s"""

DIR_TEMPLATE = "<li><a href='%(path)s'>%(name)s</a>/</li>"
FILE_TEMPLATE = "<li><a href='%(path)s'>%(name)s</a></li>"

class BaseHTTPStatus:
    """Singleton object for getting http status"""
    def __new__(cls, *args, **kwargs):
        if cls.instance:
            return cls.instance

        cls.instance = super().__new__(cls, *args, **kwargs)

        return cls.instance

    # Needing for get values, like simple attributes
    def __getattr__(self, value):
        if value in self.status:
            return self.status.get(value)

    instance = None

    status = {
        "HTTP_200_OK": "200 OK",
        "HTTP_404_NOT_FOUND": "404 Not found",
    }

status = BaseHTTPStatus()

class SimpleHTTPServer:
    def __init__(self, *, host: str, port: str):
        self.host = host
        self.port = port
        self.socket = None
        self.path = "/"
        self.module_path = os.path.dirname(os.path.abspath(__file__))

    def echo_about_run(self) -> None:
        """Write in stdout message with info about start server"""
        print(ECHO_MESSAGES_TEMPLATE % dict(port=self.port, host=self.host))

    def get_relative_path(self, path: str) -> str:
        """Return path relative to module path for link"""
        return os.path.relpath(path, self.module_path)

    def parsing_request(self, headers: str) -> None:
        """Parsing url and send response"""
        path = self.get_url_path(headers)

        full_path = os.path.dirname(os.path.abspath(__file__)) + path

        # send 404 if path is not found
        if not os.path.exists(full_path):
            return self.send_error()

        if os.path.isfile(full_path):
            return self.send_response_file(path=full_path)

        content = ''

        # generate too lists of dirs and file
        # del dirs[:] make deep=1
        for _, dirs, files in os.walk(full_path):
            for dr in dirs:
                pth = self.get_relative_path(full_path + '/' + dr)
                content += DIR_TEMPLATE % dict(path=pth, name=dr)

            for file in files:
                pth = self.get_relative_path(full_path + '/' + file)
                content += FILE_TEMPLATE % dict(path=pth, name=file)

            del dirs[:]

        self.send_response(content=content)

    def get_url_path(self, headers):
        """Return path of headers"""
        path = re.search(r"(/[^\s]*)", headers.decode("utf-8")).group() #@TODO: before searching, compile expression

        print("HTTP\1.1 ", path)
        self.path = path

        return path

    def send_response(self,
                      title: str = 'http server',
                      content: str = '',
                      template=RESPONSE_BODY_TEMPLATE,
                      status: str = status.HTTP_200_OK) -> None:
        """Send http responce to client"""
        body = template % dict(
                    title='Main Title',
                    content=content,
                    path=self.path)

        # include length of body for HTTP\1.1 protocol
        res = RESPONSE_HEADER_TEMPLATE % dict(
                    body=body,
                    status=status,
                    length=len(body))

        self.socket.send(res.encode())
        self.socket.close()

    def send_response_file(self, *args, path, **kwargs):
        with open(path, 'r') as file:
            content = file.read()

        self.send_response(*args, 
                           content=content,
                           template=RESPONSE_BODY_FILE_TEMPLATE,
                           **kwargs)

    def send_error(self, status: str=status.HTTP_404_NOT_FOUND) -> None:
        self.send_response(status=status, content=NOT_FOUND_TEMPLATE)

    def start_forever(self) -> None:
        self.echo_about_run()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen(LISTEN_LIMIT)
            while True:
                self.socket, addr = sock.accept()
                data = self.socket.recv(1024)

                # print(self.socket, addr, data)
                self.parsing_request(data)


if __name__ == "__main__":
    # Create simple server

    server = SimpleHTTPServer(host=HOST, port=PORT)

    webbrowser.open("0.0.0.0:%s" % PORT)

    server.start_forever()
