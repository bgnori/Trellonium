#!/usr/bin/python

import model
import objs

model.init("/home/nori/Desktop/work/Trellonium/appkey.txt", "/home/nori/Desktop/work/Trellonium/secret.txt")

app = model.theApp
app.token = file("/home/nori/Desktop/work/Trellonium/token.txt").read().split()

theBoard = objs.BoardProxy("52a113d948daf8a31e0043dd")
xs = theBoard.lists()

