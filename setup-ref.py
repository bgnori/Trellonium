#!/usr/bin/python
# -*- coding=utf-8 -*-

import os.path

import requests

from commons import objnames, dirname

source = "https://trello.com/docs/api/"

for name in objnames:
    got = requests.get(source + "/".join([name, "index.html"]))
    print "got ", got.url
    print got.headers
    with file(os.path.join(dirname, name+".html"), 'w') as f:
        f.write(got.content.encode("utf8"))


