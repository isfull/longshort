# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 , Inc. All Rights Reserved
#
################################################################################
"""
manager user stat.

Authors: allen
Date:    2016/05/03
"""
import logging
import random
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

import UserLinkFactory
import UserManager
import GameManager
import RoomGameManager

import pb_compile.PATH.mycity_pb2

log = logging.getLogger('City')

# This is just about the simplest possible protocol
class User(object):
    # 状态机：排队中，等待加载，我的回合，别人回合，等待提交结果，等待广播结果
    (QUEUE, WAIT_LOADING, GAMING_ME, GAMING_OTHER, WAIT_RESULT, BROADCAST) = (0, 1, 2, 3, 4, 5)

    def __init__(self, user_info_str, userid, username, room_id, oUserLink):
        self.m_UserId = userid
        self.m_UserName = username
        self.m_UserInfoStr = user_info_str
        self.m_user_link = oUserLink
        self.m_game_stat = self.QUEUE  # 随机和好友房间都从queue开始
        self.m_game_object = None
        self.m_room_id = room_id

    def SendUnexpectMsg(self, msg):
        UserLinkFactory.ReactorSendMessage(self.m_user_link, b"stat unexpect msg:" + msg)

    def FormLodingOk(self):
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.LOADING_DONE
        sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())
    
    def FormAskBegin(self, error):
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.FRIEND_ASK_BEGIN
        if error == True:
            sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        else:
            sc_msg.error = pb_compile.PATH.mycity_pb2.ERROR
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())
    
    def FormOP(self, error):
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.GAMER_OP
        if error == True:
            sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        else:
            sc_msg.error = pb_compile.PATH.mycity_pb2.ERROR
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())

    def FormSubmitMap(self, error):
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.FRINED_SUBMIT_MAP
        if error == True:
            sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        else:
            sc_msg.error = pb_compile.PATH.mycity_pb2.ERROR
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())
    
    def FormUPScore(self, error):
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.UP_SCORE
        if error == True:
            sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        else:
            sc_msg.error = pb_compile.PATH.mycity_pb2.ERROR
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())
    

    def Handle(self, cs_msg):
        if cs_msg.type == pb_compile.PATH.mycity_pb2.FRINED_SUBMIT_MAP:
            if self.m_game_stat == self.QUEUE:
                if cs_msg.HasField("cs3"):
                    rgm = RoomGameManager.RoomGameManager()
                    rgm.ChangeMap(self.m_room_id, cs_msg.cs3.mapid)
                    self.FormSubmitMap(True)
                else:
                    self.FormSubmitMap(False)
            else:
                self.SendUnexpectMsg("stat: not in room")
        elif cs_msg.type == pb_compile.PATH.mycity_pb2.FRIEND_ASK_BEGIN:
            if self.m_game_stat == self.QUEUE:
                rgm = RoomGameManager.RoomGameManager()
                if rgm.AskRoomBegin(self.m_room_id):
                    self.FormAskBegin(True)
                else:
                    self.FormAskBegin(False)
            else:
                self.SendUnexpectMsg("stat: not wait_loading")
        elif cs_msg.type == pb_compile.PATH.mycity_pb2.LOADING_DONE:
            if self.m_game_stat == self.WAIT_LOADING:
                self.m_game_object.LoadingOk(self.m_UserId)
                self.FormLodingOk()
            else:
                self.SendUnexpectMsg("stat: not wait_loading")
        elif cs_msg.type == pb_compile.PATH.mycity_pb2.GAMER_OP:
            if self.m_game_stat == self.GAMING_ME:
                if cs_msg.HasField("cs4"):
                    
                    xx = cs_msg.cs4.operation.x
                    yy = cs_msg.cs4.operation.y
                    rr = cs_msg.cs4.operation.r
                    if self.m_game_object.UserOperation(self.m_UserId, xx, yy, rr):
                        self.FormOP(True)
                    else:
                        self.FormOP(False)
                else:
                    self.FormOP(False)
            else:
                self.SendUnexpectMsg("stat: not your turn")
        elif cs_msg.type == pb_compile.PATH.mycity_pb2.UP_SCORE:
            if self.m_game_stat == self.WAIT_RESULT:
                if cs_msg.HasField("cs5"):
                    self.FormUPScore(True)
                    self.m_game_object.UserScore(self.m_UserId, cs_msg.cs5.score)
                    self.m_game_stat == self.BROADCAST
                else:
                    self.FormUPScore(False)
            else:
                self.SendUnexpectMsg("stat: not wait_result")
        else:
            UserLinkFactory.ReactorSendMessage(self.m_user_link, b"server get " + msg)

    def ClientDown(self):
        # 解除引用
        # game 
        if self.m_game_object != None:
            self.m_game_object.GamerDown(self.m_UserId)
        self.m_game_object = None
        # usermanager
        um = UserManager.UserManager()
        um.DelUser(self.m_UserId)
        # gamemanager
        gm = GameManager.GameManager()
        gm.DelUser(self.m_UserId)
        # roomgamemanager
        rgm = RoomGameManager.RoomGameManager()
        rgm.DelUser(self.m_UserId,self.m_room_id)
        # user link
        self.m_user_link = None

    def AllEnd(self):
        # 解除引用
        # game 
        self.m_game_object = None
        # usermanager
        um = UserManager.UserManager()
        um.DelUser(self.m_UserId)
        # user link
        UserLinkFactory.ReactorShutDown(self.m_user_link)
        self.m_user_link = None

    ######################
    #  Game.py调用的接口  #
    ######################
    # room game: room change broadcast
    def RoomChange(self, mapid, ids, names):
        um = UserManager.UserManager()

        # send msg
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.FRIEND_ROOM_CHANGE
        sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        sc_msg.sc1.mapid = str(mapid)
        name_i = 0
        for uidx in ids:
            uinfo = sc_msg.sc1.unames.add()
            uinfo.uid = uidx
            uinfo.name = um.GetUser(uidx).m_UserName
            #uinfo.name = names[name_i]
            #name_i = name_i + 1
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())
    
    # loading
    def GameBegin(self, oGame, ids, names):
        um = UserManager.UserManager()

        self.m_game_object = oGame
        self.m_game_stat = self.WAIT_LOADING
        # send msg
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.RANDOM_BROADCAST_BEGIN
        sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        sc_msg.sc2.mapid = "1"
        name_i = 0
        for uidx in ids:
            uinfo = sc_msg.sc2.unames.add()
            uinfo.uid = uidx
            uinfo.name = um.GetUser(uidx).m_UserName
            #uinfo.name = names[name_i]
            #name_i = name_i + 1
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())

    def LoadingFail(self):
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.SERVER_END
        sc_msg.error = pb_compile.PATH.mycity_pb2.LOADING_FAIL
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())
        self.AllEnd()

    def BeginWaitResult(self):
        self.m_game_stat = self.WAIT_RESULT

    def CollectFail(self):
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.SERVER_END
        sc_msg.error = pb_compile.PATH.mycity_pb2.COLLECT_SCORE_FAIL
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())
        self.AllEnd()

    def GamerDown(self):
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.SERVER_END
        sc_msg.error = pb_compile.PATH.mycity_pb2.GAMER_LEAVE
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())
        self.AllEnd()

    def BroadCastResult(self, uid_score_map):
        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.BROADCAST_END
        sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        for k in uid_score_map:
            us = sc_msg.sc4.uidscore.add()
            us.uid = str(k)
            us.score = uid_score_map[k]
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())
        self.AllEnd()

        

    # Gaming
    # flag: 0me   1other   2wait_result
    def DoRound(self, uid, roundnum, steptime, lastuid, operation, flag):
        if flag == 0:
            self.m_game_stat = self.GAMING_ME
        elif flag == 1:
            self.m_game_stat = self.GAMING_OTHER
        else:
            self.m_game_stat = self.WAIT_RESULT

        sc_msg = pb_compile.PATH.mycity_pb2.SCGameMsg()
        sc_msg.type = pb_compile.PATH.mycity_pb2.ONE_ROUND
        sc_msg.error = pb_compile.PATH.mycity_pb2.OK
        sc_msg.sc3.uid = uid
        sc_msg.sc3.roundnum = roundnum
        sc_msg.sc3.steptime = steptime
        sc_msg.sc3.lastuid = lastuid
        if len(operation) == 3:
            sc_msg.sc3.operation.x = operation[0]
            sc_msg.sc3.operation.y = operation[1]
            sc_msg.sc3.operation.r = operation[2]
        else:
            sc_msg.sc3.operation.x = -1
            sc_msg.sc3.operation.y = -1
            sc_msg.sc3.operation.r = -1
        UserLinkFactory.ReactorSendMessage(self.m_user_link, sc_msg.SerializeToString())

