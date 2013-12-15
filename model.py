#!/usr/bin/python

import re
import requests
import json

from urllib import quote_plus

source = "https://trello.com/docs/api/index.html"
pattern = re.compile(
    r"    (?P<method>[A-Z]+) /(?P<version>\d+)/(?P<object_name>\w+)/(?P<object_id>\[[^]]+\])/?(?P<entity>[^/]*)/?(?P<params>.*)")



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
    knowns = {}

    def __init__(self, idstr):
        self.__dict__["idstr"] = idstr

    def __repr__(self):
        return "(%s, %s)"%(self.__class__.__name__, self.idstr)

    @staticmethod
    def build(methods):
        rs = dict(GET={}, PUT={}, DELETE={}, POST={})
        for line in methods.splitlines():
            m = pattern.match(line)
            if m:
                d = m.groupdict()
                xs = rs[d["method"]].get(d["entity"], None)
                if xs is None:
                    xs = []
                xs.append(d["params"])
                rs[d["method"]][d["entity"]] = xs
        return rs

    @classmethod
    def register(kls, subk):
        kls.knowns[subk.path] = subk

    @classmethod
    def create(kls, **kw):
        f = theApp.POST(kls.path)
        got = f(**kw)
        x = json.loads(got.content)
        return kls.knowns[kls.path](x['id']) 

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
            if path in self.knowns:
                def foo(**kw):
                    f = theApp.GET(self.__class__.path, self.idstr, path)
                    return [self.knowns[path](x['id']) for x in f(**kw)]
                return foo
            return theApp.GET(self.__class__.path, self.idstr, path)
        elif '[field]' in self.availables["GET"]:
            if path in self.fields:
                return theApp.GET(self.__class__.path, self.idstr, path)
            else:
                raise

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



