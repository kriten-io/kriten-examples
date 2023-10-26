import json
import os
import re

extra_vars = os.environ.get("EXTRA_VARS")
#
# Parse extra_vars
# Expecting JSON string eg. '{"macaddress": "00:50:56:9a:25:71"}'
#
if extra_vars:
    data = json.loads(extra_vars)
    mac = data.get("macaddress")
    #
    # Logic to find macaddress in the network goes here.
    # We will fake it :~)
    #
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
        print(f"MAC address: {mac} found on switch uk-lon-57 port 7/36.")
    else:
        print(f"I don't recognise this MAC address: {mac}.")
        print("MAC address must be 12 hex digits, with each pair separated by ':' or '-'.")
