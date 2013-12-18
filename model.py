#!/usr/bin/python

import re
import requests
import json

from urllib import quote_plus

from commons import objnames
from parsehtml import process



class AppConnection:
    urlwversion= "https://api.trello.com/1/"
    def __init__(self, key, secret, token=None):
        self.key = key
        self.secret = secret
        self.token = token

    def token_url(self, app_name, expiration='30days', write_access=True):
        url = self.urlwversion + "/".join(["authorize"])
        params = dict(key=self.key,
                name=app_name,
                expiration=expiration,
                response_type="token",
                scope='read,write' if write_access else 'read')
        req = requests.Request(method='GET', url=url, params=params)
        return req.full_url

    def GET(self, *paths):
        def f(**kw):
            url = self.urlwversion + "/".join(paths)
            params = dict(key=self.key, **kw)
            got = requests.get(url, params=params)
            return json.loads(got.content)
        return f

    def POST(self, *paths):
        def f(**kw):
            url = self.urlwversion + "/".join(paths)
            params = dict(key=self.key, token=self.token, **kw)
            got = requests.post(url, params=params)
            return got
            #return json.loads(got.content)
        return f

    def PUT(self, *paths):
        def f(value):
            url = self.urlwversion + "/".join(paths)
            params = dict(key=self.key, token=self.token, value=value)
            got = requests.put(url, params=params)
            return json.loads(got.content)
        return f


theApp = None


class TrelloProxy(object):
    fields = set([])
    _by_name = {}
    _by_path = {}

    def __init__(self, idstr):
        self.__dict__["idstr"] = idstr

    def __repr__(self):
        return "(%s, %s)"%(self.__class__.__name__, self.idstr)

    @staticmethod
    def build(source):
        rs = dict(GET={}, PUT={}, DELETE={}, POST={})
        for s in source:
            self.buildone(rs, s)
        return rs

    @staticmethod
    def _buildone(rs, d):
        xs = rs[d["method"]].get(d["entity"], None)
        if xs is None:
            xs = []
        xs.append(d["params"])
        rs[d["method"]][d["entity"]] = xs

    @classmethod
    def register(kls, subk):
        kls._by_name[subk.name] = subk
        kls._by_path[subk.path] = subk

    @classmethod
    def find_by_name(kls, name):
        return kls._by_name[name]

    @classmethod
    def find_by_path(kls, path):
        return kls._by_path[subk.path]

    @classmethod
    def create(kls, **kw):
        f = theApp.POST(kls.path)
        got = f(**kw)
        x = json.loads(got.content)
        return kls(x['id'])  #FIXME Need to cache other fields.

    def validate(self, method, path):
        m = self.availables[method]
        try:
            return path in m
        except:
            if '[field]' not in m:
                return False
            return path in self.fields

    def __getattr__(self, path):
        if self.validate("GET", path):
            def foo(**kw):
                f = theApp.GET(self.__class__.path, self.idstr, path)
                return [self.find_by_path(path)(x['id']) for x in f(**kw)]
            return foo
        elif '[field]' in self.availables["GET"]:
            if path in self.fields:
                return theApp.GET(self.__class__.path, self.idstr, path)
            else:
                raise "Bad Field %s for %s "%(path, self.__klass__)

    def __setattr__(self, path, value):
        if self.validate("PUT", path):
            f = theApp.PUT(self.__class__.path, self.idstr, path)
            print f(value)
        elif '[field]' in self.availables["PUT"]:
            if path in self.fields:
                return theApp.PUT(self.__class__.path, self.idstr, path)
            else:
                raise



def init(keyfile, secretfile):
    global theApp
    with file(keyfile, "r") as f:
        with file(secretfile, "r") as g:
            theApp = AppConnection(f.read().strip(), g.read().strip())

    for name, path in objnames.items():
        p = type(name, (TrelloProxy, ), dict(path=path, name=name))
        TrelloProxy.register(p)

if __name__  == "__main__":
    init("/home/nori/Desktop/work/Trellonium/appkey.txt", "/home/nori/Desktop/work/Trellonium/secret.txt")
    theApp.token = file("/home/nori/Desktop/work/Trellonium/token.txt").read().split()
    theBoard = TrelloProxy.find_by_name("board")("52a113d948daf8a31e0043dd")
    print theBoard




