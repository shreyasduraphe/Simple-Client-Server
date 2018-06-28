#import libraries and classes
import socket
import sys
from threading import Thread
from SocketServer import ThreadingMixIn
from utils import Parse


TCP_IP = 'localhost'
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print "A New thread started for "+ip+":"+str(port)


    def run(self):
        print 'HostName: ', self.ip
        print 'Socket Type', self.sock.type
        print 'Socket Family: ', self.sock.family
        print 'Peer Name', self.sock.getpeername()
        print 'Socket Protocol', self.sock.proto
        data = self.sock.recv(1024)
        initial_data =  repr(data)
        filename = Parse.extract(initial_data.strip("'"))

        if not filename:
            print 'HTTP/1.1 400 Bad Request'
            self.sock.send('HTTP/1.1 400 Bad Request\nContent-Type: text/html\n\n<body>Invalid URL!! File name is required</body>')
        elif filename in ["HelloCN1.txt", "WorldCN2.txt"]:
            f = open(filename,'rb')
            buffered_data = ''
            while True:
                eachline = f.read(BUFFER_SIZE)
                while (eachline):
                    buffered_data = buffered_data + eachline
                    eachline = f.read(BUFFER_SIZE)
                if not eachline:
                    f.close()
                    break
            
            print 'HTTP/1.0 200 OK'
            self.sock.send(
                'HTTP/1.0 200 OK'+
                '\nHost: '+TCP_IP+
                '\nContent-Disposition: attachment; filename="received.txt"'+
                '\nContent-Length: '+str(len(buffered_data))+
                '\nContent-Type: text/plain; charset=utf-8'+
                '\n\n'+
                buffered_data)

        else:
            print 'HTTP/1.1 400 Bad Request'
            self.sock.send('HTTP/1.1 400 Bad Request\nContent-Type: text/html\n\n<body>Page Not Found</body>')
        self.sock.close()


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(10)
    print "Waiting for incoming requests from clients..."
    (conn, (ip,port)) = tcpsock.accept()
    print 'Got a client connection from ', (ip,port)
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()