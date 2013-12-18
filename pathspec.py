#!/usr/bin/python

import re

class PathFrag(object):
    def __repr__(self):
        return "<PathFrag%s>"%(self.path_text)

class PathFragText(PathFrag):
    def __init__(self, t):
        self.t = t
    def realize(self, **kw):
        return self.t

class PathFragVariable(PathFrag):
    def __init__(self, t):
        self.ts = []
        for x in re.split(' or ', t.strip('[]')):
            y = re.split('[ _]', x)
            if 'id' in y:
                assert len(y) == 2
                y = [y[1], y[0].capitalize()]
            self.ts.append(''.join(y))

    def realize(self, **kw):
        for t in self.ts:
            x = kw.get(t, None)
            if x:
                return x
        return "===err==="

class PathSpec(object):
    def __init__(self, path_text):
        self.path_text = path_text
        xs = path_text.split('/')
        self.frags = []
        for x in xs:
            if x.startswith('['):
                y = PathFragVariable(x)
            else:
                y = PathFragText(x)
            self.frags.append(y)

    def __hash__(self):
        return hash(self.prop_name)

    def __repr__(self):
        return "<PathSpec %s>"%(self.path_text)

    def realize(self, **kw):
        return "/".join(frag.realize(**kw) for frag in self.frags)

    @property
    def prop_name(self):
        return self.frags[4].realize()


