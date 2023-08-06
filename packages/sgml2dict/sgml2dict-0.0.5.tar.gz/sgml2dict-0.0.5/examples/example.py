#!/usr/bin/python3

import json
import sgml2dict

text = "<hello world/></hello>"

data = sgml2dict.convert(text)

print("Dictionary view:", data)
print("JSON view:", json.dumps(data))
