
import sys
import socket
import time
from utils import display_file

TCP_IP = sys.argv[1] #'localhost'
TCP_PORT = int(sys.argv[2]) #9001
BUFFER_SIZE = 1024
try:
    req_filename = sys.argv[3]
except:
    req_filename = ''
get_req = 'GET /{filename} HTTP/1.1'.format(filename=req_filename)
print get_req

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
t = time.time()
s.connect((TCP_IP, TCP_PORT))
print 'RTT Connection: ', time.time()-t
t = time.time()
s.send(get_req)

buffered_data = ''
while True:
    data = s.recv(BUFFER_SIZE)
    if data:
        buffered_data = buffered_data + data
    else:
        break
print 'HostName: ', TCP_IP
print 'Socket Type: ', s.type
print 'Peer Name: ', s.getpeername()
print 'Socket Family: ', s.family
    
s.close()
print 'Connection closed'
print 'RTT Get File: ', time.time()-t

display_file(buffered_data)
