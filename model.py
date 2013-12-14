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


class TrelloProxy:
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


class BoardProxy(TrelloProxy):
    path = "boards"
    fields = set(["name", "desc", "descData", "closed", "idOrganization",
        "invited", "pinned", "url", "prefs", "invitations", "memberships",
        "shortLink", "subscribed", "labelNames", "powerUps", "dateLastActivity",
        "dateLastView", "shortUrl"])

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

TrelloProxy.register(BoardProxy)


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

    availables = TrelloProxy.build(methods) #FIXME
    fields = set(["badges", "checkItemStates", "closed", "dateLastActivity",
        "desc", "descData", "due", "idBoard", "idChecklists", "idList",
        "idMembers", "idMembersVoted", "idShort", "idAttachmentCover",
        "manualCoverAttachment", "labels", "name", "pos", "shortLink",
        "shortUrl", "subscribed", "url",])

TrelloProxy.register(CardProxy)


class CheckListProxy(TrelloProxy):
    path = "checklists"
    fields = set(["name", "idBoard", "idCard", "pos"])
    methods = """
    GET /1/checklists/[idChecklist]
    GET /1/checklists/[idChecklist]/[field]
    GET /1/checklists/[idChecklist]/board
    GET /1/checklists/[idChecklist]/board/[field]
    GET /1/checklists/[idChecklist]/cards
    GET /1/checklists/[idChecklist]/cards/[filter]
    GET /1/checklists/[idChecklist]/checkItems
    GET /1/checklists/[idChecklist]/checkItems/[idCheckItem]
    PUT /1/checklists/[idChecklist]
    PUT /1/checklists/[idChecklist]/idCard
    PUT /1/checklists/[idChecklist]/name
    PUT /1/checklists/[idChecklist]/pos
    POST /1/checklists
    POST /1/checklists/[idChecklist]/checkItems
    DELETE /1/checklists/[idChecklist]
    DELETE /1/checklists/[idChecklist]/checkItems/[idCheckItem]
    """
    availables = TrelloProxy.build(methods) #FIXME

TrelloProxy.register(CheckListProxy)


class ListProxy(TrelloProxy):
    path = "lists"
    fields = set(["name", "closed", "idCard", "pos", "subscribed"])
    methods = """
    GET /1/lists/[idList]
    GET /1/lists/[idList]/[field]
    GET /1/lists/[idList]/actions
    GET /1/lists/[idList]/board
    GET /1/lists/[idList]/board/[field]
    GET /1/lists/[idList]/cards
    GET /1/lists/[idList]/cards/[filter]
    PUT /1/lists/[idList]
    PUT /1/lists/[idList]/closed
    PUT /1/lists/[idList]/idBoard
    PUT /1/lists/[idList]/name
    PUT /1/lists/[idList]/pos
    PUT /1/lists/[idList]/subscribed
    POST /1/lists
    POST /1/lists/[idList]/archiveAllCards
    POST /1/lists/[idList]/cards
    """
    availables = TrelloProxy.build(methods) #FIXME

TrelloProxy.register(ListProxy)


class MemberProxy(TrelloProxy):
    path = "members"
    fields = set(["avatarHash", "bio", "bioData", "confirmed",
        "fullName", "idPremOrgsAdmin", "initials", "memberType",
        "products", "status", "url", "username", "avatarSource",
        "email", "gravatarHash", "idBoards", "idBoardsInvited",
        "idBoardsPinned", "idOrganizations", "idOrganizationsInvited",
        "loginTypes", "newEmail", "oneTimeMessagesDismissed", "prefs",
        "status", "trophies", "uploadedAvatarHash", "premiumFeatures"])
    methods = """
    GET /1/members/[idMember or username]
    GET /1/members/[idMember or username]/[field]
    GET /1/members/[idMember or username]/actions
    GET /1/members/[idMember or username]/boardBackgrounds
    GET /1/members/[idMember or username]/boardBackgrounds/[idBoardBackground]
    GET /1/members/[idMember or username]/boardStars
    GET /1/members/[idMember or username]/boards
    GET /1/members/[idMember or username]/boards/[filter]
    GET /1/members/[idMember or username]/boardsInvited
    GET /1/members/[idMember or username]/boardsInvited/[field]
    GET /1/members/[idMember or username]/cards
    GET /1/members/[idMember or username]/cards/[filter]
    GET /1/members/[idMember or username]/customBoardBackgrounds
    GET /1/members/[idMember or username]/customBoardBackgrounds/[idBoardBackground]
    GET /1/members/[idMember or username]/customEmoji
    GET /1/members/[idMember or username]/customEmoji/[idCustomEmoji]
    GET /1/members/[idMember or username]/customStickers
    GET /1/members/[idMember or username]/customStickers/[idCustomSticker]
    GET /1/members/[idMember or username]/notifications
    GET /1/members/[idMember or username]/notifications/[filter]
    GET /1/members/[idMember or username]/organizations
    GET /1/members/[idMember or username]/organizations/[filter]
    GET /1/members/[idMember or username]/organizationsInvited
    GET /1/members/[idMember or username]/organizationsInvited/[field]
    GET /1/members/[idMember or username]/sessions
    GET /1/members/[idMember or username]/tokens
    PUT /1/members/[idMember or username]
    PUT /1/members/[idMember or username]/avatarSource
    PUT /1/members/[idMember or username]/bio
    PUT /1/members/[idMember or username]/boardBackgrounds/[idBoardBackground]
    PUT /1/members/[idMember or username]/boardStars/[idBoardStar]
    PUT /1/members/[idMember or username]/customBoardBackgrounds/[idBoardBackground]
    PUT /1/members/[idMember or username]/fullName
    PUT /1/members/[idMember or username]/initials
    PUT /1/members/[idMember or username]/prefs/colorBlind
    PUT /1/members/[idMember or username]/prefs/minutesBetweenSummaries
    PUT /1/members/[idMember or username]/username
    POST /1/members/[idMember or username]/avatar
    POST /1/members/[idMember or username]/boardBackgrounds
    POST /1/members/[idMember or username]/boardStars
    POST /1/members/[idMember or username]/customBoardBackgrounds
    POST /1/members/[idMember or username]/customEmoji
    POST /1/members/[idMember or username]/customStickers
    POST /1/members/[idMember or username]/idBoardsPinned
    POST /1/members/[idMember or username]/oneTimeMessagesDismissed
    POST /1/members/[idMember or username]/unpaidAccount
    DELETE /1/members/[idMember or username]/boardBackgrounds/[idBoardBackground]
    DELETE /1/members/[idMember or username]/boardStars/[idBoardStar]
    DELETE /1/members/[idMember or username]/customBoardBackgrounds/[idBoardBackground]
    DELETE /1/members/[idMember or username]/customStickers/[idCustomSticker]
    DELETE /1/members/[idMember or username]/idBoardsPinned/[idBoard]
    """
    availables = TrelloProxy.build(methods) #FIXME

TrelloProxy.register(MemberProxy)


def init(keyfile, secretfile):
    global theApp
    with file(keyfile, "r") as f:
        with file(secretfile, "r") as g:
            theApp = AppConnection(f.read().strip(), g.read().strip())



