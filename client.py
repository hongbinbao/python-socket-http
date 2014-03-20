#!/usr/bin/python
# -*- coding:utf-8 -*- 

import socket, threading    
  
SERVER = '127.0.0.1'
PORT = 8080  
START = u'^MyP 1.0'   
START2 = u'^MyP 1.0'   
START3 = u'[^st]'   
BUFLEN = 1024   
USER_list = [u'user01', u'user02']  
  
class connector(threading.Thread):  
    def __init__(self,num):  
        threading.Thread.__init__(self)  
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.num = num  
  
    def run(self):  
        try:  
            self.sock.connect((SERVER,PORT))  
            self.sock.send(START)  
            print '>>>>>sent ',START              
            rstr = self.sock.recv(BUFLEN)  
            print 'received>>>>>>>',rstr  
            self.sock.close()  
            return  
        except socket.error,e:  
            print e  
            return  
  
if __name__ == '__main__':  
    cnlist = []  
    i = 0  
    while i<10:  
        cn = connector(i)  
        cn.start()  
        cnlist.append(cn)  
        i = i + 1  
    for cn in cnlist:  
        cn.join()  
