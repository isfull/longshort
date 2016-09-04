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

from twisted.internet.protocol import Protocol, Factory
from twisted.internet.protocol import ServerFactory
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.protocols.basic import LineReceiver

import TaskRunner
import ServerStatFactory
import UserLinkFactory
import UserManager
import GameManager  
import RoomGameManager  
import common.GenId


def main():

    # init log. both file and console
    log = logging.getLogger('City')
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s-%(asctime)s]-tid:%(thread)d-%(filename)s-%(lineno)d:%(message)s')  
    
    fh = logging.FileHandler('city.log')  
    fh.setLevel(logging.INFO) 
    fh.setFormatter(formatter) 

    ch = logging.StreamHandler()  
    ch.setLevel(logging.INFO)  
    ch.setFormatter(formatter)
    
    log.addHandler(ch)  
    log.addHandler(fh) 
    # 使用多线程，要处理好锁问题
    tr = TaskRunner.TaskRunner()
    tr = TaskRunner.TaskRunner()    
    tr.InitPool()
    # 启动用户管理器
    um = UserManager.UserManager()
    um = UserManager.UserManager()
    # 启动游戏管理器
    gm = GameManager.GameManager()
    gm = GameManager.GameManager()
    gm.Init()

    rgm = RoomGameManager.RoomGameManager()
    rgm = RoomGameManager.RoomGameManager()
    rgm.Init()

    gidm = common.GenId.GameIdManager()
    gidm = common.GenId.GameIdManager()
    gidm.Init()
    #aaa = ttt()
    #TaskRunner.DoProto(Testt, aaa, "22")


    # 启动服务器状态请求socket
    f2 = ServerStatFactory.ServerStatLinkFactory()
    reactor.listenTCP(8001, f2)

    f2 = UserLinkFactory.UserLinkFactory()
    reactor.listenTCP(8002, f2)

    reactor.suggestThreadPoolSize(2)
    reactor.run()

if __name__ == '__main__':
    main()
