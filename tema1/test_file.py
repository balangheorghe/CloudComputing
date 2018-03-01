from apis import virus_total, hybrid_analysis, dasmalwerk

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
    main_result[item] = {"hybrid_analysis": infos[item], "virustotal": result, "url":url_to_download}

