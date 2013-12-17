#!/usr/bin/python

import os.path
import model
import objs

model.init("/home/nori/Desktop/work/Trellonium/appkey.txt", "/home/nori/Desktop/work/Trellonium/secret.txt")

app = model.theApp
token_loc = "/home/nori/Desktop/work/Trellonium/token.txt"

if os.path.isfile(token_loc):
    app.token = file(token_loc).read().split()
    theBoard = objs.BoardProxy("52a113d948daf8a31e0043dd")
    xs = theBoard.lists()
    print xs
else:
    print app.token_url


