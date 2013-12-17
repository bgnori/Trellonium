#!/usr/bin/python

import os.path

from lxml import etree

from commons import objnames, dirname


class Handler(object):
    def __init__(self, name):
        self.name = name

    def handle(self, t):
        for found in self.handle_root(t):
            print found

    def handle_root(self, t):
        for n in t.xpath("//div[@id=$id]/div", id=self.name):
            yield self.handle_node(n)

    def handle_node(self, node):
        d = {}
        d["id"] = node.attrib['id']
        for s in node.xpath("h2"):
            d["method"] = s.text
        for s in node.xpath("h2/span"):
            d["path_text"] = s.text
        for m in node.xpath('ul/li[strong/text()="Required permissions:"]/text()'):
            d["permission_text"] = m
        for m in node.xpath('ul/li[strong/text()="Arguments"]'):
            d["argument"] = self.handle_argument(m)
        #for m in n.xpath("ul/li/ul/li"):
        #    print m.text
        print d
        return d

    def handle_argument(self, node):
        argspec = {}
        for p in node.xpath('ul/li[tt/span[@class="pre"]]'):
            paramspec = self.handle_param(p)
            argspec[paramspec["name"]] = paramspec
        return argspec

    def handle_param(self, node):
        d = {}
        d["name"] = node.xpath('tt/span/text()')[0]
        d["op_text"] = node.xpath('tt/following-sibling::text()[1]')[0]
        d["is_required"] = d["op_text"].strip(" ()") == "required"
        d["is_optional"] = d["op_text"].strip(" ()") == "optional"
        d["default"] = node.xpath('ul/li[strong/text()="Default:"]/text()')
        d["vv"] = set(node.xpath('ul/li[strong/text()="Valid Values:"]/ul/li/tt/span/text()'))
        d["description"] = text = node.xpath('ul/li[strong/text()="Valid Values:"]/text()')
        return d



def process(name):
    h = Handler(name)
    with file(os.path.join(dirname, name+".html"), 'r') as f:
        p = etree.HTMLParser()
        t = etree.parse(f, p)
        h.handle(t)


if __name__  == "__main__":
    process("card")
    
    for name in objnames:
        pass

