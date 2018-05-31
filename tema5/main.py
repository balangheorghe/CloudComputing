#!/usr/bin/env python3
import json                        
import requests
import random
import time
import paho.mqtt.client as mqtt
        
def request_all_devices():
	tt = requests.get("http://data.uradmonitor.com/api/v1/devices", headers = {"X-User-id":"4126", "X-User-hash":"063cf4fdf721e844980c6f3b8b6eddcf"})
	return tt.json()

def build_random_list(full_list):
	MIN = 2
	MAX = 5
	MAX = min(len(full_list), MAX)
	MIN = min(len(full_list), MIN)
	rr = random.randint(MIN, MAX)
	output_set = set()
	while True:
		if len(output_set) == rr:
			break
		output_set.add(random.choice(full_list))
	return output_set

def get_device(id):
	tt = requests.get("http://data.uradmonitor.com/api/v1/devices/{}".format(id), headers = {"X-User-id":"4126", "X-User-hash":"063cf4fdf721e844980c6f3b8b6eddcf"})
	return tt.json()

def get_ids(json):
	id_set = set()
	for item in json:
		id_set.add(item["id"])
	return id_set

def get_device_data(id, senzor, timer):
        tt = requests.get("http://data.uradmonitor.com/api/v1/devices/{}/{}/{}".format(id, senzor, timer), headers = {"X-User-id":"4126", "X-User-hash":"063cf4fdf721e844980c6f3b8b6eddcf"})
	return tt.json()


def get_client():
	client = mqtt.Client(client_id="urn:lo:nsid:cloud_project_device:dmig1")
	client.username_pw_set("json+device", "dc11eef728ed410bb992e801c7821a55")
	client.connect("liveobjects.orange-business.com", 1883, 60)
	return client
	

def main():
	all_dev = request_all_devices()
	all_ids = get_ids(all_dev)
	random_list = build_random_list(list(all_ids))

	client = get_client()	

	for item in random_list:
		device = get_device(item)
		random_senzors = build_random_list(device.keys())
		for senzor in random_senzors:
			data = get_device_data(item, senzor, 24 * 3600)
			time.sleep(30)
			for rt in data:
				duty = None
				altitude = None
				longitude = None
				time = None
				if "duty" in rt:
					duty = rt["duty"]
				if "altitude" in rt:
					altitude = rt["altitude"]
				if "longitude" in rt:
					longitude = rt["longitude"]
				if "time" in rt:
					time = rt["time"]

				new_dict = dict()
				new_dict["s"] = "data_flood"
				new_dict["ts"] = time
				new_dict["m"] = "model_1"
				new_dict["v"] = {"duty":duty, "altitude":altitude, "longitude":longitude} 
				new_dict["tags"] = ["custom_cloud_upload"]
				print("Publishing: {}".format(new_dict))
				client.publish("dev/data", json.dumps(new_dict))
	client.disconnect()

main()
	