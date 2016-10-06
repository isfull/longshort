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

import threading
import time
import logging

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

import common.Singleton
import common.GenId
import Game
import UserManager

log = logging.getLogger('City')

class Room(object):
    def __init__(self, gamer, mapid):
        self.m_gamers = [gamer]
        self.m_mapid = mapid
# 使用单例模式；使用锁保证操作安全
class RoomGameManager(common.Singleton.Singleton):

    # {roomid:room object}
    m_waiting_rooms = {}
    # 已经开始的游戏（玩家退出，通知对手，然后结束游戏）
    m_gameing_list = []
    # 房间m_gameing_list变化队列,存放房间号,有队列定期检查广播房间变化
    m_change_event = []
    # 锁
    m_lock = threading.Lock() # 操作时加锁
    #self.m_lock.acquire()
    #self.m_lock.release()

    # 添加用户：判断房间是否已存在，然后把用户加入房间
    def AddUser(self, user_id, roomid):
        self.m_lock.acquire()
        if self.m_waiting_rooms.has_key(roomid):
            # roomid exist
            if len(self.m_waiting_rooms[roomid].m_gamers) >= 8: 
                # too many gamer
                self.m_lock.release()
                return False
            else:
                log.info("enter room. roomid:"+roomid+"|userid:"+user_id)
                self.m_waiting_rooms[roomid].m_gamers.append(user_id)
                self.m_change_event.append(roomid)
        else:
            # roomid not exist
            log.info("create room. roomid:"+roomid+"|userid:"+user_id)
            self.m_waiting_rooms[roomid] = Room(user_id, 1)
            self.m_change_event.append(roomid)
        self.m_lock.release()
        return True

    # 删除用户:判断房间是否存在，然后从房间删除
    def DelUser(self, uid, roomid):
        self.m_lock.acquire()
        if self.m_waiting_rooms.has_key(roomid):
            for i in range(0,len(self.m_waiting_rooms[roomid].m_gamers)): 
                if uid == self.m_waiting_rooms[roomid].m_gamers[i]:
                    del self.m_waiting_rooms[roomid].m_gamers[i]
                    self.m_change_event.append(roomid)
                    break
        else:
            None
        self.m_lock.release()
        return True

    # 用户修改地图
    def ChangeMap(self, roomid, mapid):
        um = UserManager.UserManager()
        self.m_lock.acquire()
        if self.m_waiting_rooms.has_key(roomid):
            # 发布变化
            self.m_waiting_rooms[roomid].m_mapid = mapid
            self.m_change_event.append(roomid)
        else:
            # roomid not exist
            None
        self.m_lock.release()

    # 用户请求启动游戏
    def AskRoomBegin(self, roomid):
        um = UserManager.UserManager()
        rt = False
        self.m_lock.acquire()
        if self.m_waiting_rooms.has_key(roomid):
            if len(self.m_waiting_rooms[roomid].m_gamers) < 2:
                rt = False
            else:
                self._NewGame(roomid)
                rt = True
        else:
            # roomid not exist
            rt = False
        self.m_lock.release()
        return rt

    ## todo
    def DelGame(self, game_id):
        self.m_lock.acquire()
        for i in range(0,len(self.m_gameing_list)):
            if self.m_gameing_list[i] == game_id:
                del self.m_gameing_list[i]
                break
        self.m_lock.release()
        return True

    def Init(self):
        self.m_waiting_rooms = {}
        self.m_gameing_list = []
        self.m_change_event = []
        ## 循环检测房间变化队列，广播变化
        # 1s检测一次
        t = threading.Thread(target=self._DoQueue)
        t.setDaemon(False)
        t.start()

    #################
    #  广播房间变化  #
    #################
    def _DoQueue(self):
        sleepflag = True
        while True:
            if sleepflag:
                time.sleep(0.2)
            else:
                sleepflag = True
            # 检查是否有变化
            self.m_lock.acquire()
            if len(self.m_change_event) > 0:
                try:
                    self._DoChange(self.m_change_event[0])
                    del self.m_change_event[0]
                    sleepflag = False
                except Exception as e:
                    log.error("[room game manager]:"+str(e))
            self.m_lock.release()

    # 广播房间变化，广播房间全部信息，不只是小变化
    def _DoChange(self, roomid):
        um = UserManager.UserManager()
        if self.m_waiting_rooms.has_key(roomid):
            # 发布变化
            names = ["allen","bill","cavan","david","ellie","frank","gary","hans"]
            mapid = self.m_waiting_rooms[roomid].m_mapid
            for i in range(0, len(self.m_waiting_rooms[roomid].m_gamers)):
                u = um.GetUser(self.m_waiting_rooms[roomid].m_gamers[i])
                if u == False:
                    log.error("do change:room user not found:",repr(self.m_waiting_rooms[roomid].m_gamers[i]))
                else:
                    u.RoomChange(mapid,self.m_waiting_rooms[roomid].m_gamers,names)
        else:
            # roomid not exist
            None

    def _NewGame(self, roomid):
        g = Game.Game("friend")
        self.m_gameing_list.append(g.GetGameId())
        # 向单局游戏添加用户，并从等待队列删除
        lenx = len(self.m_waiting_rooms[roomid].m_gamers)
        for i in range(0,lenx):
            g.AddGamer(self.m_waiting_rooms[roomid].m_gamers[0])
            del self.m_waiting_rooms[roomid].m_gamers[0]
        g.SetMapId(self.m_waiting_rooms[roomid].m_mapid)
        del self.m_waiting_rooms[roomid]
        g.DoBegin()
        


            


