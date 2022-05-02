'''
Monitors ports n stuff.
'''

import socket
import os
import ssl
import datetime
import json
import time


def load_monitors():
    '''Load monitors from json file 'input.json' in root of project directory.'''
    with open("input.json", "r", encoding="utf-8") as input_file:
        data = json.load(input_file)

    return data['monitors']

def poll(mon):
    '''Given an arbitary monitor, polls it'''
    if mon['protocol'] == 'tcp':
        return poll_tcp(mon['host'], mon['port'])
    
    print("Unknown monitor type.")
    return False

def poll_tcp(hostname, port):
    '''Returns true if a TCP socket can be successfully opened on the given host and port'''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))

        print(hostname + " up")
        return True
    except socket.error:
        print(hostname + " down")
        return False

def ping(hostname):
    '''Returns true if host can be successfully pinged, false if not.'''
    response = os.system("ping " + hostname)

    return response == 0

def get_ssl_expiry(hostname, port = 443):
    '''Returns SSL certificate expiration date.'''
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

monitors = load_monitors()

for monitor in monitors:
    print(monitor)

while True:
    for monitor in monitors:
        poll(monitor)

    time.sleep(15)
