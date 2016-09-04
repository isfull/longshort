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
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
import common.Singleton

# 存储user对象实例
# 使用单例模式；使用锁保证操作安全
class UserManager(common.Singleton.Singleton):

    m_user_dict = {}
    m_lock = threading.Lock()

    def GetUser(self, user_id):
        #print("find:"+str(user_id))
        rt = None
        self.m_lock.acquire()
        if self.m_user_dict.has_key(user_id):
            rt = self.m_user_dict[user_id]
        else:
            rt = False
        self.m_lock.release()
        return rt

    def AddUser(self, oUser):
        self.m_lock.acquire()
        self.m_user_dict[oUser.m_UserId] = oUser
        self.m_lock.release()

    def DelUser(self, user_id):
        self.m_lock.acquire()
        if self.m_user_dict.has_key(user_id):
            del self.m_user_dict[user_id]
        self.m_lock.release()


