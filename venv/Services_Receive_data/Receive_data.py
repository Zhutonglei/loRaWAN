# -*- coding:utf-8 -*-

import requests
import re
import json
import  xlwt
import  xlrd
from xlutils.copy import copy
import configparser
import  os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


cf = configparser.ConfigParser()
cf.read("./config.ini")

airspeed = cf.get("setting", "AirSpeed")
CommunicationDistance = cf.get("setting", "CommunicationDistance")
Chose = cf.get("setting", "Chose")
path = cf.get("setting","path")

#登录获取session
s=requests.session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Referer": "http://47.110.127.110:8090/login",
    "Origin": "http://47.110.127.110:8090"}
payload = {"username": "njfd", "password": "888888"}
html = s.post(url="http://47.110.127.110:8080/api/v1/auth/login",data=json.dumps(payload),headers=headers)
status = html.status_code
if status==200:
    print "msg:request success"
elif status==500:
    print "msg:request error"
text=html.text
content = json.loads(text).get('data').get('jwt')
EUI=Chose
DEV1_EUI = "http://47.110.127.110:8080/api/v1/lorawan/datas/devices?devEui={a}&uplink=&page=0&pageSize=300".format(a=EUI)
auth = "Bearer "+content
headers_EUI={
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Origin": "http://47.110.127.110:8090",
    "Referer": "http://47.110.127.110:8090/user/node/data",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Authorization":auth
}
html = s.get(url=DEV1_EUI, headers=headers_EUI)
status = html.status_code
request = html.request
text = html.content
content = json.loads(text).get('data').get('content')
content = list(content)
content_list=[]
for  item  in  content:
    eachitem  = dict(item)
    if eachitem["mtypeText"]==u"UNCONFIRMED_DATA_UP":
        content_list.append(item)
        value =eachitem["payloadData"]
max = dict(content_list[0])
max = int(max["fcnt"])
list_group = []
for i in range(max, 0, -30):
    list_group.append(i)
grouping = []
for k in range(0, len(list_group)):
    temp = []
    if k + 1 < len(list_group):
        temp.append(list_group[k])
        temp.append(list_group[k + 1])
        grouping.append(temp)
for n in range(0, len(grouping)):
    temp1 = []
    temp2 = []
    temp3 = []
    temp4 = []
    a = list(grouping[n])[0]
    b = list(grouping[n])[1]
    for item in content_list:
        item = dict(item)
        fcnt = item["fcnt"]
        if fcnt > b and fcnt <= a:
            rssi = item["rssi"]
            lsnr = item["lsnr"]
            serverTime = item["serverTime"]
            temp1.append(fcnt)
            temp2.append(rssi)
            temp3.append(serverTime)
            temp4.append(lsnr)
    loss_percent =round ((float(30 - len(temp1)) / 30) * 100,2)
    print("---------------------------------------\n\rSection:[{a}~{b}]".format(a=a,b=b))
    print("Actual receipt:{a}".format(a=str(len(temp1))))
    print  ("Packet loss:" + str(loss_percent)+"%")
    total = 0
    for k in range(0, len(temp2)):
        total = total + float(temp2[k])
    per_rssi =round(total / len(temp2),1)
    print ("Average rssi:" + str(per_rssi))
    total_lsnr = 0
    for k in range(0, len(temp4)):
        total_lsnr = total_lsnr + float(temp4[k])
    per_lsnr = round(total_lsnr / len(temp4),1)
    print("Average lsnr:" + str(per_lsnr))
    endtime = temp3[0]
    starttime = temp3[len(temp3)-1]
    print ("Time:{a}~{b}".format(a=starttime, b=endtime))
    workbook = xlrd.open_workbook(path)
    table = workbook.sheets()[0]
    ncols = table.ncols
    nrows= table.nrows
    wb = copy(workbook)  # 复制
    ws = wb.get_sheet(0)
    ws.write(nrows, 0, EUI)
    ws.write(nrows, 1, "{a}~{b}".format(a=starttime, b=endtime))
    ws.write(nrows, 2, airspeed)#config
    ws.write(nrows, 3, CommunicationDistance)#config
    ws.write(nrows, 4, 30)
    ws.write(nrows, 5, "{a}".format(a=str(len(temp1))))
    ws.write(nrows, 6, str(loss_percent))
    ws.write(nrows, 7, str(per_rssi))
    ws.write(nrows, 8, str(per_lsnr))
    wb.save(path)
raw_input("Press <enter>")




















