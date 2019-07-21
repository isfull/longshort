# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 , Inc. All Rights Reserved
#
################################################################################
"""
singleton base.

Authors: allen
Date:    2016/05/10
"""
import logging
#import MySQLdb
import common.Singleton

log = logging.getLogger('City')


uid = 1000
def GetId():
    global uid 
    uid = uid + 1
    return uid

class GameIdManager(common.Singleton.Singleton):

    def GetGameId(self):
        self.gid = self.gid + 1
        return self.gid

    def Init(self):
        self.gid = 0;
        #con = MySQLdb.connect(host="localhost", user="chenyu", passwd="City#2016",db="db_city",port=3306)
        #cur = con.cursor()
        
        #rs_num = cur.execute("SELECT max(gid) FROM `tb_game`")
        #if rs_num == 1:
        #    rs = cur.fetchone()
        #    log.info("max gid:"+str(rs[0]))
        #    self.gid = rs[0]
        #else:
        #    self.gid = 0

        #cur.close()
        #con.commit()
        #con.close()