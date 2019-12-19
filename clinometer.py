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

def ByteToHex( bins ):
    return ''.join( [ "%02X" % x for x in bins ] ).strip()

if __name__ == '__main__':

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
            s.write(bytes.fromhex("FE 04 00 00 00 03 A4 04"))
            count = s.inWaiting()
            while count < 5:
                time.sleep(0.2)
                count = s.inWaiting()

       
            local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            recv = s.read(count)
            data = ByteToHex(recv)
            # print(local_time+' '+ data + ' ' + data[14:18] + ' '+ data[6:10])
            
            x = int(data[14:18],16)
            xdata={
                'id':'WY001',
                'type':'double',
                'value': x
            }
            sql = "insert into serial_data(id,create_date,parse_data,receive_data) values('%s','%s','%s','%s')"%(
                uuid.uuid4(),
                local_time, 
                pdb.escape_string(requests.post(url,data=xdata).text),
                "WY001-" + str(x))
            
            cursor.execute(sql)
            
            y = int(data[6:10],16)
            ydata={
                'id':'WY002',
                'type':'double',
                'value': y
            }
            sql = "insert into serial_data(id,create_date,parse_data,receive_data) values('%s','%s','%s','%s')"%(
                uuid.uuid4(),
                local_time, 
                pdb.escape_string(requests.post(url,data=ydata).text), 
                "WY002-" + str(y))
            
            cursor.execute(sql)
            time.sleep(1)
            s.write(bytes.fromhex("01 03 00 00 00 02 C4 0B"))
            count = s.inWaiting()
            while count < 5:
                time.sleep(0.2)
                count = s.inWaiting()

       
            local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            recv = s.read(count)
            data = ByteToHex(recv)
            print(local_time+' '+ data + ' ' + data[10:14] + ' '+ data[6:10])
            
            
            x = int(data[10:14],16)-65535
            xdata={
                'id':'JD001',
                'type':'double',
                'value': x
            }
            sql = "insert into serial_data(id,create_date,parse_data,receive_data) values('%s','%s','%s','%s')"%(
                uuid.uuid4(),
                local_time, 
                pdb.escape_string(requests.post(url,data=xdata).text),
                "JD001-" + str(x))
            
            cursor.execute(sql)
            
            y = int(data[6:10],16)
            ydata={
                'id':'JD002',
                'type':'double',
                'value': y
            }
            sql = "insert into serial_data(id,create_date,parse_data,receive_data) values('%s','%s','%s','%s')"%(
                uuid.uuid4(),
                local_time, 
                pdb.escape_string(requests.post(url,data=ydata).text), 
                "JD002-" + str(y))
            
            cursor.execute(sql)

            db.commit()
            time.sleep(1)
         
    except KeyboardInterrupt:
        print("exit")

    if s != None:
        s.close()
    if cursor != None:
        cursor.close() 
    if db != None:
        db.close()
