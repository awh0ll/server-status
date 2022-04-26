import socket
import os

def poll_tcp(hostname, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
        return True
    except Exception as e:
        print(e)
        return False

def ping(hostname):
    response = os.system("ping " + hostname)

    return response == 0

if ping("google.com"):
    print("it works!")
else:
    print("oh no!")