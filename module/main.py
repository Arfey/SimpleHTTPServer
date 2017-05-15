__author__ = "Misha Gavela"

import socket
import webbrowser


HOST, PORT = "", 8000
LISTEN_LIMIT = 1

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
    def start_forever(self):
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

    server = SimpleServer()

    # webbrowser.open("0.0.0.0:%s" % PORT)

    server.start_forever()
