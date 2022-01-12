#!/usr/bin/env python3

import json
import sys

def main(argv):
	print("1")
	with open("data.json") as infile:
		obj = json.loads(infile.read())
	print("2")
	for item_name in obj["items"]:
		item = obj["items"][item_name]
		if item["sinkPoints"] == None or item["sinkPoints"] == 0:
			continue
		recipe = {}
		recipe["slug"] = "sink-point"
		recipe["name"] = "Sink Point"
		recipe["className"] = "Recipe_SinkPoint_" + item["className"]
		recipe["alternate"] = False
		recipe["time"] = 1
		recipe["manuelTimeMultiplier"] = 1
		recipe["ingredients"] = [{"item": item["className"], "amount": 1}]
		recipe["forBuilding"] = False
		recipe["inMachine"] = True
		recipe["inhand"] = True
		recipe["inWorkshop"] = False
		recipe["products"] = [{"item": "Desc_ResourceSinkCoupon_C", "amount": item["sinkPoints"]}]
		recipe["producedIn"] = ["Desc_ResourceSink_C"]
		recipe["isVariablePower"] = False
		obj["recipes"][recipe["className"]] = recipe
	print("3")
	with open("data.json", "w") as outfile:
		outfile.write(json.dumps(obj, indent=4))
	print("4")

if __name__ == '__main__':
	main(sys.argv)
