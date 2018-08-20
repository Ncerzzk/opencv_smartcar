#!/usr/bin/env python
# coding=utf-8

import serial
import struct

class MySerial:
    def __init__(self,baud=115200):
        self.ser=serial.Serial("/dev/ttyAMA0",baud)
        print(self.ser)

    def __del__(self):
        self.ser.close()

    def send_cross_data(self,x,y,angle):
        head=b'by'
        length=struct.pack('b',8)
        type=struct.pack('b',15)
        try:
            s_x=struct.pack('h',x)
            s_y=struct.pack('h',y)
            s_a=struct.pack('f',angle)
            s=head+length+type+s_x+s_y+s_a+b'\r\n'
            self.ser.write(s)
        except:
            print("error!\r\n")
            print(s)

    def send_chess_data(self,x,y,r):
        head=b'by'
        length=struct.pack('b',6)
        type=struct.pack('b',14)
        try:
            s_x=struct.pack('h',x)
            s_y=struct.pack('h',y)
            s_r=struct.pack('h',r)
            s=head+length+type+s_x+s_y+s_r+b'\r\n'
            self.ser.write(s)
        except:
            print("error!\r\n")
            print(s)



