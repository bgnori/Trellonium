#!/usr/bin/python

import os.path

from lxml import etree


dirname = "fromRef"
objnames = ["action", "board", "card", "checklist", "member", "notification", "organaization", "search", "token", "type", "webhook", ]


keywords = {
        "Required permissions:": None,
        "Arguments": None,
        "Valid Values:": None,
        }

def handle_argument(node):
    print node.xpath('tt/span[@class="pre"]/text()')[0]
    xs = node.xpath('ul/li[strong/text()="Valid Values:"]/ul/li/tt/span/text()')
    if not xs:
        xs = ['descriptive'] + node.xpath('ul/li[strong/text()="Valid Values:"]/text()')
    print xs


def handle_node(node):
    print "id:", node.attrib['id']
    for s in node.xpath("h2"):
        print "method:", s.text
    for s in node.xpath("h2/span"):
        print "path:", s.text
    for m in node.xpath('ul/li[strong/text()="Required permissions:"]/text()'):
        print 'permissions:', m
    for m in node.xpath('ul/li[strong/text()="Arguments"]/ul/li'):
        handle_argument(m)
    #for m in n.xpath("ul/li/ul/li"):
    #    print m.text


def process(name):
    with file(os.path.join(dirname, name+".html"), 'r') as f:
        p = etree.HTMLParser()
        t = etree.parse(f, p)
        for n in t.xpath("//*[@id=$id]/div", id=name):
            print "-"*30
            handle_node(n)

for name in objnames:
    pass

process("board")
