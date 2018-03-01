import os
import json
import cherrypy
import time
from socket import *
from apis import virus_total, hybrid_analysis, dasmalwerk
from jinja2 import Environment, FileSystemLoader

sock=socket()
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

class Server(object):
    def __init__(self):
        self.data = ""


    @cherrypy.expose
    def index(self):
        # templates_env = Environment(loader=FileSystemLoader(templates_dir))
        # template = templates_env.get_template('index.html')
        # # return template.render({})
        # return template.render({"input_dict": self.data})
        templates_env = Environment(loader=FileSystemLoader(templates_dir))
        template = templates_env.get_template('index.html')
        file_dict = dasmalwerk.Main()
        test_stuff = dict()
        for item in file_dict:
            test_stuff[item] = file_dict[item]
            break

        infos = hybrid_analysis.Main(test_stuff)
        main_result = dict()
        for item in infos:
            to_scan_url = set()
            if "domains" in infos[item]:
                for domain in infos[item]["domains"]:
                    to_scan_url.add(domain)
            if "hosts" in infos[item]:
                for host in infos[item]["hosts"]:
                    to_scan_url.add(host)

            result = virus_total.Main(to_scan_url)

            url_to_download = "http://dasmalwerk.eu/zippedMalware/{}".format(file_dict[item])
            main_result[item] = {"hybrid_analysis": infos[item], "virustotal": result, "url": "{}.zip".format(url_to_download)}

        print(main_result)
        return template.render({"input_dict": main_result})


if __name__ == '__main__':
    cherrypy.quickstart(Server(), "/", "server.conf")