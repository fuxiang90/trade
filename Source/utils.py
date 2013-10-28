#!/usr/bin/python 
# -*- coding: utf8 -*-
import datetime
import time
def strip_str_head_tail(s ):
    # 去掉字符串的头尾
    if len(s) > 2:
        return s[1:-1]
    return ""

def str_to_datetime(s):
    pos = s.find('.')
    if pos != -1 :
        s = s[:pos]
    dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")  
    return dt

def get_date_str_from_file_name(file_name):
    #从文件名中抽取日期
    start_pos = file_name.find('.')
    end_pos = file_name.find('.',start_pos + 1)
    s = file_name[start_pos + 1 : end_pos]
    
    dt = datetime.datetime.strptime(s ,"%Y%m%d")
    return str(dt).split(' ')[0]
def get_m(dt):
    pass

def normalize(data):
    Max  = -100.0
    Min = 1000000000000000.0 

    
if __name__ == '__main__':

    print strip_str_head_tail('[shhhsd]')

    print str_to_datetime("2013-10-22 09:10:13.729")
    d1 = str_to_datetime("2013-10-22 09:10:13.729")
    d2 = str_to_datetime("2013-10-22 09:12:13.729")
    d3 = str_to_datetime("2013-10-22 12:10:13.729")
    d4 = str_to_datetime("2013-10-22 00:10:13.729")
    print d2 > d1 
    print str(d1)
    print (d2 - d1).seconds
    

    print  get_date_str_from_file_name(".20121202.")
