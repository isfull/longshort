# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2016 , Inc. All Rights Reserved
#
################################################################################
"""
encode decode

Authors: allen
Date:    2016/07/10
"""
import logging

log = logging.getLogger('City')

def CityDecode(in_str):
    l = len(in_str)
    out_str=""
    i = 0
    while i < l:
        if ord(in_str[i]) == 255:
            i = i+1
            if i >= l:
                log.error("Decode error: 255 appear at last place")
                break;
            if ord(in_str[i]) == 1:
                out_str = out_str + chr(0)
            else:
                out_str = out_str + chr(255)
            i = i+1
        else:
            out_str = out_str + in_str[i]
            i = i+1
    return out_str


def CityEncode(in_str):
    l = len(in_str)
    out_str=""
    i = 0
    while i < l:
        if ord(in_str[i]) == 255:
            out_str = out_str + chr(255) + chr(2)
        elif ord(in_str[i]) == 0:
            out_str = out_str + chr(255) + chr(1)
        else:
            out_str = out_str + in_str[i]
        i = i+1
    return out_str