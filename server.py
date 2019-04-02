import socket, select
from random import randint
import pickle

# COLORED TEXT FUNCTIONS
def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk)) 
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk)) 
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk)) 
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk)) 
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk)) 

connected_list =[]

def main():
	name=""
	global connected_list
	#dictionary to store socket object and uniqure ID corresponding to address
	connected_dict = {}
	
	
	buffer = 4096
	port = 5002
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("localhost", port))
	server_socket.listen(10) 
	
	# List to keep track of socket descriptors
	connected_list = [server_socket]

	prGreen("SERVER IS RUNNING ... ")

	while True:
	# Add server socket to the list of readable connections
		rList,wList,error_sockets = select.select(connected_list,[],[])
		for sock in rList:
			if sock == server_socket:
				#Accept new connection:
				new_sock, address = server_socket.accept()
				
				#Recive name from new connected client & assign unique ID with random_num + name
				name = new_sock.recv(buffer)
				name = name.decode('ascii')
				
				#assign unique_ID:
				random_num = generate_random_number(7) #Generate random string number with length 7
				unique_ID = random_num + '[' + name + ']'

				#add new socket to connected list
				connected_list.append(new_sock)
				#add new socket & unique_ID with its coresponding address to dictionary
				connected_dict[address]= [new_sock,unique_ID]

				print("Client \033[96m{}\033[00m with addess {} connected.".format(unique_ID,address))
				tem_msg = "\33[32m\r\33[1m Welcome to chatApp. Enter 'exit' anytime to exit\n\33[0m"
				new_sock.send(tem_msg.encode("ascii"))
				
				# list of online clients (unique_ID)
				online_clients = online_list(connected_dict)
				online_clients_string = '  '.join(online_clients)
				# Send client their unique ID
				ID_notification_msg = "\033[96m {}\033[00m" .format("Your ID is "+ unique_ID + "\nConnected client: " + online_clients_string) 
				new_sock.send(ID_notification_msg.encode('ascii'))
				message = "\033[95m "+unique_ID+" joined the room\033[00m"
				send_to_all(new_sock, server_socket, message.encode("ascii"))
				

			#Handle message from other clients:
			else:
				
				data1 = sock.recv(buffer)
				data_list = pickle.loads(data1) #list = ["message","uniqueID"]
				
				#Find address of the client
				address = sock.getpeername()

				#Send message to particular client by their unique ID:
				if len(data_list)== 2:
					clientID = data_list[1]
					if clientID in online_clients:
						msg="\r\33[1m"+"\33[35m "+clientID+": "+"\33[0m"+data_list[0]+"\n"
						target_address = find_add_from_ID(clientID, connected_dict)
						send_to_clientID(target_address, connected_dict, msg.encode('ascii'))
					else:
						msg = "\033[91m {} is not online\033[00m" .format(clientID)
						sock.send(msg.encode('ascii'))

				# handle when client exit:
				elif len(data_list) == 1 and data_list[0] == "exit":
					sender_ID = get_unique_ID(address, connected_dict)
					msg="\r\33[1m"+"\33[31m "+sender_ID+" left the conversation \33[0m\n"
					send_to_all(sock,server_socket, msg.encode('ascii'))
					ID = connected_dict[address]
					print("Client (%s) is offline" % ID[1])
					del connected_dict[address]
					connected_list.remove(sock)
					sock.close()
					continue

				#send message to chat room
				else:
					sender_ID = get_unique_ID(address, connected_dict)
					msg="\r\33[1m"+"\33[35m "+ sender_ID +": "+"\33[0m"+data_list[0]+"\n"
					send_to_all(sock,server_socket, msg.encode('ascii'))
	
	server_socket.close()

	

def get_unique_ID(add,dict):
	value = dict[add]
	ID = value[1]
	return ID

def online_list(dict):
	list = dict.values()
	return [i[1] for i in list]

# Generate random number with specific length
def generate_random_number(length):
    return ''.join(["%s" % randint(0, 9) for num in range(0, length)])


#Function to send message to all connected clients
def send_to_all (sock, server_sock, message):
	#Message not forwarded to server and sender itself
	for socket in connected_list:
		if socket != server_sock and socket != sock :
			try :
				socket.send(message)
			except :
				# if connection not available
				socket.close()
				connected_list.remove(socket)

def send_to_clientID(add,dict,msg):
	value = dict[add]
	sock = value[0]
	try:
		sock.send(msg)
	except:
		sock.close()
		del dict[add]
		print("\033[91m {}\033[00m" .format("Connection is not available!"))

def find_add_from_ID(id, dict):
	for addr, sock_and_id in dict.items():
		if sock_and_id[1] == id:
			return addr


if __name__ == "__main__":
	main()