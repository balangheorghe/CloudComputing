import requests
import time
r = requests.get ('http://dasmalwerk.eu/api')
table = r.json()

for item in table["items"]:
    if "Hashvalue" in item:
        time.sleep(30)
        print(item["Hashvalue"])
        params = {"apikey": "s0wc04w0skoco4okowckc0c4goowsggkkwcos0o4so4s080wssw0gs8ks0ws44k8", "secret":"676a17e53d21e3b74c0939a333beaed16bce008dc9a73fa5"}
        r = requests.get('https://www.hybrid-analysis.com/api/scan/{hash}'.format(hash=item["Hashvalue"]), params=params)
        response = r.json()
        if response["response_code"] == 0:
            for rsp in response["response"]:
                for value in rsp:
                    if value in ["threatlevel", "threatscore", "verdict", "domains", "hosts"]:
                        print(value, rsp[value])

"""
API Key	s0wc04w0skoco4okowckc0c4goowsggkkwcos0o4so4s080wssw0gs8ks0ws44k8
Secret	676a17e53d21e3b74c0939a333beaed16bce008dc9a73fa5
"""

# r = requests.get()