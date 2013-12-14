#!/usr/bin/python

import os.path

import requests

source = "https://trello.com/docs/api/"

dirname = "fromRef"

objnames = ["action", "board", "card", "checklist", "member", "notification", "organaization", "search", "token", "type", "webhook", ]


for name in objnames:
    got = requests.get(source + "/".join([name, "index.html"]))
    print "got ", got.url 
    with file(os.path.join(dirname, name+".html"), 'w') as f:
        f.write(got.content)



