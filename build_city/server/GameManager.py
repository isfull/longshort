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

# 使用单例模式；使用锁保证操作安全
class GameManager(common.Singleton.Singleton):

    # 排队玩家(可增加删除排队玩家)
    m_waiting_users = []
    # 已经开始的游戏（玩家退出，通知对手，然后结束游戏）
    m_gameing_list = []
    # 锁
    m_lock = threading.Lock() # 操作玩家时加锁
    #self.m_lock.acquire()
    #self.m_lock.release()

    def GetWaitingUserNum(self):
        wait_num = len(self.m_waiting_users)
        return wait_num

    def GetGamingNum(self):
        game_num = len(self.m_gameing_list)
        return game_num

    def AddUser(self, user_id):
        self.m_lock.acquire()
        for uid in self.m_waiting_users:
            if uid == user_id:
                self.m_lock.release()
                return False
        self.m_waiting_users.append(user_id);
        self.m_lock.release()
        return True
    
    def DelUser(self, user_id):
        self.m_lock.acquire()
        for i in range(0,len(self.m_waiting_users)):
            if self.m_waiting_users[i] == user_id:
                del self.m_waiting_users[i]
                break
        self.m_lock.release()
        return True

    def DelGame(self, game_id):
        self.m_lock.acquire()
        for i in range(0,len(self.m_gameing_list)):
            if self.m_gameing_list[i] == game_id:
                del self.m_gameing_list[i]
                break
        self.m_lock.release()
        return True

    def Init(self):
        ## 循环检测排队玩家，依据规则创建游戏
        # 2s检测一次
        # 不满3人： 不开始
        # 超过3人：1 满8人立刻开始  2 累计15s，立即开始
        t = threading.Thread(target=self._DoQueue)
        t.setDaemon(False)
        t.start()

    #################
    #  生成随机房间  #
    #################
    def _DoQueue(self):
        check_counter = 0
        um = UserManager.UserManager()
        while True:
            time.sleep(2)

            self.m_lock.acquire()
            # 检查人数
            wait_num = len(self.m_waiting_users)
            #log.info("Server Stat: wait_num:"+str(wait_num))
            #log.info("Um:"+str(um.m_user_dict))
            if wait_num < 2:
                check_counter = 0
            elif wait_num > 7:
                # 开始一局
                log.info("game begin:num>7")
                self._NewGame()
                check_counter = 0
            else:
                if check_counter > 7:
                    # 开始一局
                    log.info("game begin:num>2&&time>7")
                    self._NewGame()
                    check_counter = 0
                else:
                    check_counter = check_counter + 2
            self.m_lock.release()

    def _NewGame(self):
        g = Game.Game()
        self.m_gameing_list.append(g.GetGameId())
        # 向单局游戏添加用户，并从等待队列删除
        lenx = 8
        if len(self.m_waiting_users) < 8:
            lenx = len(self.m_waiting_users)
        else:
            lenx = 8
        for i in range(0,lenx):
            g.AddGamer(self.m_waiting_users[0])
            del self.m_waiting_users[0]
        g.DoBegin()


            


