# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 , Inc. All Rights Reserved
#
################################################################################
"""
multiprocess task.

Authors: allen
Date:    2016/05/03
"""
from multiprocessing.dummy import Pool as ThreadPool
from twisted.internet import reactor
import common.Singleton

#class T():
#	d=1
#
#def Test( ob, num):
#    print("ddd:"+ob.d)
#    print("ddd:"+num)
#    return num
def DoProto(func, ob, pb):
    TaskRunner().thread_pool.apply(func, (ob, pb, ))

class TaskRunner(common.Singleton.Singleton):
    key = 123
    thread_pool = None

    def InitPool(self):
        self.thread_pool = ThreadPool(4)
        #self.thread_pool.startThreads() 
        #self.thread_pool.map(self._task_handler, urls)
    

    