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

class SimpleServer:
    def __init__(self, *, host, port):
        self.host = host
        self.port = port

    def echo_about_run(self):
        print(ECHO_MESSAGES_TEMPLATE % dict(port=self.port, host=self.host))

    def start_forever(self):
        self.echo_about_run()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen(LISTEN_LIMIT)
            while True:
                conn, addr = sock.accept()
                data = conn.recv(1024)

                print(conn, addr, data)

                body = RESPONSE_BODY_TEMPLATE % dict(
                        title='Main Title',
                        content="<h1>Hello world!!!</h1>"
                    )
                res = RESPONSE_HEADER_TEMPLATE % dict(
                        body=body,
                        status="200 OK",
                        length=len(body)
                    )

                conn.send(res.encode())
                conn.close()


if __name__ == "__main__":
    # Create simple server

    server = SimpleServer(host=HOST, port=PORT)

    webbrowser.open("0.0.0.0:%s" % PORT)

    server.start_forever()
