#!/usr/bin/env python
# -*- coding: utf8 -*-
#

import struct
import socket
import time
import logging

logger = logging.getLogger('common')

class SocketSimple():
    '''
        server_address ("127.0.0.1", 8888)
    '''
    def __init__(self, server_address):
        self.server_address = server_address
        self.sock = None
        self.data = ""

    def __del__(self):
        if self.sock:
            self.Close("del")

    def Close(self, tag="normal"):
        if self.sock:
            logger.info("poppy: sock close:" + tag + "|" + str(self.sock.getsockname()) + "->" + str(self.sock.getpeername()))
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.sock = None

    def Connect(self):
        if not self.sock:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                self.sock.connect(self.server_address)
                return True
            except socket.error as message:
                self.sock = None
                logger.error("connect fail:" + message)
                return False 
        return True

    '''
        打包： [len: 4byte][data]
    '''
    def PackSend(self, data):
	#length = socket.htonl(len(data)+4)
        sock_data = struct.pack('!i', len(data)+4)
        sock_data += data
        return self.DelimiterSend(sock_data,"")

    '''
        打包： [data + "\0"]
    '''
    def DelimiterSend(self, data, delimiter="\0"):
        try:
            self.sock.sendall(data+delimiter)
            return True
        except socket.error as message:
            logger.error("send fail:" + message)
            return False

    '''
        按打包截取数据包 [len: 4byte][data]
    '''
    def PackRecieve(self, timeout=0.2):
        self.sock.settimeout(timeout)
        ## first part
        response_data = self.data # 保留遗留数据
        self.data = ""
        try:
            response_data = self.sock.recv(512)
        except Exception:
            logger.error("recv data timeout")
            print "recv1 data timeout"
            return ""
        ## other part
        count = 0
        if not response_data: return ""
        headers = struct.unpack('!i', response_data[:4])
        print repr(headers[0])
        total = headers[0]-4
        rlen = len(response_data)
        try:
            
            while len(response_data) < total:
                count = count + 1
                part = self.sock.recv(512)
                if not part: break
                response_data = response_data + part
                rlen = len(response_data)
            self.data = response_data[total:]
            return response_data[0:total]
        except Exception:
            logger.error("recv data timeout: count:" + str(count) + "|total:" + str(total) + "|len" + str(rlen))
            print "recv2 data timeout"
            return ""

    '''
        按分隔符截取数据包 [aaaaa\0bbbbbb\0ccccc\0]
    '''
    def DelimiterRecieve(self, delimiter="\0", timeout=0.2):
        self.sock.settimeout(timeout)
        ## first part
        response_data = self.data # 保留遗留数据
        self.data = ""
        try:
            response_data = response_data + self.sock.recv(512)
        except Exception:
            logger.error("recv data timeout")
            print "recv data timeout"
            return ""
        ## other part
        count = 0
        if not response_data: return ""
        try:
            while True:
                count = count + 1
                part = self.sock.recv(512)
                if not part: break
                pos = part.find(delimiter)
                if pos > -1:
                    response_data = response_data + part[0:pos]
                    self.data = part[pos+1:]
                    break
            return response_data
        except Exception:
            logger.error("recv data timeout: count:" + str(count))
            print "recv data timeout"
            return ""

