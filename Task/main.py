from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import socket
from A_server_socket import run_server
from threading import Thread
import logging

UDP_IP = ''
UDP_PORT = 5000


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        logging.debug("do_post")
        send_to_socket(data)

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)
        logging.debug("do_get")

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(f'files/{filename}', 'rb') as fd:
            self.wfile.write(fd.read())


def run_HTTPserver(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def send_to_socket(data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(data, (UDP_IP, UDP_PORT))
    logging.debug("send_to_socket")


def run_web_app():
    thread_socket_server = Thread(target=run_server,
                                  args=(UDP_IP, UDP_PORT))
    thread_socket_server.start()
    thread_HTTP_server = Thread(target=run_HTTPserver,
                                args=(HTTPServer, HttpHandler))
    thread_HTTP_server.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(threadName)s %(message)s')
    run_web_app()
