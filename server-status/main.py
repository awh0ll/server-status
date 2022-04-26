import socket

def poll_tcp(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return True
    except Exception as e:
        print(e)
        return False


if(poll_tcp("127.0.0.1", 443)):
    print("it works!")
else:
    print("oh no!")