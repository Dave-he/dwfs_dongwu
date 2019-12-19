#!/usr/bin/python
# -*-coding: utf-8 -*-
# 声光报警器

import serial
import time
import pymysql as pdb
import uuid

port = 'com2'
buand = 9600


def sendMessage(msg):
    s = serial.Serial(port,buand)
    s.write(bytes.fromhex(msg))
    db = pdb.connect(
    "localhost",
    "root",
    "root",
    "dwzc_socket"
    )
    cursor = db.cursor()
    sql = "insert into serial_data(id,create_date,parse_data,receive_data) values('%s','%s','%s','%s')"%(
       uuid.uuid4(), 
       time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
       msg, "alarm")
               
    cursor.execute(sql)
    db.commit()
    if s != None:
        s.close()
    if cursor != None:
        cursor.close() 
    if db != None:
        db.close()

def start():
    msg = '7E FF 06 3A 00 81 00 EF'
    sendMessage(msg)

def stop():
    msg ='7E FF 06 3A 00 00 01 EF 00 00 00 7E FF 06 16 00 00 00 EF'
    sendMessage(msg)
    time.sleep(2)
    sendMessage(msg)

if __name__ == '__main__':
    # start()
    time.sleep(1)
    stop()