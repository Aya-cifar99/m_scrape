import json
import os

with open(f"../core/properties/muvi_properties.json") as json_file:
    properties = json.load(json_file)

# MUVI - PROXY CREDENTIALS
PROXY_USERNAME = os.environ.get("PROXY_USERNAME")
PROXY_PASSWORD = os.environ.get("PROXY_PASSWORD")