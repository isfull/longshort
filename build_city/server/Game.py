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
import logging
import MySQLdb
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

import UserManager
import GameManager
import RoomGameManager
import common.GenId
import random

log = logging.getLogger('City')

class Game():
    #
    # 游戏状态机：等待大家加载，游戏中，等待提交结果，结算广播并结束,异常结束
    #

    (WAIT_LOADING, GAMING, WAIT_RESULT, BROADCAST, ERROR_END) = (0, 1, 2, 3, 4)

    def __init__(self, gametype="random"):
        self.m_game_stat = self.WAIT_LOADING
        self.m_game_id = common.GenId.GameIdManager().GetGameId()
        self.m_map_id = str(random.randint(1,3)) # 好友房间会额外调用setmapid重置
        self.m_userid_list = []  # 用户列表
        self.m_username_list = ["allen","bill","cavan","david","ellie","frank","gary","hans"] # 后台给的用户名字，和上一个字段一起描述用户
        self.m_set_lock = threading.Lock()
        self.m_room_type = gametype

        # 等待加载
        self.m_loading_timer = None
        self.m_loading_set = set()
        self.m_round_num = 10   # 设定回合数,在GameBegin里会依据人数重置这个值

        # 游戏中
        self.m_iterator = 0 # 当前轮到谁
        self.m_round_timer = None
        self.m_round = 0 # 当前第几轮
        self.m_last_uid = "$" # 上一轮的uid
        self.m_last_data = [] # 上一步走的啥
        self.m_all_data = "" # 所有人的操作
        # 等待提交结果
        self.m_score_set = set()
        # 结束广播并结束
        self.m_score_map = {}

    def GetGameId(self):
        return self.m_game_id
    def GetMapId(self):
        return self.m_map_id
    def SetMapId(self, mapid):
        self.m_map_id = str(mapid)

    def AddGamer(self, userid):
        self.m_userid_list.append(userid)

    # 玩家下线，立刻结束游戏，通知所有人
    def GamerDown(self, userid):
        self.m_game_stat = self.ERROR_END
        # 删除玩家
        for i in range(0, len(self.m_userid_list)):
            if self.m_userid_list[i] == userid:
                del self.m_userid_list[i]
                break
        # 清理游戏数据
        if self.m_loading_timer != None:
            self.m_loading_timer.cancel()
        if self.m_round_timer != None:
            self.m_round_timer.cancel()
        # 通知玩家，游戏结束
        um = UserManager.UserManager()
        for userid in self.m_userid_list:
            user_x = um.GetUser(userid)
            if user_x != False:
                user_x.GamerDown()
        for i in range(0, len(self.m_userid_list)):
            del self.m_userid_list[0]

    ############
    #  游戏状态 #
    ############
    #---------------------------self.WAIT_LOADING---------------------
    def DoBegin(self):
        # 初始化一些游戏参数
        self.m_round_num = int(round(80/len(self.m_userid_list)))

        log.info("gamer"+str(self.m_userid_list)+"|mapid:"+self.m_map_id)
        # 游戏状态机进入等待大家加载状态
        self.m_game_stat = self.WAIT_LOADING
        # 启动加载计时器
        self.m_loading_timer = threading.Timer(5, self._CheckLoading)
        self.m_loading_timer.start()
        # 通知开始
        um = UserManager.UserManager()
        #ids_names_str = ""
        #for userid in self.m_userid_list:
        #    ids_names_str = ids_names_str+"|"+userid+",U"+userid
        #log.info(ids_names_str)
        #ids_names_str = ids_names_str[1:]
        for userid in self.m_userid_list:
            u = um.GetUser(userid)
            if u == False:
                log.error("user not found. why game begin?:", userid)
            else:
                u.GameBegin(self, self.m_userid_list, self.m_username_list, self.m_map_id, self.m_round_num)

    # 某一个用户加载成功
    def LoadingOk(self, user_id):
        # 检查游戏状态
        if self.m_game_stat != self.WAIT_LOADING:
            return
        self.m_set_lock.acquire()
        self.m_loading_set.add(user_id)
        self.m_set_lock.release()

    def _CheckLoading(self):
        if len(self.m_userid_list) == len(self.m_loading_set):
            self.m_game_stat = self.GAMING
            self.m_round = 0
            self._DoRound()
        else:
            # 通知加载失败，游戏结束
            um = UserManager.UserManager()
            for userid in self.m_userid_list:
                user_x = um.GetUser(userid)
                if user_x != False:
                    user_x.LoadingFail()

    #---------------------------self.GAMING---------------------
    # 用户提交操作
    def UserOperation(self, user_id, x, y, r):
        # 检查游戏状态
        if self.m_game_stat != self.GAMING:
            return
        # 检查是否轮到该用户操作
        if user_id != self.m_userid_list[self.m_iterator-1]:
            return
        # 提交操作，停止计时器，开始下一轮
        if self.m_round_timer != None:
            self.m_round_timer.cancel()
        # 记录用户行为
        self.m_last_uid = user_id
        self.m_last_data = [x,y,r]
        self.m_all_data = self.m_all_data + "\n" + user_id +":["+str(x)+","+str(y)+","+str(r)+"]"
        self._DoRound()
        None

    def _DoRound(self):
    #    print("round:"+str(self.m_round)+"|total round:"+self.m_round_num+"|iterator:"+str(self.m_iterator))
        # m_round是一轮 m_iterator 是一轮里每个人
        # 增加计数器
        if self.m_iterator == len(self.m_userid_list):
            self.m_round = self.m_round + 1
            self.m_iterator = 1
        else:
            self.m_iterator = self.m_iterator + 1
        # 判断回合
        if self.m_round == self.m_round_num:
            # 修改状态机状态，启动结算timer
            self.m_game_stat = self.WAIT_RESULT
            self.m_round_timer = threading.Timer(6, self._CheckResult)
            self.m_round_timer.start()

            # 结束时得等广播最后一个用户操作
            um = UserManager.UserManager()
            for i in range(0, len(self.m_userid_list)):
                userx = um.GetUser(self.m_userid_list[i])
                if userx != False:
                    userx.BeginWaitResult()
            for i in range(0, len(self.m_userid_list)):
                userx = um.GetUser(self.m_userid_list[i])
                if userx != False:
                    userx.DoRound("-1", -1, 5, self.m_last_uid, self.m_last_data, 2)
            # 重置上一步操作
            self.m_last_uid = "$"
            self.m_last_data = []
            
        else:                
            # 广播上一步，并告知下一步是谁
            um = UserManager.UserManager()
            for i in range(0, len(self.m_userid_list)):
                if i == (self.m_iterator-1):
                    userx = um.GetUser(self.m_userid_list[i])
                    if userx != False:
                        userx.DoRound(self.m_userid_list[self.m_iterator-1], self.m_round, 60, self.m_last_uid, self.m_last_data, 0)
                else:
                    userx = um.GetUser(self.m_userid_list[i])
                    if userx != False:
                        userx.DoRound(self.m_userid_list[self.m_iterator-1], self.m_round, 60, self.m_last_uid, self.m_last_data, 1)
            # 重置上一步操作
            self.m_last_uid = "$"
            self.m_last_data = []

            # 启动下一轮timer
            self.m_round_timer = threading.Timer(60, self._DoRound)
            self.m_round_timer.start()
            
    #---------------------------self.WAIT_RESULT-------------------
    def UserScore(self, user_id, score):
        # 检查游戏状态
        if self.m_game_stat != self.WAIT_RESULT:
            return
        self.m_set_lock.acquire()
        self.m_score_map[user_id] = score
        self.m_score_set.add(user_id)
        self.m_set_lock.release()

    def _CheckResult(self):
        if len(self.m_userid_list) == len(self.m_score_set):
            self.m_game_stat = self.BROADCAST
            self._WriteDB()
            self._BroadCast()
        else:
            # 通知统计失败，游戏结束
            um = UserManager.UserManager()
            for userid in self.m_userid_list:
                user_x = um.GetUser(userid)
                if user_x != False:
                    user_x.CollectFail()
    #---------------------------self.BROADCAST---------------------
    def _BroadCast(self):
        # 形成分数结果
        #rs = "\n"
        #for k in self.m_score_map:
        #    rs = rs + "user:" + str(k) + "|score:" + str(self.m_score_map[k]) + "\n"
        # 写数据库

        # 广播结果，游戏结束
        um = UserManager.UserManager()
        for userid in self.m_userid_list:
            userx = um.GetUser(userid)
            if userx != False:
                userx.BroadCastResult(self.m_score_map)

        # 删除游戏管理器中的game，删除game实例
        if self.m_room_type == "random":
            GameManager.GameManager().DelGame(self.m_game_id)
        else:
            RoomGameManager.RoomGameManager().DelGame(self.m_game_id)
        
        del self

    def _WriteDB(self):
        um = UserManager.UserManager()
        sql2 = "insert into tb_game (gid,mapid,operation) values (%d,%s,%s)"%(int(self.m_game_id),str(self.m_map_id),self.m_all_data)
        sql3 = "insert into tb_game_user (gid,uid,score) values (%d,%s,%d)"%(int(self.m_game_id),k,self.m_score_map[k])
        try:
            con = MySQLdb.connect(host="localhost", user="chenyu", passwd="City#2016",db="db_city",port=3306)
            cur = con.cursor()
            
            # 保存用户信息
            for userid in self.m_userid_list:
                sql1 = "insert into tb_user (uid,info,uname) values (%s,%s,%s)"%(um.GetUser(userid).m_UserId,um.GetUser(userid).m_UserInfoStr,um.GetUser(userid).m_UserName)
                log.info(sql1)
                cur.execute(sql1)
            # 保存对局信息
            cur.execute(sql2)
            # 保存分数信息
            for k in self.m_score_map:
                cur.execute(sql3)
            con.commit()
        except Exception as e:
            log.error("[mysql error]:"+str(e)+"|sql2:"+sql2+"|sql3:"+sql3)




