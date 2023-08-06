"""
Where the work takes place.
"""

import copy
import pprint
import socket
import ssl


def _read_wordlist(wordlist_path):
    words = []
    if not wordlist_path:
        return words
    with open(wordlist_path) as f:
        words = [line.strip() for line in f.read().splitlines()
                 if not line.startswith("#")]
    return words


def _read_req(request_path):
    headers = {}
    with open(request_path) as f:
        start_line = f.readline().strip()
        for line in f.read().splitlines():
            key, value = line.split(":", 1)
            headers.update({key: value.strip()})

    return start_line, headers


def start(request, header, target, wordlist_path=None):
    wordlist = _read_wordlist(wordlist_path)
    start_line_orig, req_headers_orig = _read_req(request)

    context = ssl.create_default_context()
    context.check_hostname = 0
    context.verify_mode = ssl.CERT_NONE

    for i, word in enumerate(wordlist):
        req_headers = copy.deepcopy(req_headers_orig)
        start_line = start_line_orig
        if "REPLACEME" in req_headers[header]:
            req_headers[header] = req_headers[header].replace("REPLACEME",
                                                              word)
        elif "REPLACEME" in start_line:
            start_line = start_line.replace("REPLACEME", word)
        else:
            req_headers[header] = word
        data = str.encode(start_line + "\r\n")
        for key, val in req_headers.items():
            data += str.encode(key)
            data += str.encode(": ")
            data += str.encode(val)
            data += str.encode("\r\n")
        data += str.encode("\r\n")

        target_and_port = target.split(":")
        conn = context.wrap_socket(socket.socket(socket.AF_INET),
                                   server_hostname=target_and_port[0])

        if len(target_and_port) == 1:
            conn.connect((target_and_port[0], 443))
        else:
            conn.connect((target_and_port[0], target_and_port[1]))
        conn.sendall(data)

        print("########### Test case {i} ###########")
        print("###### SENT")
        pprint.pprint(data.split(b"\r\n"))
        print("###### RECEIVED")
        pprint.pprint(conn.recv(4096).split(b"\r\n"))
        conn.close()
        print("################ END ################")
