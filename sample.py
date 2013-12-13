#!/usr/bin/python

import model


model.init("/home/nori/Desktop/work/Trellonium/appkey.txt", "/home/nori/Desktop/work/Trellonium/secret.txt")


b = model.BoardProxy("52a113d948daf8a31e0043dd")
print b.members()
xs = b.lists()
print xs
print xs[0]["id"]


app = model.theApp
print app.token_url("bgnoritest")

app.token = file("/home/nori/Desktop/work/Trellonium/token.txt").read().split()

c = model.CardProxy.create_card(idList=xs[0]["id"], name="by bot", due="null")

print c
