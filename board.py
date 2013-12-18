#!/usr/bin/python

from commons import objnames, dirname
from model import TrelloProxy

from parsehtml import process

klassfields = dict(
    path = "boards",
    fields = set(["name", "desc", "descData", "closed", "idOrganization",
        "invited", "pinned", "url", "prefs", "invitations", "memberships",
        "shortLink", "subscribed", "labelNames", "powerUps", "dateLastActivity",
        "dateLastView", "shortUrl"])
    )

BoardProxy = type('BoardProxy', (TrelloProxy, ), klassfields)

BoardProxy.availables = TrelloProxy.build("    GET /1/boards/[board_id]/cards")
TrelloProxy.register(BoardProxy)


if __name__ == "__main__":
    import model
    model.init("/home/nori/Desktop/work/Trellonium/appkey.txt", "/home/nori/Desktop/work/Trellonium/secret.txt")
    app = model.theApp
    app.token = file("/home/nori/Desktop/work/Trellonium/token.txt").read().split()
    theBoard = BoardProxy("52a113d948daf8a31e0043dd")
    print theBoard
    print theBoard.cards()

