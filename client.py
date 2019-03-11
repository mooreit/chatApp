
import socket

def Main():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 

    host = socket.gethostname()		# Host IP
    port = 5001	        # specified port to connect

    server = (host,5000)

    sock.bind((host,port))

    msg = input("-> ")
    while msg !='q':
        sock.sendto(msg.encode('utf-8'),server)
        data, addr = sock.recvfrom(1024)
        data = data.decode('utf-8')
        print("Receive from server: " + data)
        msg = input("->")
    sock.close()

if __name__ == '__main__':
    Main()