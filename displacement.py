#!/usr/bin/python
# -*-coding: utf-8 -*-
# 位移传感器-指令查看聚英软件
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
            s.write(bytes.fromhex("01 03 00 00 00 02 C4 0B"))
            time.sleep(0.1)
            count = s.inWaiting()
            if count > 0:
                id += 1
                data = s.read(count)
                sql = "insert into serial_data(id,create_date,parse_data,receive_data) values('%s','%s','%s','%s')"%(
                    uuid.uuid4(), 
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
                    str(data, 'utf-8'), 
                    str(data,'utf-8'))
               
              
                cursor.execute(sql)
                db.commit()
                postdata={
                    'id':'WY001',
                    'type':'double',
                    'value':'0.001'
                }
                r=requests.post(url,data=postdata)
                print(r.text)

                postdata={
                    'id':'WY002',
                    'type':'double',
                    'value':'0.001'
                }
                r=requests.post(url,data=postdata)
                print(r.text)
                print("receive:", data)
       
    except KeyboardInterrupt:
        print("exit")

    if s != None:
        s.close()
    if cursor != None:
        cursor.close() 
    if db != None:
        db.close()
