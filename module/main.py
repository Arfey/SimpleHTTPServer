__author__ = "Misha Gavela"

import socket
import webbrowser


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

RESPONSE_BODY_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
<head>
    <meta charset="UTF-8">
    <title>%(title)s</title>
</head>
<body>
    %(content)s
</body>
</html>
"""

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

    def echo_about_run(self) -> None:
        """Write in stdout message with info about start server"""
        print(ECHO_MESSAGES_TEMPLATE % dict(port=self.port, host=self.host))

    def send_response(self, title: str = 'http server', conent: str = '', status: str = status.HTTP_200_OK) -> None:
        """Send http responce to client"""
        body = RESPONSE_BODY_TEMPLATE % dict(
                    title='Main Title',
                    content="<h1>Hello world!!!</h1>")

        # include length of body for HTTP\1.1 protocol
        res = RESPONSE_HEADER_TEMPLATE % dict(
                    body=body,
                    status=status,
                    length=len(body))

        self.socket.send(res.encode())
        self.socket.close()

    def send_error(status: str=status.HTTP_404_NOT_FOUND) -> None:
        self.send_response(status=status)

    def start_forever(self) -> None:
        self.echo_about_run()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen(LISTEN_LIMIT)
            while True:
                self.socket, addr = sock.accept()
                data = self.socket.recv(1024)

                print(self.socket, addr, data)

                self.send_response()

                


if __name__ == "__main__":
    # Create simple server

    server = SimpleHTTPServer(host=HOST, port=PORT)

    webbrowser.open("0.0.0.0:%s" % PORT)

    server.start_forever()
