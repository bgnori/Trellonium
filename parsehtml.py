#!/usr/bin/python

import os.path

from lxml import etree

from commons import objnames, dirname


class Handler(object):
    def __init__(self, name):
        self.name = name

    def handle(self, t):
        self.handle_root(t)

    def handle_root(self, t):
        print t
        for n in t.xpath("//div[@id=$id]/div", id=self.name):
            print n
            self.handle_node(n)

    def handle_node(self, node):
        print "id:", node.attrib['id']
        for s in node.xpath("h2"):
            print "method:", s.text
        for s in node.xpath("h2/span"):
            print "path:", s.text
        for m in node.xpath('ul/li[strong/text()="Required permissions:"]/text()'):
            print 'permissions:', m
        for m in node.xpath('ul/li[strong/text()="Arguments"]/ul/li'):
            self.handle_argument(m)
        #for m in n.xpath("ul/li/ul/li"):
        #    print m.text

    def handle_argument(self, node):
        print node.xpath('tt/span[@class="pre"]/text()')[0]
        xs = node.xpath('ul/li[strong/text()="Valid Values:"]/ul/li/tt/span/text()')
        if not xs:
            xs = ['descriptive'] + node.xpath('ul/li[strong/text()="Valid Values:"]/text()')
        print xs


def process(name):
    h = Handler(name)
    with file(os.path.join(dirname, name+".html"), 'r') as f:
        p = etree.HTMLParser()
        t = etree.parse(f, p)
        h.handle(t)

for name in objnames:
    pass

process("card")
