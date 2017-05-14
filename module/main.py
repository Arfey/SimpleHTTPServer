__author__ = "Misha Gavela"

import socket
import webbrowser


HOST, PORT = "", 8001
LISTEN_LIMIT = 1

SIMPLE_RESPONCSE = b"""HTTP/1.1 200 OK
    Date: Wed, 04 Jun 2014 20:35:29 GMT
    Server: Apache/2.2.17 (Unix)
    Set-Cookie: PHPSESSID=dc09f975147aa6011cac3177c1646625; path=/
    Expires: Thu, 19 Nov 1981 08:52:00 GMT
    Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
    Pragma: no-cache
    Content-Length: 263
    Keep-Alive: timeout=5, max=100
    Connection: Keep-Alive
    Content-Type: text/html

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
    <head>
    <title>Welcome to Python.com</title>    
    </head>
    <body>    
        <p>Hello world!!!</p>
    </body>
    <frameset rows="100%,*" frameborder=0 border=0>
    <frame name="main" src="inside.phtml?source=home&" frameborder="0">
    </frameset>
    </html>
    """

class SimpleServer:
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen(LISTEN_LIMIT)
            conn, addr = sock.accept()

        print(conn, addr)


        conn.send(SIMPLE_RESPONCSE)
        conn.close()


if __name__ == "__main__":
    # Create simple server

    server = SimpleServer()

    webbrowser.open("0.0.0.0:%s" % PORT)

    server.start()
