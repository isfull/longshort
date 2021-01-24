#!/usr/bin/env python
# -*- coding: utf8 -*-
#
import os
import sys
import time
import datetime
import struct
import socket
import logging
import socket_client_simple

logger = logging.getLogger('common')

TTY_ENCODING = sys.getfilesystemencoding()


def main():
    s = socket_client_simple.SocketSimple(("127.0.0.1", 31000))
    rt = s.Connect()
    if rt:
        req = "{\"buzid\":\"test\",\"data\":{\"channel\":\"1\",\"version\":\"1.1\"},\"version\":\"1\"}"
        s.DelimiterSend(req, "\0")
        rsp = s.DelimiterRecieve()
        print("a:" + rsp)
        req = "{\"buzid\":\"test\",\"data\":{\"channel\":\"1\",\"version\":\"1.1\"},\"version\":\"1\"}"
        s.DelimiterSend(req, "\0")
        rsp = s.DelimiterRecieve()
        print("b:" + rsp)
        s.Close()
    else:
        print("connect fail")
    return


if __name__ == "__main__":
    import gc

    gc.set_debug(gc.DEBUG_LEAK)

    main()
