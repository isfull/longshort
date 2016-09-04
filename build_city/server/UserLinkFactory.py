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
import base64

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

import User
import TaskRunner
import UserManager
import GameManager
import RoomGameManager
import common.GenId
import pb_compile.PATH.mycity_pb2
import common.Coding

log = logging.getLogger('City')


#
# put logic to thread pool
#
def _SendMessage(oUserLink, s):
    oUserLink.sendLine(s)

def ReactorSendMessage(oUserLink, s):
    ss = common.Coding.CityEncode(s)
    reactor.callFromThread(_SendMessage, oUserLink, ss)

def _ShutDown(oUserLink):
    oUserLink.m_game_stat = False
    oUserLink.transport.loseConnection()

def ReactorShutDown(oUserLink):
    reactor.callFromThread(_ShutDown, oUserLink)

# python 2.7只能给进程池传func，不能传类的func
def HandleRequest(oUserLink, line):
    cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
    try:
        cs_msg.ParseFromString(line)

        # 使用观察者模式改写大循环？
        # 是否是登录信息
        if cs_msg.type == pb_compile.PATH.mycity_pb2.ENTER_RANDOM:
            if cs_msg.HasField("cs1"):
                log.info("random room: uid"+cs_msg.cs1.uid+"|userinfo:"+cs_msg.cs1.userinfo)
                oUserLink.m_user = User.User(cs_msg.cs1.userinfo, cs_msg.cs1.uid, cs_msg.cs1.username, "-1", oUserLink)
                UserManager.UserManager().AddUser(oUserLink.m_user)
                if GameManager.GameManager().AddUser(cs_msg.cs1.uid) == False:
                    sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
                    sc_msg.type = pb_compile.PATH.mycity_pb2.ENTER_RANDOM
                    sc_msg.error = pb_compile.PATH.mycity_pb2.ERROR
                    ReactorSendMessage(oUserLink, sc_msg.SerializeToString()) 
                else:
                    sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
                    sc_msg.type = pb_compile.PATH.mycity_pb2.ENTER_RANDOM
                    sc_msg.error = pb_compile.PATH.mycity_pb2.OK
                    ReactorSendMessage(oUserLink, sc_msg.SerializeToString())
            else:
                print("ENTER_RANDOM not exist")
        elif cs_msg.type == pb_compile.PATH.mycity_pb2.ENTER_FRIEND:
            if cs_msg.HasField("cs2"):
                log.info("friend room: uid"+cs_msg.cs2.uid+"|userinfo:"+cs_msg.cs2.userinfo)
                oUserLink.m_user = User.User(cs_msg.cs2.userinfo, cs_msg.cs2.uid, cs_msg.cs2.username, cs_msg.cs2.roomid, oUserLink)
                UserManager.UserManager().AddUser(oUserLink.m_user)
                if RoomGameManager.RoomGameManager().AddUser(cs_msg.cs2.uid, cs_msg.cs2.roomid) == False:
                    sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
                    sc_msg.type = pb_compile.PATH.mycity_pb2.ENTER_FRIEND
                    sc_msg.error = pb_compile.PATH.mycity_pb2.NO_ROOM_PLACE
                    ReactorSendMessage(oUserLink, sc_msg.SerializeToString()) 
                else:
                    sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
                    sc_msg.type = pb_compile.PATH.mycity_pb2.ENTER_FRIEND
                    sc_msg.error = pb_compile.PATH.mycity_pb2.OK
                    ReactorSendMessage(oUserLink, sc_msg.SerializeToString())
            else:
                print("ENTER_FRIEND not exist")
        # 登陆后信息处理
        else:
            if oUserLink.m_user == None:
                ReactorSendMessage(oUserLink, b"please login")
            else:
                oUserLink.m_user.Handle(cs_msg)
    except Exception as e:
        log.info("error:"+str(e))
        ReactorSendMessage(oUserLink, b"unknow request")

#
# User link protocol
#
class UserLink(LineReceiver):

    delimiter = "\x00"
    m_user = None
    m_game_stat = False

    def connectionMade(self):
        log.info("some one on")
        self.m_game_stat = True
        #self.sendLine("stat server ok!")

    def connectionLost(self, reason):
        log.info("some one down"+str(reason))
        if self.m_user != None and self.m_game_stat == True:
            self.m_user.ClientDown()


    def lineReceived(self, line):
        #log.info("receive:"+line)
        ss = common.Coding.CityDecode(line)
        # 使用观察者模式改写大循环？
        TaskRunner.DoProto(HandleRequest, self, ss)
        
        
class UserLinkFactory(ServerFactory):
    protocol = UserLink

    def __init__(self):
        None