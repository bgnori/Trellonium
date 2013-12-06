#!/usr/bin/python

import re
import requests
import json

source = "https://trello.com/docs/api/index.html"
pattern = re.compile(
    r"    (?P<method>[A-Z]+) /(?P<version>\d+)/boards/\[board_id\]/?(?P<entity>[^/]*)/?(?P<params>.*)")


def empty():
    return dict(GET={}, PUT={}, DELETE={}, POST={})

class AppConnection:
    urlwversion= "https://api.trello.com/1/" 
    def __init__(self, key):
        self.key = key

    def GET(self, *paths): 
        def f(**kw):
            url = self.urlwversion + "/".join(paths)
            params = dict(key=self.key, **kw)
            got = requests.get(url, params=params)
            return json.loads(got.content)
        return f 

theApp = None

class TrelloProxy:
    def __init__(self, idstr):
        self.idstr = idstr

    def validate(self, method, path):
        return bool(self.availables[method][path])

    def __getattr__(self, path):
        if self.validate("GET", path):
            return theApp.GET(self.__class__.path, self.idstr, path)
        else:
            raise

class BoardProxy(TrelloProxy):
    path = "boards"
    methods = """
    GET /1/boards/[board_id]
    GET /1/boards/[board_id]/[field]
    GET /1/boards/[board_id]/actions
    GET /1/boards/[board_id]/cards
    GET /1/boards/[board_id]/cards/[filter]
    GET /1/boards/[board_id]/cards/[idCard]
    GET /1/boards/[board_id]/checklists
    GET /1/boards/[board_id]/lists
    GET /1/boards/[board_id]/lists/[filter]
    GET /1/boards/[board_id]/members
    GET /1/boards/[board_id]/members/[filter]
    GET /1/boards/[board_id]/members/[idMember]/cards
    GET /1/boards/[board_id]/membersInvited
    GET /1/boards/[board_id]/membersInvited/[field]
    GET /1/boards/[board_id]/memberships
    GET /1/boards/[board_id]/memberships/[idMembership]
    GET /1/boards/[board_id]/myPrefs
    GET /1/boards/[board_id]/organization
    GET /1/boards/[board_id]/organization/[field]
    PUT /1/boards/[board_id]
    PUT /1/boards/[board_id]/closed
    PUT /1/boards/[board_id]/desc
    PUT /1/boards/[board_id]/idOrganization
    PUT /1/boards/[board_id]/labelNames/blue
    PUT /1/boards/[board_id]/labelNames/green
    PUT /1/boards/[board_id]/labelNames/orange
    PUT /1/boards/[board_id]/labelNames/purple
    PUT /1/boards/[board_id]/labelNames/red
    PUT /1/boards/[board_id]/labelNames/yellow
    PUT /1/boards/[board_id]/members
    PUT /1/boards/[board_id]/members/[idMember]
    PUT /1/boards/[board_id]/memberships/[idMembership]
    PUT /1/boards/[board_id]/myPrefs/emailPosition
    PUT /1/boards/[board_id]/myPrefs/idEmailList
    PUT /1/boards/[board_id]/myPrefs/showListGuide
    PUT /1/boards/[board_id]/myPrefs/showSidebar
    PUT /1/boards/[board_id]/myPrefs/showSidebarActivity
    PUT /1/boards/[board_id]/myPrefs/showSidebarBoardActions
    PUT /1/boards/[board_id]/myPrefs/showSidebarMembers
    PUT /1/boards/[board_id]/name
    PUT /1/boards/[board_id]/prefs/background
    PUT /1/boards/[board_id]/prefs/calendarFeedEnabled
    PUT /1/boards/[board_id]/prefs/cardAging
    PUT /1/boards/[board_id]/prefs/cardCovers
    PUT /1/boards/[board_id]/prefs/comments
    PUT /1/boards/[board_id]/prefs/invitations
    PUT /1/boards/[board_id]/prefs/permissionLevel
    PUT /1/boards/[board_id]/prefs/selfJoin
    PUT /1/boards/[board_id]/prefs/voting
    PUT /1/boards/[board_id]/subscribed
    POST /1/boards
    POST /1/boards/[board_id]/calendarKey/generate
    POST /1/boards/[board_id]/checklists
    POST /1/boards/[board_id]/emailKey/generate
    POST /1/boards/[board_id]/lists
    POST /1/boards/[board_id]/markAsViewed
    POST /1/boards/[board_id]/powerUps
    DELETE /1/boards/[board_id]/members/[idMember]
    DELETE /1/boards/[board_id]/powerUps/[powerUp]"""

    availables = empty()
    for line in methods.splitlines():
        m = pattern.match(line)
        if m:
            d = m.groupdict()
            xs = availables[d["method"]].get(d["entity"], None)
            if xs is None:
                xs = []
            xs.append(d["params"])
            availables[d["method"]][d["entity"]] = xs


theApp = AppConnection(file("appkey.txt", "r").read().strip())

b = BoardProxy("52a113d948daf8a31e0043dd")
#print b.memnbers
#print b.members
print b.lists()

