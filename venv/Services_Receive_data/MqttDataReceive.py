# -*- coding:utf-8 -*-

import sys
import logging
import os
import time
import configparser
import requests
import json
import xlrd
import xlwt
from xlutils.copy import copy
import  pymysql
import threading
import  matplotlib.pyplot as plt
import numpy as np
import time
from math import *
import math






cf = configparser.ConfigParser()
cf.read("./config.ini")
host = cf.get("setting","host")
con=pymysql.connect(host=host,
                    db="lorawan",
                    user="root",
                    password="1qaz@WSX",
                    port=3306,
                    charset="utf8")
cursor = con.cursor()

threads=[]

eui = cf.get("setting","EUI")
Euidevice = str(eui).split(",")
path = cf.get("setting","path")

airspeed = cf.get("setting", "AirSpeed")
CommunicationDistance = cf.get("setting", "CommunicationDistance")

def _getLogger():
        logger = logging.getLogger('[MqttDataReceive]')
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        handler = logging.FileHandler(os.path.join(dirpath, "service.log"))
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

def login():
        s = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Referer": "http://47.110.127.110:8090/login",
            "Origin": "http://47.110.127.110:8090"}
        payload = {"username": "njfd", "password": "888888"}
        html = s.post(url="http://47.110.127.110:8080/api/v1/auth/login", data=json.dumps(payload), headers=headers)
        status = html.status_code
        text=html.text
        if status==200:
            content = json.loads(text).get('data').get('jwt')
            Auth = "Bearer "+content
        return  Auth,s

def unix_time(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime



def __withintimeinterval__(timestamp):
    cur_timestamp = time.time()
    cur_timestamp  =str(cur_timestamp)
    cur_timestamp = cur_timestamp[0:10]
    cur_timestamp =long(cur_timestamp)
    pre_timestamp = cur_timestamp-86400
    if timestamp>pre_timestamp and timestamp<cur_timestamp:
        return  True
    else:
        return  False

def __Arrangement__(lt=[]):
    #lt = [3, 5, 2, 1, 8, 4]
    n = len(lt)
    for x in range(n - 1):
        for y in range(n - 1 - x):
            if lt[y] > lt[y + 1]:
                lt[y], lt[y + 1] = lt[y + 1], lt[y]
    #print  lt
    return lt





def refresh_data(device_eui,Auth,s):
        headers_EUI = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Origin": "http://47.110.127.110:8090",
            "Referer": "http://47.110.127.110:8090/user/node/data",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Authorization": Auth
        }
        DEV_EUI = "http://47.110.127.110:8080/api/v1/lorawan/datas/devices?devEui={a}&uplink=&page=0&pageSize=500".format(a=device_eui)
        html = s.get(url=DEV_EUI, headers=headers_EUI)
        status = html.status_code
        temp =[]
        total =[]
        Originally=[]
        if status == 200:
            text = html.content
            content = json.loads(text).get('data').get('content')
            content = list(content)
            content_list = []
            for item in content:
                eachitem = dict(item)
                if eachitem["mtypeText"] == u"UNCONFIRMED_DATA_UP":
                    content_list.append(item)
            for item  in  content_list:
                ServerTime = item['serverTimeMillis']
                ServerTime = str(ServerTime)
                fcnt = item['fcnt']
                fcnt = int(fcnt)
                dict_temp ={
                    "servertime":item['serverTime'],
                    "fcnt":item['fcnt']
                }
                total.append(dict_temp)
                #截取不好含时分秒
                timestamp = ServerTime[0:10]
                timestamp = long(timestamp)
                flage = __withintimeinterval__(timestamp)
                if flage == True:
                    temp.append(fcnt)
            #print temp
            temp = __Arrangement__(temp)
            min = temp[0]
            max =temp[len(temp)-1]
            count = max-min+1
            if count ==len(temp):
                print "No packet lose\r\n"
                print "receive total number"+str(count)
            else:
                for i  in range(min,max+1):
                    Originally.append(i)
                #计算差集
                ret = list(set(Originally) ^set(temp))

                #print ret
                for  los  in ret:
                    for  i  in range(0,len(temp)):
                        if  los >temp[i] and los<temp[i+1]:
                            for  j  in  range(0,len(total)):
                                dict1 = dict(total[j])
                                dict2 =dict(total[j+1])
                                if int(dict1["fcnt"])==int(temp[i+1])and  int(dict2["fcnt"])==int(temp[i]):
                                    print ("LosePacketNum:{a},Timer interval is:{c}~{d}\r\n".format(a=los,c=dict1["servertime"],d=dict2["servertime"]))
                                    break
                print ("Lose numerber:{a}\r\n".format(a=len(ret)))
                print("Total Packet number:{b}\r\n".format(b=max))
                print("Lose Rate:{c}%\r\n".format(c=float(len(ret)*100/float(max))))
















a =login()
for i  in range(0,len(Euidevice)):
    try:
        print("------------DeviceEui:{a}-------------\r\n".format(a=Euidevice[i]))
        refresh_data(Euidevice[i],a[0],a[1])
    except:
        pass
raw_input("Press <enter>")





