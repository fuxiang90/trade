#!/usr/bin/python 
# -*- coding: utf8 -*-

import json 
import re 
import os
import argparse 
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
import numpy as np


from utils import strip_str_head_tail, str_to_datetime, get_date_str_from_file_name 
from csv_write import write_question_one, write_question_two, write_question_three 
class Trade(object):

    def __init__(self,path):

        self._product_dict = {}
        self._product_result = {}
        self._user_dict = {}
        self._order_dict = {}
        
        self._bad_time_dict = {}
        self._path = path
        self._home = os.environ['CODEHOME']

        #某一个时刻如果
        self._time_count = 2 
        self._now_date_str = ""

        self._order_user = {}
        self._order_info = {} #order count  price
        pass

    
    def handle_one(self,file_path):
        fin = open(file_path)
        self._product_dict = {}
        for line in fin:
            line_list = line.strip().split(' ')
            if len(line_list) < 13 : continue 
            
            m = re.findall('code:([^,]+),' ,line_list[13])
            if len(m) == 1 :
                print line_list[13]
                print m[0]
                if line_list[12] == "buy" or line_list[12] == "sell":
                    count = re.findall('quantity:(\d+),',line_list[13])[0]
                    self._product_dict[m[0]]  = self._product_dict.get(m[0],0) + int(count)
                    
                    price = 0.0
                    try:
                        price_str = re.findall('price:(\d+.\d+)]',line_list[13])[0]
                        price = float(price_str)
                    except:
                        pass 
                    user_str = strip_str_head_tail(line_list[10]) 
                    if user_str not in self._user_dict:
                        self._user_dict[user_str] = [0 , 0.0]
                    self._user_dict[user_str][0] += 1 
                    self._user_dict[user_str][1] += int(count)* price 
                    
                    order_seq = strip_str_head_tail(line_list[5])
                    self._order_user[order_seq] = user_str
                    self._order_info[order_seq] = [int(count) ,price*(int(count))] 
        print self._product_dict                     
        max_product = sorted(self._product_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[:10]
        print max_product
        product_list = []
        for product in max_product :
            product_list.append(product[0])
        self._product_result[self._now_date_str] = product_list 
    def work_one(self):
        file_list = os.listdir(self._path)
        for file_name in file_list :
            if file_name.endswith('log') == False : continue 
            
            self._now_date_str = get_date_str_from_file_name(file_name)
            file_path = os.path.join(self._path , file_name)
            print file_path 
            self.handle_one(file_path)
       
        print self._product_result 
        write_question_one(self._product_result)

            
    
    def handle_two(self,file_path):
        fin = open(file_path)

        zero_time_str = ""  
        for line in fin :
            line_list = line.strip().split(' ')
            
            time_str = strip_str_head_tail (line_list[0] + ' '+ line_list[1] )
            zero_time_str = line_list[0]
            dt = str_to_datetime(time_str)
            
            #print dt
            len_list = len(line_list)
            if len(line_list) > 5 :
                if line_list[4] == "Request" :
                    order_str = strip_str_head_tail(line_list[5])
                    self._order_dict[order_str] = [dt]
                elif len_list > 9 and  line_list[6] == "created" :
                    request_str = strip_str_head_tail( line_list[9] )
                    if request_str  in self._order_dict :
                        self._order_dict[request_str].append(dt) 
                elif len_list > 9  and line_list[6] == "cancelled":
                    request_str = strip_str_head_tail( line_list[9] )
                    if request_str  in self._order_dict :
                        self._order_dict[request_str].append(dt) 
                    
                    #
                    if request_str in self._order_user :
                        user = self._order_user[request_str]
                        price = self._order_info[request_str][1]
                        self._user_dict[user][0] -= 1 
                        self._user_dict[user][1] -= price 
                elif len_list > 7 and  line_list[7] == "rejected":
                    request_str = strip_str_head_tail( line_list[5] )
                    if request_str  in self._order_dict :
                        self._order_dict[request_str].append(dt) 
        

        for k,v in self._order_dict.iteritems():
            if len(v) != 2 : continue
            t = (v[1] - v[0]).seconds
            if t >= 1: 
                print k,(v[1] -v[0]).seconds 
        
        self._bad_time = []
        zero_dt = str_to_datetime( zero_time_str[1:] + ' ' + '0:0:0')

        #得到了order起始时间
        bad_time_dict = {}
        bad_time_count_dict = {}
        


        for order in self._order_dict :
            order_list = self._order_dict[order]
            if len(order_list) != 2 : continue 
            start_time = order_list[0]
            
            end_time = order_list[1]
            dt = end_time - start_time
            #print dt.seconds
            if dt.seconds >= 1 : 
                #self._bad_time.append(start_time)

                #start_time = str(start_time)
                start_pos = (start_time - zero_dt ).seconds 
                end_pos = (end_time - zero_dt ).seconds
                
                """
                if start_time not in bad_time_count_dict :
                    bad_time_count_dict[start_time] = 0
                """
                if start_pos not in bad_time_count_dict :
                    bad_time_count_dict[start_pos] = 0
                #print start_time 
                bad_time_count_dict[start_pos] += 1
                """
                if start_pos not in bad_time_dict  :
                    bad_time_dict [start_pos]  = end_pos
                
                if end_pos > bad_time_dict[start_pos] :
                    bad_time_dict [start_pos]  = end_pos 
                """
                if start_time not in bad_time_dict  :
                    bad_time_dict [start_time]  = end_time
                
                if end_time > bad_time_dict[start_time] :
                    bad_time_dict [start_time]  = end_time 
                #step = (start_time - zero_dt ).seconds 
                #self._bad_time_dict[step] = self._bad_time_dict.get(step ,0) + 1
        #print self._bad_time
        
        #for each in bad_time_count_dict :

        l = sorted(bad_time_count_dict.items() ,key = lambda bad_time_count_dict:bad_time_count_dict[0]) 
        for each in l:
            print each[0] ,each[1] 
        print "-------------------------"

        l = sorted(bad_time_dict.items(), lambda x, y: cmp(x[1], y[1]))
        
        bad_time_list = []
        for each in l:
            if (each[1]-each[0]).seconds > 5* 60 :
                bad_time_list.append(each)   
        write_question_two(zero_dt,bad_time_list)

    def bad_time_analyze(self):
        #分析出 bad time 的点
        
        bad_time_list = []
        for time in self._bad_time_dict :
            if self._bad_time_dict[time] >= self._time_count  :
                bad_time_list.append(time)
        #bad_time_list = self._bad_time_dict.keys()
        pos = 0
        l = len(bad_time_list)
        bad_time_tuple = []

        while pos < l - 2:
            start_pos = pos 
            while pos + 1 < l and  bad_time_list[pos] == bad_time_list[pos + 1] - 1:
                pos += 1 
            print  (bad_time_list[start_pos] ,bad_time_list[pos] )  
            if pos - start_pos > 10 :
                bad_time_tuple.append( (bad_time_list[start_pos] ,bad_time_list[pos] ) )
            pos += 1 
        print bad_time_tuple 


    def work_two(self):
        file_list = os.listdir(self._path)
        for file_name in file_list :
            if file_name.endswith('log') == False : continue 
            file_path = os.path.join(self._path , file_name)
            print file_path 
            self.handle_two(file_path)

            #debug 
            break
        #self.bad_time_analyze()

    def work_three(self):
        
        self._user_dict = {}
        file_path = os.path.join(self._path , 'eTrade.20131021.log')
        self.handle_one( file_path)
        self.handle_two( file_path )
        data = []
        user_list = []
        for user in self._user_dict :

            
            user_list.append(user)

        for user in self._user_dict :
            c = self._user_dict[user][0] 
            p = self._user_dict[user][1]
            #c = (c - c_min)*1.0/(c_max-c_min) 
            #p = (p- p_min)/(p_max-p_min)
            data.append([c,p])
        X = np.array(data) 
        af = AffinityPropagation(preference=None,max_iter=200 ,damping = 0.5  ).fit(X)
        #af = AffinityPropagation(damping=0.5, max_iter=600, convergence_iter=15, copy=True, preference=None, affinity='euclidean', verbose=False).fit(X)
        cluster_centers_indices = af.cluster_centers_indices_
        labels = af.labels_
        print labels

        write_question_three(labels,user_list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",dest = 'test',help="increase output verbosity",nargs = '?') 
    args = parser.parse_args()



    root_path = os.environ['CODEHOME']
    if args.test:
        test = Trade(root_path+'/Data/Test')
    else :
        test = Trade(root_path+'/Data/Prod')
    #test.work_one()
    test.work_two()
    #test.work_three()
if __name__ == '__main__':
    main()

