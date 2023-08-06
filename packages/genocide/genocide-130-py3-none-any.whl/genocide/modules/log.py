# This file is placed in the Public Domain.


"log text"


__author__ = "Bart Thate <programmingobject@gmail.com>"


# IMPORTS


import time


from ..objects import Object, find, fntime, write
from ..repeats import elapsed


# CLASSES


class Log(Object):

    "log objects"

    def __init__(self):
        super().__init__()
        self.createtime = time.time()
        self.txt = ''

    def __size__(self):
        return len(self.txt)

    def __since__(self):
        return self.createtime


# COMMANDS


def log(event):
    "log text"
    if not event.rest:
        nmr = 0
        for obj in find('log'):
            lap = elapsed(time.time() - fntime(obj.__oid__))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply('no log')
        return
    obj = Log()
    obj.txt = event.rest
    write(obj)
    event.reply('ok')
