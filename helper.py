#!/usr/bin/python

import model

model.init("/home/nori/Desktop/work/Trellonium/appkey.txt", "/home/nori/Desktop/work/Trellonium/secret.txt")

app = model.theApp
app.token = file("/home/nori/Desktop/work/Trellonium/token.txt").read().split()

theBoard = model.BoardProxy("52a113d948daf8a31e0043dd")
xs = theBoard.lists()
theList = model.ListProxy(xs[0]['id'])
ys = theList.cards()
theCard = model.CardProxy(ys[0]['id'])

