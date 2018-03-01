import os
import time
import logging
import requests

def GetTime():
    localtime = time.localtime(time.time())
    return "{0:02}.{1:02}.{2:02} {3:02}.{4:02}.{5:02}".format(localtime.tm_year, localtime.tm_mon, localtime.tm_mday, localtime.tm_hour, localtime.tm_min, localtime.tm_sec)


def init_logging():
    logger = logging.getLogger("VirusTotalAPI")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s]-%(message)s")
    dateformat = "{0}.log".format(GetTime())
    if not os.path.isdir("logs"): os.makedirs("logs")
    if not os.path.isdir(os.path.join("logs", "virustotal")): os.makedirs(os.path.join("logs", "virustotal"))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if os.path.isfile(".debug"):
        if not os.path.isdir(os.path.join("logs", "virustotal", "debug")): os.makedirs(os.path.join("logs", "virustotal", "debug"))
        file_handler = logging.FileHandler(os.path.join("logs", "virustotal", "debug", dateformat))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if not os.path.isdir(os.path.join("logs", "virustotal", "misc")): os.makedirs(os.path.join("logs", "virustotal", "misc"))
    file_handler = logging.FileHandler(os.path.join("logs", "virustotal", "misc", dateformat))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if not os.path.isdir(os.path.join("logs", "virustotal", "err")): os.makedirs(os.path.join("logs", "virustotal", "err"))
    file_handler = logging.FileHandler(os.path.join("logs", "virustotal", "err", dateformat))
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # setam logger-ul nostru custom ca logger principal
    logging.root = logger
    return dateformat

def Main(hash_set):
    init_logging()
    response_dict = dict()
    logging.info("Received: {}".format(hash_set))
    for item in hash_set:
        params = {'apikey': '5fb57c7a20fa55b264a17ac0fa2e12b290f172ac1cb86b2b18aa25192e11c82e',
                  'url': '{}'.format(item)}
        logging.info("Making the scan request for item: {}".format(item))
        response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
        json_response = response.json()
        logging.info("Response: {}".format(json_response))
        logging.info("Sleeping for 30 seconds...")
        time.sleep(30)
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "gzip,  My Python requests library example client or username"
        }
        params = {'apikey': '5fb57c7a20fa55b264a17ac0fa2e12b290f172ac1cb86b2b18aa25192e11c82e',
                  'resource': '{}'.format(item)}
        logging.info("Making the report request for item: {}".format(item))
        response = requests.post('http://www.virustotal.com/vtapi/v2/url/report', data=params, headers=headers)
        json_response = response.json()
        logging.info("Response: {}".format(json_response))
        temp_dict = dict()
        if "positives" in json_response:
            temp_dict["positives"] = json_response["positives"]
        # if "scans" in json_response:
        #     temp_dict["scans"] = json_response["scans"]
        logging.info("adding {} in dict for item {}".format(temp_dict, item))
        response_dict[item] = temp_dict

    logging.info("To return: {}".format(response_dict))
    return response_dict
#
# ab = set()
# ab.add("http://www.virustotal.com")
# Main(ab)




