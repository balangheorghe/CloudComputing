import os
import time
import logging
import requests

def GetTime():
    localtime = time.localtime(time.time())
    return "{0:02}.{1:02}.{2:02} {3:02}.{4:02}.{5:02}".format(localtime.tm_year, localtime.tm_mon, localtime.tm_mday, localtime.tm_hour, localtime.tm_min, localtime.tm_sec)


def init_logging():
    logger = logging.getLogger("HybridAnalysis")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s]-%(message)s")
    dateformat = "{0}.log".format(GetTime())
    if not os.path.isdir("logs"): os.makedirs("logs")
    if not os.path.isdir(os.path.join("logs", "hybridanalysis")): os.makedirs(os.path.join("logs", "hybridanalysis"))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if os.path.isfile(".debug"):
        if not os.path.isdir(os.path.join("logs", "hybridanalysis", "debug")): os.makedirs(os.path.join("logs", "hybridanalysis", "debug"))
        file_handler = logging.FileHandler(os.path.join("logs", "hybridanalysis", "debug", dateformat))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if not os.path.isdir(os.path.join("logs", "hybridanalysis", "misc")): os.makedirs(os.path.join("logs", "hybridanalysis", "misc"))
    file_handler = logging.FileHandler(os.path.join("logs", "hybridanalysis", "misc", dateformat))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if not os.path.isdir(os.path.join("logs", "hybridanalysis", "err")): os.makedirs(os.path.join("logs", "hybridanalysis", "err"))
    file_handler = logging.FileHandler(os.path.join("logs", "hybridanalysis", "err", dateformat))
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # setam logger-ul nostru custom ca logger principal
    logging.root = logger
    return dateformat

def Main(hash_set):
    init_logging()
    main_dict = dict()
    params = {"apikey": "s0wc04w0skoco4okowckc0c4goowsggkkwcos0o4so4s080wssw0gs8ks0ws44k8",
              "secret": "676a17e53d21e3b74c0939a333beaed16bce008dc9a73fa5"}
    logging.info("Received: {}".format(hash_set))
    for item in hash_set:
        logging.info("Making the request for item {}".format(item))
        r = requests.get('https://www.hybrid-analysis.com/api/scan/{hash}'.format(hash=item),
                         params=params)
        response = r.json()
        custom_dict = dict()
        logging.info("Received: {}".format(response))
        if response["response_code"] == 0:
            for rsp in response["response"]:
                for value in rsp:
                    if value in ["threatlevel", "threatscore", "verdict", "domains", "hosts"]:
                        custom_dict[value] = rsp[value]
        main_dict[item] = custom_dict

        logging.info("Sleeping for 20 seconds...")
        time.sleep(20)

    logging.info("To return: {}".format(main_dict))
    return main_dict

# ab = set()
# ab.add("40c913b6837bb03dd168536710d88a05faa6a6956b1c210758a0979a6782bf62")
# Main(ab)