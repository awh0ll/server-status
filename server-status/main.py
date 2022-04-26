import socket

def poll_http(host, port = 80):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return True
    except Exception as e:
        print(e)
        return False

if(poll_http("127.0.0.1")):
    print("it works!")
else:
    print("oh no!")