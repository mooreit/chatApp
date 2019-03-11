import socket

def Main():
    serverSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      

    host = socket.gethostname()		        
    port = 5000		                

    #print type(sock) ============> 'type' can be used to see type 
                    # of any variable ('sock' here)

    serverSock.bind((host,port))
    print("Server started")
    while True:
        print("Waiting for client ...")
        data,addr = serverSock.recvfrom(1024)	        #receive data from client
        data = data.decode('utf-8')
        print("Message from:" + str(addr))
        print("Received From User: " + data)
        serverSock.sendto(data.encode('utf-8'),addr)
    serverSock.close()

if __name__ == '__main__':
    Main()
