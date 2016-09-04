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

class EchoClient(LineReceiver):
    delimiter = "\x00"
    end = "Bye-bye!"
    uid = ""
    userinfo = ""

    def connectionMade(self):
        self.uid = str(time.time())
        self.userinfo = "some info"
        self.connectionMade2()

    def lineReceived(self, line):
        a = base64.b64decode(line)
        self.lineReceived2(a)

    # stat
    def connectionMade1(self):
        #self.sendLine("random_match")
        cs_msg = pb_compile.PATH.mycity_pb2.CSStatMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.ONLINE
        self.sendLine(cs_msg.SerializeToString())

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


    # logic
    def connectionMade2(self):
        print("fuck")
        #self.sendLine("random_match")
        cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.ENTER_RANDOM
        cs_msg.cs1.uid = self.uid
        cs_msg.cs1.userinfo = self.userinfo
        self.sendLine(cs_msg.SerializeToString())

    def lineReceived2(self, line):
        print("-------------")
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
                    print("mapid:"+sc_msg.sc2.mapid+"|names:"+sc_msg.sc2.unames)
                    self.FormLoading()
                else:
                    print("SCBroadcastBegin not exist")
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.LOADING_DONE:
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("loding ok")
                else:
                    print("server loading error")
            # round
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.ONE_ROUND:
                if sc_msg.HasField("sc3"):
                    print("uid:"+sc_msg.sc3.uid+"|round:"+str(sc_msg.sc3.roundnum)+"|steptime:"+str(sc_msg.sc3.steptime))
                    print("\nlastuid:"+sc_msg.sc3.lastuid+"|operation:"+sc_msg.sc3.operation)
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
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("server get op ok")
                else:
                    print("server get op error")
            # score
            elif sc_msg.type == pb_compile.PATH.mycity_pb2.UP_SCORE:
                if sc_msg.error == pb_compile.PATH.mycity_pb2.OK:
                    print("server get score ok")
                else:
                    print("server get score error")

            elif sc_msg.type == pb_compile.PATH.mycity_pb2.BROADCAST_END:
                if sc_msg.HasField("sc4"):
                    print("score:"+sc_msg.sc4.uidscore)
                else:
                    print("SCBroadcastEnd not exist")
            else:
                print("undefine")
        except:
            print(line)

    def FormLoading(self):
        cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.LOADING_DONE
        self.sendLine(cs_msg.SerializeToString())

    def FormOP(self):
        cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.GAMER_OP
        cs_msg.cs4.operation = "(x,y,z)"
        self.sendLine(cs_msg.SerializeToString())

    def FormScore(self):
        cs_msg = pb_compile.PATH.mycity_pb2.CSGameMsg()
        cs_msg.type = pb_compile.PATH.mycity_pb2.UP_SCORE
        cs_msg.cs5.score = 333
        time.sleep(2)
        self.sendLine(cs_msg.SerializeToString())


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
    reactor.connectTCP('132.148.23.104', 8002, factory)
    #reactor.connectTCP('127.0.0.1', 8002, factory)
    return factory.done



if __name__ == '__main__':
    task.react(main)
