#!/usr/bin/python

import re

class PathFrag(object):
    pass

class PathFragText(PathFrag):
    def __init__(self, t):
        self.t = t
    def __repr__(self):
        return "<PathFragText: %s>"%(self.t)
    
    def realize(self, **kw):
        return self.t

class PathFragVariable(PathFrag):
    def __init__(self, t):
        self.ts = []
        for x in re.split(' or ', t.strip('[]')):
            y = re.split('[ _]', x)
            if 'id' in y:
                if len(y) == 1:
                    pass
                elif len(y) == 2:
                    y = [y[1], y[0].capitalize()]
                else:
                    raise
            self.ts.append(''.join(y))

    def __repr__(self):
        return "<PathFragVariable: %s>"%(self.ts)

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
                try:
                    y = PathFragVariable(x)
                except:
                    print path_text
                    raise
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
        if len(self.frags) < 5:
            return "[field]"
        else:
            return self.frags[4].realize(field='[field]')

