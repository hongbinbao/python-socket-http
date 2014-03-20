#! /usr/bin/python
# -*- coding:utf-8 -*- 
import socket, sys, threading  
    
SERVER = u'127.0.0.1'   
PORT = 8080    
MAXTHREADS = 10  
RECVBUFLEN = 1024  
HTTPTAG = u'HTTP/1.'  
MYTAG = u'^MyP 1.0'  
RSTR = u''''HTTP/1.1 200 OK 
Proxy-Connection: Keep-Alive 
Connection: Keep-Alive 
Content-Length: 8296 
Via: 1.1 JA-ISA02 
Expires: Fri, 18 May 2012 09:05:56 GMT 
Date: Fri, 18 May 2012 09:05:56 GMT 
Content-Type: text/html;charset=gb2312 
Server: BWS/1.0 
Cache-Control: private 
 
test'''  
RSTR2 = u'''''my defined p... '''  
RSTR3 = u'''''unknown p... '''  
userlist = [u'user01', u'user02']  
BADUSER = u'bad'  
class Checker(threading.Thread):  
    def __init__(self,socket,num):  
        threading.Thread.__init__(self)  
        self.socket = socket  
        self.num = num  
        print 'thread started!'  
  
    def run(self):  
        while True:  
            self.socket.listen(2)  
            cs,address = self.socket.accept()  
            recvstr = cs.recv(RECVBUFLEN)  
            print '>>>>>>>>>>>>thread [%d] received:\r\n%s' % (self.num,recvstr)  
            if recvstr == '':  
                print 'empty request'  
                cs.close()  
                return  
            TAG = recvstr.split('\r\n', 1)[0]  
            if HTTPTAG in TAG:  
                print 'HTTP Request'  
                cs.send(RSTR)  
                print 'response is: \r\n%s' % RSTR  
            elif MYTAG in TAG:  
                print 'My define Request'  
                cs.send(RSTR2)  
                print 'response is: \r\n%s' % RSTR2  
            else:  
                print 'other request'  
                cs.send(RSTR3)  
                print 'response is: \r\n%s' % RSTR3  
            print '>>>>>>>>>>>>thread [%d] end check>>>>>>>>>>>>' % (self.num,)  
            cs.close()  
  
  
class authServer(object):  
    def __init__(self):  
        self.socket = None  
    def run(self):  
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.socket.bind((SERVER,PORT))  
        i = 0  
        chkerlist = []  
        while i<MAXTHREADS:  
            chker = Checker(self.socket,i)  
            chker.start()  
            i = i + 1  
            chkerlist.append(chker)  
        for chker in chkerlist:  
            chker.join()  
  
if __name__ == '__main__':  
    asvr = authServer()  
    asvr.run()  
    print 'ending'  
      
