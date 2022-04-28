import socket
import os
import ssl
import datetime
import json

class Monitor:
    def __init__(self, hostname, port, protocol = "tcp", interval = 5) -> None:
        self.hostname = hostname
        self.port = port
        self.protocol = protocol
        self.interval = interval

#Load monitors from json file 'input.json' in root of project directory.
def load_monitors():
    f = open('input.json')

    data = json.load(f)

    return data['monitors']

#Returns true if a TCP socket can be successfully opened on the given host and port, false if not.
def poll_tcp(hostname, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
        return True
    except Exception as e:
        print(e)
        return False

#Returns true if host can be successfully pinged, false if not.
def ping(hostname):
    response = os.system("ping " + hostname)

    return response == 0

#Returns SSL certificate expiration date.
def get_ssl_expiry(hostname, port = 443):
    ssl_dateformat = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()

    #Configure connection, connect.
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname = hostname)
    conn.settimeout(5.0)
    conn.connect((hostname, port))

    #Get the cert
    cert = conn.getpeercert()

    #Return just date
    return datetime.datetime.strptime(cert['notAfter'], ssl_dateformat)

load_monitors()