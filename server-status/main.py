import socket
import os
import ssl
import datetime
from xmlrpc.client import Boolean

class Monitor:
    def __init__(self, hostname, port, protocol = "tcp", interval = 5) -> None:
        self.hostname = hostname
        self.port = port
        self.protocol = protocol
        self.interval = interval

def poll_tcp(hostname, port) -> Boolean:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
        return True
    except Exception as e:
        print(e)
        return False

def ping(hostname) -> Boolean:
    response = os.system("ping " + hostname)

    return response == 0

def get_ssl_expiry(hostname, port = 443):
    ssl_dateformat = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()

    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = hostname)

    conn.settimeout(5.0)

    conn.connect((hostname, port))
    cert = conn.getpeercert()

    return datetime.datetime.strptime(cert['notAfter'], ssl_dateformat)

