#!/usr/bin/python
# -*-coding: utf-8 -*-
# 土压力盒
import serial
import time
import pymysql as pdb
import requests
import uuid
import binascii


port = 'com7'
buand = 2400

url = "http://dwb.maplebim.com/data/upload"


def ByteToHex( bins ):
    return ''.join( [ "%02X" % x for x in bins ] ).strip()

def ByteToStr(src):
    return ' '.join( [ str(x) for x in src ] ).strip()


def getIDs(num):
    ids = []
    for m in range(1,num):
        ids.append('C0'+str(m))
    return ids

def getIndexOf(data):
    for index in range(3,12):
        if ord(data[index]) > 127:
            return index

    return 0    

def readData(data):
    result = {}
    for i in getIDs(9):
        datas = data.split(i)
        if len(datas) > 1 :
            src = datas[1]
            index = getIndexOf(src)
            if index > 0 :
                s = int(src[3:index])
                if s <0:
                    s+= 65535
                result[i] = s/100
    return result

def parseData(data):
    out = ''
    res = data.split(' ')
    if len(res) > 10:
        for i in res:
            out+=  chr(int(i))
        return readData(out)
    return {}

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
            s.write(bytes.fromhex("23 33 34 31 39 30 34 39 34 41 E3 21"))
            time.sleep(1)
            count = s.inWaiting()
            b = 0
            while count < 55:
                if b> 10:
                    break
                b+=1
                time.sleep(1)
                count = s.inWaiting()

            recv = s.read(count)

            data = ByteToStr(recv)
            result = parseData(data)
            sql = "insert into jinma_data(id,create_date,parse_data,receive_data) values('%s','%s','%s','%s')"%(
                uuid.uuid4(), 
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 
                data,pdb.escape_string(str(result)))
            
            
            cursor.execute(sql)
            db.commit()

            if 'C01' in result.keys():
                postdata={
                    'id':'TY001',
                    'type':'double',
                    'value': result['C01']
                }
                requests.post(url,data=postdata)
         
            if 'C02' in result.keys():
                postdata={
                    'id':'TY002',
                    'type':'double',
                    'value': result['C02']
                }
                requests.post(url,data=postdata)
                
            if 'C05' in result.keys():
                postdata={
                    'id':'TY003',
                    'type':'double',
                    'value': result['C05']
                }
                requests.post(url,data=postdata)
                
            if 'C08' in result.keys():
                postdata={
                    'id':'TY004',
                    'type':'double',
                    'value': result['C08']
                }
                requests.post(url,data=postdata)
    

        
    except KeyboardInterrupt:
        print("exit")

    if s != None:
        s.close()
    if cursor != None:
        cursor.close() 
    if db != None:
        db.close()
