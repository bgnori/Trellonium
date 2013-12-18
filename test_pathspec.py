#!/usr/bin/python

import unittest

import pathspec


class TestFragValiable(unittest.TestCase):
    def test_A(self):
        self.assertIn('idBoard', pathspec.PathFragVariable("[board_id").ts)

    def test_B(self):
        self.assertIn('idBoard', pathspec.PathFragVariable("[board id").ts)

    def test_C(self):
        self.assertIn('idCard', pathspec.PathFragVariable("[card id or shorturl").ts)

    def test_D(self):
        self.assertIn('shorturl', pathspec.PathFragVariable("[card id or shorturl").ts)


class TestPathSpec(unittest.TestCase):
    def setUp(self):
        self.path = "/1/boards/[board_id]/cards"
        self.ps = pathspec.PathSpec(self.path)
        self.ps1 = pathspec.PathSpec("/1/boards/[board_id]/members/[idMember]")

    def test_hash(self):
        self.assertEqual(hash(self.path), hash(self.ps))

    def test_realize(self):
        self.assertEqual('/1/boards/123/cards', self.ps.realize(idBoard='123'))

    def test_realize1(self):
        self.assertEqual('/1/boards/123/members/345', self.ps1.realize(idBoard='123', idMember='345'))


if __name__ == "__main__":
    unittest.main()
