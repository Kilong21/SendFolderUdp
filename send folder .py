import socket
import os
import time
import sys
class app():
    def __init__(self):
        self.port = 4444
        self.f = b'<213><123><132>'
        self.s = socket.socket()
        if not os.path.isdir('DATA'):
            os.mkdir('DATA/')
    def connect(self,ip):
        self.s.connect((ip,self.port))
    def bind(self):
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.s.bind(( '' , self.port ))
        self.s.listen(1)
        self.s , addr = self.s.accept()
        print("connected ............")    
    def Recv(self):
        x=0
        DATA = b''
        while 1:
            DATA += self.s.recv(40000)
            x += 1
            if self.f in DATA:
                n = DATA.find(self.f)
                paths= eval(DATA[:n])
                m = len(paths)
                DATA = DATA[n+15:]
                for path in paths:
                    
                    if not os.path.isdir('DATA/'+path[0]):
                        os.makedirs('DATA/'+path[0])
                    file = open('DATA/'+'/'.join(path),'wb')
                    while 1:
                        DATA += self.s.recv(40000)
                        if self.f in DATA:
                            n = DATA.find(self.f)
                            file.write(DATA[:n])
                            DATA = DATA[n+15:]
                            print('\r'+str(   ( (  paths.index(path)+1  ) * 100)//m)        +' %' ,end='' )
                            break
                        else:
                            file.write(DATA)
                            DATA = b''
                    self.s.send(b'22')
                print('[+]       Ending .......... \n')
                    
                break
    def Send(self,path):
                path = path.replace('\\','/')
                sr = os.path.dirname(path)+'/'
                print(sr)
                input()
                data = str([
                    [root.replace('\\','/').replace(sr,'').replace(':','') ,file]
                    for root , dirs , files in os.walk(path )
                    for file in files]).encode()+self.f
                self.s.send(data)
                for root , dirs , files in os.walk(path.replace('\\','/')):
                    for file in files:
                        self.s.sendfile(open(root+'/'+file,'rb'))
                        self.s.send(self.f)
                        self.s.recv(2)
                        print('Sendig  => ',file)
                print("[+]        Ending .............  \n")
    def pro(self):
        b1 = '''
            [ 01 ]  ==> Sending
            [ 02 ]  ==> Receiving
            [ 03 ]  ==> Exit

        '''''
        while 1:
            print(b1)
            try:
                n = int(input('Enter 01 or 02  => '))
                if n  == 1 or n == 2  :
                    while 1:
                        yn = input('Enter y or n => ').lower()
                        if yn == 'y' or yn == 'n':
                            if yn == 'n':
                                os.system('cls')
                                self.pro()
                            else:
                                break
                    break
            except:
                os.system('cls')
        if n == 1 :
            while 1:
                try:
                    ip = input('Recipient IP  => ')
                    self.connect(ip)
                    break
                except:
                    print('The Address Was Not Found')
            while 1:
                    path = input('Enter Path Folder  => ')
                    if  os.path.isdir(path):
                        self.Send(path)
                        input()
                    else:
                        print('Path Folder Not Found')
        elif n == 2:
            while 1:
                    self.bind()
                    self.Recv()
                    input()
                    self.pro()
                    
app().pro()                   
