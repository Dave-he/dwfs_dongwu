#!/usr/bin/python
# -*-coding: utf-8 -*-
# 土压力盒
import serial
import time
import pymysql as pdb
import requests


port = 'com10'
buand = 9600

url = "http://dwb.maplebim.com/data/upload"

def hexsend(string_data=''):
    return string_data.decode("hex")

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
                sql = "insert into serial_data(id,create_date,parse_data,receive_data) values('%s','%s','%s','%s')"%("alarm-" + str(id), local_time, str(data, 'utf-8'), str(data,'utf-8'))
               
              
                cursor.execute(sql)
                db.commit()
                postdata={
                    'id':'TY001',
                    'type':'double',
                    'value':'0.001'
                }
                r=requests.post(url,data=postdata)
                print(r.text)
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
