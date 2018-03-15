import json
import logging
import os
import socket
import sqlite3
import threading

logger = logging.getLogger("WebServer")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)
logging.root = logger


def _connect_to_db(db_path):
    logging.info("Connecting to: {}".format(db_path))
    con = sqlite3.connect(db_path)
    return con


def get_function(parameters):
    global db_path
    _DB_CON_ = _connect_to_db(db_path)
    logging.info("Calling get function with parameters: {}".format(parameters))
    item = parameters[0]
    items = item.split(" ")
    if len(items) == 2:
        return construct_response(400, "Bad Request")
    else:
        item = items[1].strip("/")

        if len(item) == 0:
            st = _DB_CON_.execute("SELECT * from exploits").fetchall()
            tt = {"status_code": 1, "result": st}
            return append_dict(construct_response(200, "OK"), tt)
        if len(item) != 32:
            tt = {"status_code": -1, "result": "Invalid md5"}
            return append_dict(construct_response(400, "Bad Request"), tt)

        st = _DB_CON_.execute("SELECT * from exploits where md5='{}'".format(item)).fetchall()
        if len(st) == 0:
            tt = {"status_code": 0}
        else:
            tt = {"status_code": 1, "result": [{"md5": st[0][0], "description": st[0][1]}]}

    return append_dict(construct_response(200, "OK"), tt)


def put_function(parameters):
    logging.info("Calling put function with parameters: {}".format(parameters))
    md5 = ''
    description = ''
    for item in parameters:
        if "md5" in item:
            md5 = item.split("\"md5\":")[1].split('"')[1].split('"')[0]
            description = item.split("\"details\":")[1].split('"')[1].split('"')[0]
    if md5 == '' or description == '':
        tt = {"md5":md5, "description": description}
        return append_dict(construct_response(400, "Bad Request"), tt)

    items = parameters[0].split(" ")
    item = items[1].strip("/")

    _DB_CON_ = _connect_to_db(db_path)
    if len(item) == 0:
        _DB_CON_.execute("INSERT into exploits values('{}', '{}')".format(md5, description))
        st = _DB_CON_.execute("SELECT * from exploits where md5='{}'".format(md5)).fetchall()
        _DB_CON_.commit()
        if len(st) != 0:
            tt = {"status_code": 1, "result": json.dumps(st)}
            return append_dict(construct_response(200, "OK"), tt)
        else:
            tt = {"status_code": 0, "result": "Something went wrong"}
            return append_dict(construct_response(200, "OK"), tt)
    elif len(item) == 32:
        st = _DB_CON_.execute("SELECT * from exploits where md5='{}'".format(md5)).fetchall()
        _DB_CON_.commit()
        if len(st) != 0:
            st = _DB_CON_.execute("UPDATE exploits set details = '{}' where md5='{}'".format(description, md5))
            st = _DB_CON_.execute("SELECT * from exploits where md5='{}'".format(item)).fetchall()
            _DB_CON_.commit()
            tt = {"status_code": 1, "result": json.dumps(st)}
            return append_dict(construct_response(200, "OK"), tt)
        else:
            tt = {"status_code": 0, "result": "Something went wrong"}
            return append_dict(construct_response(200, "OK"), tt)
    else:
        tt = {"status_code": -1, "result": "Invalid md5"}
        return append_dict(construct_response(400, "Bad Request"), tt)


def post_function(parameters):
    logging.info("Calling post function with parameters: {}".format(parameters))
    _DB_CON_ = _connect_to_db(db_path)
    _DB_CON_.execute("DELETE from exploits")
    new_result = []
    for item in parameters:
        if "md5" in item:
            results = item.split(",")
            counter = 0
            rez = {"md5":None, "details":None}
            for tt in results:
                if "md5" in tt:
                    md5 = tt.split("\"md5\":")[1].split('"')[1].split('"')[0]
                    rez = {"md5": md5, "details":None}
                if "details" in tt:
                    description = tt.split("\"details\":")[1].split('"')[1].split('"')[0]
                    rez["details"] = description
                    new_result.append(rez.copy())
    for item in new_result:
        _DB_CON_.execute("INSERT into exploits values('{}','{}')".format(item["md5"], item["details"]))
    _DB_CON_.commit()
    return construct_response(202, "Accepted")


def delete_function(parameters):
    logging.info("Calling update function with parameters: {}".format(parameters))
    global db_path
    _DB_CON_ = _connect_to_db(db_path)
    logging.info("Calling get function with parameters: {}".format(parameters))
    item = parameters[0]
    items = item.split(" ")
    if len(items) == 2:
        return construct_response(400, "Bad Request")
    else:
        item = items[1].strip("/")

        if len(item) == 0:
            st = _DB_CON_.execute("DELETE from exploits")
            tt = {"status_code": 1, "result": "all datas have been deleted"}
            st = _DB_CON_.execute("SELECT * from exploits").fetchall()
            _DB_CON_.commit()
            if len(st) == 0:
                tt = {"status_code": 1, "result": "ALL DATA HAS BEEN DELETED"}
                return append_dict(construct_response(200, "OK"), tt)
            else:
                tt = {"status_code": 0, "result": "Something went wrong"}
                return append_dict(construct_response(200, "OK"), tt)
        if len(item) != 32:
            tt = {"status_code": -1, "result": "Invalid md5"}
            return append_dict(construct_response(400, "Bad Request"), tt)

        st = _DB_CON_.execute("DELETE from exploits where md5='{}'".format(item))
        st = _DB_CON_.execute("SELECT * from exploits where md5='{}'".format(item)).fetchall()
        _DB_CON_.commit()
        if len(st) == 0:
            tt = {"status_code": 1, "result": "DATA HAS BEEN DELETED"}
            return append_dict(construct_response(200, "OK"), tt)
        else:
            tt = {"status_code": 0, "result": "Something went wrong"}
            return append_dict(construct_response(200, "OK"), tt)


possible_requests = {
    "get": get_function,
    "put": put_function,
    "post": post_function,
    "delete": delete_function,
}


def construct_response(code, text):
    response = ''
    response += 'HTTP/1.1 {} {}\r\n'.format(code, text)
    response += 'Connection: close\r\n\r\n'
    return response.encode()


def append_dict(response, dict):
    response = response.decode()
    response += json.dumps(dict)
    response = response.encode()
    return response


def server_function(client, address):
    logging.info("[server function][connection] client: {} | address: {}".format(client, address))
    while True:
        packet = client.recv(4096).decode()
        packet = packet.split("\r\n")
        logging.info("packet:\n{}".format(packet))
        method = packet[0].split(" ")[0].lower()
        if method not in possible_requests:
            response = construct_response(400, "Bad Request")
        else:
            response = possible_requests[method](packet)
        logger.info(packet)
        logging.info("sending response: {}".format(response))
        client.send(response)
        client.close()
        break


host = socket.gethostname()
port = int(input("Please insert the server port: "))
html_docs = str(input("Please insert the directory path for your resources: "))

logging.info("Preparing to start the server {}:{} | Resource location: {}".format(host, port, html_docs))
logging.info("Creating the server...")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host, port))
serversocket.listen(5)
logger.info("Server has started...")

db_path = os.path.join(html_docs, "data")

while True:
    (client, address) = serversocket.accept()
    logging.info("[new connection] client: {} | address: {}".format(client, address))
    threadObj = threading.Thread(target=server_function, args=(client, address))
    threadObj.start()
