#!/usr/bin/python

import re
import requests
import json

from urllib import quote_plus

source = "https://trello.com/docs/api/index.html"
pattern = re.compile(
    r"    (?P<method>[A-Z]+) /(?P<version>\d+)/boards/\[board_id\]/?(?P<entity>[^/]*)/?(?P<params>.*)")


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


theApp = None

class TrelloProxy:
    def __init__(self, idstr):
        self.__dict__["idstr"] = idstr

    @staticmethod
    def build(methods):
        availables = dict(GET={}, PUT={}, DELETE={}, POST={})
        for line in methods.splitlines():
            m = pattern.match(line)
            if m:
                d = m.groupdict()
                xs = availables[d["method"]].get(d["entity"], None)
                if xs is None:
                    xs = []
                xs.append(d["params"])
                availables[d["method"]][d["entity"]] = xs
        return availables

    def validate(self, method, path):
        return bool(self.availables[method][path])

    def __getattr__(self, path):
        if self.validate("GET", path):
            return theApp.GET(self.__class__.path, self.idstr, path)
        else:
            raise

    def __setattr__(self, path, value):
        if self.validate("POST", path):
            f = theApp.POST(self.__class__.path, self.idstr, path)
            print f(**value)
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

    availables = TrelloProxy.build(methods) #FIXME

class CardProxy(TrelloProxy):
    path = "cards"
    methods = """
    GET /1/cards/[card id or shortlink]
    GET /1/cards/[card id or shortlink]/[field]
    GET /1/cards/[card id or shortlink]/actions
    GET /1/cards/[card id or shortlink]/attachments
    GET /1/cards/[card id or shortlink]/attachments/[idAttachment]
    GET /1/cards/[card id or shortlink]/board
    GET /1/cards/[card id or shortlink]/board/[field]
    GET /1/cards/[card id or shortlink]/checkItemStates
    GET /1/cards/[card id or shortlink]/checklists
    GET /1/cards/[card id or shortlink]/list
    GET /1/cards/[card id or shortlink]/list/[field]
    GET /1/cards/[card id or shortlink]/members
    GET /1/cards/[card id or shortlink]/membersVoted
    GET /1/cards/[card id or shortlink]/stickers
    GET /1/cards/[card id or shortlink]/stickers/[idSticker]
    PUT /1/cards/[card id or shortlink]
    PUT /1/cards/[card id or shortlink]/actions/[idAction]/comments
    PUT /1/cards/[card id or shortlink]/checklist/[idChecklist]/checkItem/[idCheckItem]/name
    PUT /1/cards/[card id or shortlink]/checklist/[idChecklist]/checkItem/[idCheckItem]/pos
    PUT /1/cards/[card id or shortlink]/checklist/[idChecklist]/checkItem/[idCheckItem]/state
    PUT /1/cards/[card id or shortlink]/checklist/[idChecklistCurrent]/checkItem/[idCheckItem]
    PUT /1/cards/[card id or shortlink]/closed
    PUT /1/cards/[card id or shortlink]/desc
    PUT /1/cards/[card id or shortlink]/due
    PUT /1/cards/[card id or shortlink]/idAttachmentCover
    PUT /1/cards/[card id or shortlink]/idBoard
    PUT /1/cards/[card id or shortlink]/idList
    PUT /1/cards/[card id or shortlink]/idMembers
    PUT /1/cards/[card id or shortlink]/labels
    PUT /1/cards/[card id or shortlink]/name
    PUT /1/cards/[card id or shortlink]/pos
    PUT /1/cards/[card id or shortlink]/stickers/[idSticker]
    PUT /1/cards/[card id or shortlink]/subscribed
    POST /1/cards
    POST /1/cards/[card id or shortlink]/actions/comments
    POST /1/cards/[card id or shortlink]/attachments
    POST /1/cards/[card id or shortlink]/checklist/[idChecklist]/checkItem
    POST /1/cards/[card id or shortlink]/checklist/[idChecklist]/checkItem/[idCheckItem]/convertToCard
    POST /1/cards/[card id or shortlink]/checklists
    POST /1/cards/[card id or shortlink]/idMembers
    POST /1/cards/[card id or shortlink]/labels
    POST /1/cards/[card id or shortlink]/markAssociatedNotificationsRead
    POST /1/cards/[card id or shortlink]/membersVoted
    POST /1/cards/[card id or shortlink]/stickers
    DELETE /1/cards/[card id or shortlink]
    DELETE /1/cards/[card id or shortlink]/actions/[idAction]/comments
    DELETE /1/cards/[card id or shortlink]/attachments/[idAttachment]
    DELETE /1/cards/[card id or shortlink]/checklist/[idChecklist]/checkItem/[idCheckItem]
    DELETE /1/cards/[card id or shortlink]/checklists/[idChecklist]
    DELETE /1/cards/[card id or shortlink]/idMembers/[idMember]
    DELETE /1/cards/[card id or shortlink]/labels/[color]
    DELETE /1/cards/[card id or shortlink]/membersVoted/[idMember]
    DELETE /1/cards/[card id or shortlink]/stickers/[idSticker]
    """

    @classmethod
    def create_card(kls, **kw):
        #idList, name, desc=None, pos=None, due=None,
        #    labels=None, idMembers=None, idCardSource=None,
        #    keepFromSource=None):
        """
    POST /1/cards
Arguments
    name (required)
        Valid Values: a string with a length from 1 to 16384
    desc (optional)
        Valid Values: a string with a length from 0 to 16384
    pos (optional)
        Default: bottom
        Valid Values: A position. top, bottom, or a positive number.
    due (required)
        Valid Values: A date, or null
    labels (optional)
    idList (required)
        Valid Values: id of the list that the card should be added to
    idMembers (optional)
        Valid Values: A comma-separated list of objectIds, 24-character hex strings
    idCardSource (optional)
        Valid Values: The id of the card to copy into a new card.
    keepFromSource (optional)
        Default: all
        Valid Values: Properties of the card to copy over from the source.
        """
        f = theApp.POST(kls.path)
        return f(**kw)
    

def init(keyfile, secretfile):
    global theApp
    with file(keyfile, "r") as f:
        with file(secretfile, "r") as g:
            theApp = AppConnection(f.read().strip(), g.read().strip())



