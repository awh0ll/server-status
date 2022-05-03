'''
Monitors ports n stuff.
'''

import logging
import socket
import os
import ssl
import datetime
import json
import time


def load_monitors():
    '''Load monitors from json file 'input.json' in root of project directory.'''
    with open("input.json", "r", encoding="utf-8") as input_file:
        logging.debug("Opening %s...", "input.json")
        data = json.load(input_file)

    return data['monitors']

def poll(mon):
    '''Given an arbitary monitor, polls it'''
    if mon['protocol'] == 'tcp':
        return poll_tcp(mon['host'], mon['port'])

    logging.error("Unknown monitor type: \n" + mon)
    return False

def poll_tcp(hostname, port):
    '''Returns true if a TCP socket can be successfully opened on the given host and port'''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))

        logging.info("%s up", hostname)
        return True
    except socket.error:
        logging.info("%s down", hostname)
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


def main():
    '''Main program loop.'''
    monitors = load_monitors()

    for monitor in monitors:
        logging.info("Loaded monitor for host: %s on port: %d", monitor['host'], monitor['port'])

    while True:
        for monitor in monitors:
            poll(monitor)

        time.sleep(15)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
