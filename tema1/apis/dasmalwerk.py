import os
import time
import logging
import requests

def GetTime():
    localtime = time.localtime(time.time())
    return "{0:02}.{1:02}.{2:02} {3:02}.{4:02}.{5:02}".format(localtime.tm_year, localtime.tm_mon, localtime.tm_mday, localtime.tm_hour, localtime.tm_min, localtime.tm_sec)


def init_logging():
    logger = logging.getLogger("DasMalwerk")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s]-%(message)s")
    dateformat = "{0}.log".format(GetTime())
    if not os.path.isdir("logs"): os.makedirs("logs")
    if not os.path.isdir(os.path.join("logs", "dasmalwerk")): os.makedirs(os.path.join("logs", "dasmalwerk"))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if os.path.isfile(".debug"):
        if not os.path.isdir(os.path.join("logs", "dasmalwerk", "debug")): os.makedirs(os.path.join("logs", "dasmalwerk", "debug"))
        file_handler = logging.FileHandler(os.path.join("logs", "dasmalwerk", "debug", dateformat))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if not os.path.isdir(os.path.join("logs", "dasmalwerk", "misc")): os.makedirs(os.path.join("logs", "dasmalwerk", "misc"))
    file_handler = logging.FileHandler(os.path.join("logs", "dasmalwerk", "misc", dateformat))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if not os.path.isdir(os.path.join("logs", "dasmalwerk", "err")): os.makedirs(os.path.join("logs", "dasmalwerk", "err"))
    file_handler = logging.FileHandler(os.path.join("logs", "dasmalwerk", "err", dateformat))
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # setam logger-ul nostru custom ca logger principal
    logging.root = logger
    return dateformat

def Main():
    init_logging()
    logging.info("Preparing the request...")
    response = requests.get('http://dasmalwerk.eu/api')
    response = response.json()
    logging.info("Received response: {}".format(response))
    hash_set = dict()
    for item in response["items"]:
        if "Hashvalue" in item:
            logging.info("Received hash: {}".format(item["Hashvalue"]))
            hash_set[item["Hashvalue"]] = None
            if "Filename" in item:
                logging.info("Hash: {} has name: {}".format(item["Hashvalue"], item["Filename"]))
                hash_set[item["Hashvalue"]] = item["Filename"]

    logging.info("To return hashset: {}".format(hash_set))
    return hash_set