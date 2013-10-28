
# -*- coding: utf8 -*-
import csv 
import os

result_path = os.path.join(os.environ['CODEHOME'] , 'Result')


def write_question_one( data ):
    file_path = os.path.join(result_path , 'Q1.csv')

    print file_path,data
    writer = csv.writer(file(file_path, 'w'))
    for line in data :
         
        writer.writerow([ line ]+ data[line]) 

def write_question_two(dt,data):
    file_path = os.path.join(result_path , 'Q2.csv')

    dt_time = dt.strftime("%Y-%m-%d")
    writer = csv.writer(file(file_path, 'w'))
    for line in data :
         
        writer.writerow([ dt_time ,line[0].strftime("%H:%M:%S"),line[1].strftime("%H:%M:%S") ]) 

def write(c ,l ):
    file_name = 'Q3_%s.csv' %(str(c) )  
    file_path = os.path.join(result_path , file_name )

    writer = csv.writer(file(file_path, 'w'))
    for line in l :
         
        writer.writerow([ line ]) 


def write_question_three(data,user_list):
    
    l = len(user_list)
    d = {}
    for pos in range(l):
        c = data[pos].real 
        print data[pos]
        print type(c)
        user = user_list[pos]
        if c not in d :
            d[c] = []
        d[c].append(user)

    for each in d :
        write(each,d[each])
    
