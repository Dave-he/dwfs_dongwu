#!/usr/bin/python
# -*-coding: utf-8 -*-
# 倾角仪

import serial
import time
import pymysql as pdb
import requests
import uuid

port = 'com10'
buand = 9600

url = "http://dwb.maplebim.com/data/upload"

if __name__ == '__main__':
    id = 0
    db = pdb.connect(
    "localhost",
    "root",
    "root",
    "dwzc_socket"
    )
    cursor = db.cursor()
    s = serial.Serial(port,buand)
    try:
        while True:
            time.sleep(0.1)
            count = s.inWaiting()
            if count > 0:
                id +=1
                local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                data = s.read(count)
         
                xdata={
                    'id':'JD001',
                    'type':'double',
                    'value':'0.001'
                }
                sql = "insert into serial_data(id,create_date,parse_data,receive_data) values('%s','%s','%s','%s')"%(
                    uuid.uuid4(),
                    local_time, 
                    requests.post(url,data=xdata).text,
                    "JD001-" +str(data,'utf-8'))
               
                cursor.execute(sql)

                ydata={
                    'id':'JD002',
                    'type':'double',
                    'value':'0.002'
                }
                sql = "insert into serial_data(id,create_date,parse_data,receive_data) values('%s','%s','%s','%s')"%(
                    uuid.uuid4(),
                    local_time, 
                    requests.post(url,data=ydata).text, 
                    "JD002-" + str(data,'utf-8'))
               
                cursor.execute(sql)
                db.commit()
                if data != b'':
                    print("receive:", data)
                    s.write(data)
                else:
                    s.write(hexsend(data))
       
    except KeyboardInterrupt:
        print("exit")

    if s != None:
        s.close()
    if cursor != None:
        cursor.close() 
    if db != None:
        db.close()
