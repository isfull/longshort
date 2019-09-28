# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 , Inc. All Rights Reserved
#
################################################################################
"""
client call for server stat.

Authors: allen
Date:    2016/05/03
"""
import logging

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

import UserManager
import GameManager
import pb_compile.PATH.mycity_pb2

log = logging.getLogger('City')
# This is just about the simplest possible protocol
class ServerStatLink(LineReceiver):
    #self.factory
    delimiter = b"\0"

    def connectionMade(self):
        log.info("some query stat")
        

    def connectionLost(self, reason):
        log.info("some stat one down" + str(reason))

    def lineReceived(self, line):
        cs_msg = pb_compile.PATH.mycity_pb2.CSStatMsg()
        try:
            cs_msg.ParseFromString(line)
            log.info("stat server receive:"+repr(cs_msg))

            # 使用观察者模式改写大循环？
            call_time = cs_msg.time
            self.FormStat(call_time)
        except:
            self.FormStat("-1")

    ##-------封装消息---------##
    def FormStat(self, calltime):
        wait = GameManager.GameManager().GetWaitingUserNum()
        sc_msg = pb_compile.PATH.mycity_pb2.SCStatMsg()
        sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        sc_msg.time = calltime
        sc_msg.version = "1.2"
        sc_msg.waitnum = str(wait)
        log.info("stat server send:"+repr(sc_msg))
        self.sendLine(sc_msg.SerializeToString())

        
class ServerStatLinkFactory(ServerFactory):
    protocol = ServerStatLink

    def __init__(self):
        None
