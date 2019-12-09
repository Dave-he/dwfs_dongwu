#!/usr/bin/python
# -*-coding: utf-8 -*-
# 土压力盒
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
            s.write(bytes.fromhex("23 33 34 31 39 30 34 39 34 41 E3 21"))
            time.sleep(1)
            count = s.inWaiting()
            while count < 10:
                time.sleep(1)
                count = s.inWaiting()

            id +=1
            data = s.read(count)
            sql = "insert into serial_data(id,create_date,parse_data,receive_data) values('%s','%s','%s','%s')"%(
                uuid.uuid4(), 
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
                str(data, 'utf-8'), 
                str(data,'utf-8'))
            
            
            cursor.execute(sql)
            db.commit()

            for i in (1,4):
                postdata={
                    'id':'TY00'+ str(i),
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
