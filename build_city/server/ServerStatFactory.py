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
        log.info("some one down" + str(reason))

    def lineReceived(self, line):
        cs_msg = pb_compile.PATH.mycity_pb2.CSStatMsg()
        try:
            cs_msg.ParseFromString(line)

            # 使用观察者模式改写大循环？
            if cs_msg.type == pb_compile.PATH.mycity_pb2.RANK:
                self.FormRank()
            elif cs_msg.type == pb_compile.PATH.mycity_pb2.ONLINE:
                self.FormOnline()
            else:
                self.UnknownRequest()
        except:
            self.UnknownRequest()

    ##-------封装消息---------##
    def FormRank(self):
        sc_msg = pb_compile.PATH.mycity_pb2.SCStatMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.RANK
        sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        sc_msg.rank.append("aa:1000")
        sc_msg.rank.append("bb:2000")
        self.sendLine(sc_msg.SerializeToString())

    def FormOnline(self):
        sc_msg = pb_compile.PATH.mycity_pb2.SCStatMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.ONLINE
        sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        wait_num = 0
        wait_num = GameManager.GameManager().GetWaitingUserNum()
        sc_msg.online = wait_num
        self.sendLine(sc_msg.SerializeToString())

    def UnknownRequest(self):
        self.sendLine("{\"error\":\"undefine error\",\"b\":\"2\",\"a\":1}")

        
class ServerStatLinkFactory(ServerFactory):
    protocol = ServerStatLink

    def __init__(self):
        None