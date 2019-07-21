# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import print_function
import base64

import time
from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

import common.GenId
import pb_compile.PATH.mycity_pb2

# 房间测试
# 废弃

class EchoClient(LineReceiver):
    delimiter = "\x00"
    end = "Bye-bye!"
    uid = ""
    userinfo = ""
    roomid = "1234"


    def connectionMade(self):
        self.uid = str(time.time())
        self.userinfo = "some info"
        self.roomid = "1234"
        self.connectionMade2()

    def lineReceived(self, line):
        print("recv:"+line)
        a = base64.b64decode(line)
        self.lineReceived2(a)
    def mysendLine(self, line):
        self.sendLine(base64.b64encode(line))
    #
    def connectionMade1(self):
        #self.mysendLine("random_match")
        cs_msg = pb_compile.PATH.mycity_pb2.CSStatMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.ONLINE
        self.mysendLine(cs_msg.SerializeToString())

    def lineReceived1(self, line):
        sc_msg = pb_compile.PATH.mycity_pb2.SCStatMsg()
        sc_msg.ParseFromString(line)
        if sc_msg.type == pb_compile.PATH.mycity_pb2.RANK:
                for rr in sc_msg.rank:
                    print("rank->"+rr)
        elif sc_msg.type == pb_compile.PATH.mycity_pb2.ONLINE:
            if sc_msg.HasField('online'):
                print("online:"+str(sc_msg.online))
        else:
            print("undefine")


    ###############################随机房间########################
    def connectionMade2(self):
        #self.mysendLine("random_match")
        cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.ENTER_RANDOM
        cs_msg.cs1.uid = self.uid
        cs_msg.cs1.username = "test1"
        cs_msg.cs1.userinfo = self.userinfo
        self.mysendLine(cs_msg.SerializeToString())

    def lineReceived2(self, line):
        print("-----------------------")
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        
        try:
            sc_msg.ParseFromString(line)
            # enter room
            if sc_msg.type == pb_compile.PATH.mycity_pb2.ENTER_RANDOM:
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("enter rand ok")
                else:
                    print("enter rand error")
            # enter loading
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.RANDOM_BROADCAST_BEGIN:
                if sc_msg.HasField("sc2"):
                    print("mapid:"+sc_msg.sc2.mapid+"\n")
                    for uu in sc_msg.sc2.unames:
                        print("id:"+uu.uid+"|name:"+uu.name)
                    self.FormLoading()
                else:
                    print("SCBroadcastBegin not exist")
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.LOADING_DONE:
                print("loading...")
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("loding ok")
                else:
                    print("server loading error")
            # round
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.ONE_ROUND:
                if sc_msg.HasField("sc3"):
                    print("game one round")
                    print("uid:"+sc_msg.sc3.uid+"|round:"+str(sc_msg.sc3.roundnum)+"|steptime:"+str(sc_msg.sc3.steptime))
                    print("\nlastuid:"+sc_msg.sc3.lastuid+"|operation:"+str(sc_msg.sc3.operation.x)+","+str(sc_msg.sc3.operation.y)+","+str(sc_msg.sc3.operation.r))
                    if sc_msg.sc3.uid == self.uid:
                        self.FormOP()
                    elif sc_msg.sc3.uid == "-1":
                        print("\nround end")
                        self.FormScore()
                    else:
                        print("\nother round")
                else:
                    print("oneround info not exist")
            # op
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.GAMER_OP:
                print("game op")
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("server get op ok")
                else:
                    print("server get op error")
            # score
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.UP_SCORE:
                print("up score")
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("server get score ok")
                else:
                    print("server get score error")

            elif sc_msg.type == pb_compile.PATH.mycity_pb2.BROADCAST_END:
                if sc_msg.HasField("sc4"):
                    print("score:\n")
                    for uu in sc_msg.sc4.uidscore:
                        print("id:"+uu.uid+"|name:"+str(uu.score))
                else:
                    print("SCBroadcastEnd not exist")
            else:
                print("undefine")
        except:
            print(line)

    def FormLoading(self):
        cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.LOADING_DONE
        self.mysendLine(cs_msg.SerializeToString())

    def FormOP(self):
        cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.GAMER_OP
        cs_msg.cs4.operation.x = 10
        cs_msg.cs4.operation.y = 10
        cs_msg.cs4.operation.r = 10
        self.mysendLine(cs_msg.SerializeToString())

    def FormScore(self):
        cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.UP_SCORE
        cs_msg.cs5.score = 333
        time.sleep(2)
        self.mysendLine(cs_msg.SerializeToString())

    def FormMapChange(self):
        cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.FRINED_SUBMIT_MAP
        cs_msg.cs3.mapid = "3"
        self.mysendLine(cs_msg.SerializeToString())

    def FormAskBegin(self):
        cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.FRIEND_ASK_BEGIN
        self.mysendLine(cs_msg.SerializeToString())

    ############################### 好友房间 ###########################
    def connectionMade3(self):
        #self.mysendLine("random_match")
        cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.ENTER_FRIEND
        cs_msg.cs2.uid = self.uid
        cs_msg.cs2.userinfo = self.userinfo
        cs_msg.cs2.roomid = self.roomid
        self.mysendLine(cs_msg.SerializeToString())

    def lineReceived3(self, line):
        print("+++++++++++++")
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        try:
            sc_msg.ParseFromString(line)
            # enter room
            if sc_msg.type == pb_compile.PATH.mycity_pb2.ENTER_FRIEND:
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("enter room ok")
                    # change map
                    #self.FormMapChange()
                else:
                    print("enter room error")
            # change map
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.FRINED_SUBMIT_MAP:
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("map change ok")
                else:
                    print("map change error")
            # room data change
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.FRIEND_ROOM_CHANGE:
                if sc_msg.HasField("sc1"):
                    print("mapid:"+sc_msg.sc1.mapid)
                    for uu in sc_msg.sc1.unames:
                        print("id:"+uu.uid+"|name:"+uu.name)
                    self.FormAskBegin()
                else:
                    print("FRIEND_ROOM_CHANGE sc1 not exist")
            # change map
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.FRIEND_ASK_BEGIN:
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("ask begin ok")
                else:
                    print("ask begin error")
            # enter loading
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.RANDOM_BROADCAST_BEGIN:
                if sc_msg.HasField("sc2"):
                    print("mapid:"+sc_msg.sc2.mapid+"\n")
                    for uu in sc_msg.sc2.unames:
                        print("id:"+uu.uid+"|name:"+uu.name)
                    self.FormLoading()
                else:
                    print("SCBroadcastBegin not exist")
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.LOADING_DONE:
                print("loading...")
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("loding ok")
                else:
                    print("server loading error")
            # round
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.ONE_ROUND:
                if sc_msg.HasField("sc3"):
                    print("game one round")
                    print("uid:"+sc_msg.sc3.uid+"|round:"+str(sc_msg.sc3.roundnum)+"|steptime:"+str(sc_msg.sc3.steptime))
                    print("\nlastuid:"+sc_msg.sc3.lastuid+"|operation:"+str(sc_msg.sc3.operation.x)+","+str(sc_msg.sc3.operation.y)+","+str(sc_msg.sc3.operation.r))
                    if sc_msg.sc3.uid == self.uid:
                        self.FormOP()
                    elif sc_msg.sc3.uid == "-1":
                        print("\nround end")
                        self.FormScore()
                    else:
                        print("\nother round")
                else:
                    print("oneround info not exist")
            # op
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.GAMER_OP:
                print("game op")
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("server get op ok")
                else:
                    print("server get op error")
            # score
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.UP_SCORE:
                print("up score")
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("server get score ok")
                else:
                    print("server get score error")

            elif sc_msg.type == pb_compile.PATH.mycity_pb2.BROADCAST_END:
                if sc_msg.HasField("sc4"):
                    print("score:\n")
                    for uu in sc_msg.sc4.uidscore:
                        print("id:"+uu.uid+"|name:"+str(uu.score))
                else:
                    print("SCBroadcastEnd not exist")
            else:
                print("undefine")
        except:
            print(line)



class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)



def main(reactor):
    factory = EchoClientFactory()
    #reactor.connectTCP('127.0.0.1', 8002, factory)
    reactor.connectTCP('129.211.115.238', 8002, factory)
    return factory.done



if __name__ == '__main__':
    task.react(main)
