#!/usr/bin/env python
# coding=utf-8

import serial
import struct

class MySerial:
    def __init__(self,baud=115200):
        self.ser=serial.Serial("/dev/ttyAMA0",baud)
        print(self.ser)
        print(self.ser.close)

    def __del__(self):
        self.ser.close()

    def send_cross_data(self,x,y):
        head=b'by'
        length=struct.pack('b',2)
        type=struct.pack('b',15)
        s_x=struct.pack('h',x)
        s_y=struct.pack('h',y)
        s=head+length+type+s_x+s_y+b'\r\n'
        print(s)
        self.ser.write(s)






