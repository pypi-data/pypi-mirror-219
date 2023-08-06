# This file is placed in the Public Domain.
#
# pylint: disable=C0413,C0115,C0116,E1101
# pylama: ignore=W0611,E303,E402


"""
    >>> from genocide import Object
    >>> o = Object()
    >>> o.o = Object()
    >>> o.o.a = "test"
    >>> print(o)
    {"o": {"a": "test"}}

"""


__author__ = "Bart Thate <programmingobject@gmail.com>"


import unittest


from genocide.recurse import readrec, writerec
from genocide.objects import Object


class TestRecursive(unittest.TestCase):

    def testrecursive(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        pth = writerec(obj)
        readrec(obj, pth)
        self.assertEqual(obj.obj.a, "test")
