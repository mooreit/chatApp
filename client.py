import socket, select, string
import sys, pickle

# COLORED TEXT FUNCTIONS
def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

def display() :
	you="\33[33m\33[1m"+" You: "+"\33[0m"
	sys.stdout.write(you)
	sys.stdout.flush()

def main():
	# Read from command line
	if len(sys.argv)<2:
		host = input("Enter host ip address: ")
	else:
		host = sys.argv[1]

	port = 5002

	#asks for user name
	prCyan("CREATING NEW ID")
	name = input("\033[96m {}\033[00m".format("Enter user name: "))

	#Creating socket and connect to server
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		client_socket.connect((host, port))
	except:
		prRed("NO CONNECTION!")
		sys.exit()


	#send name to server:
	client_socket.send(name.encode('ascii'))

	# join chat room or send private message to another client.
	
	while True:
		# Select method with multiple sockets, await a read event.
		rlist, wlist, elist = select.select([sys.stdin, client_socket] , [], [])

		for sock in rlist:
			#Receive message from server
			if sock == client_socket:
				data = sock.recv(4096)
				if not data :
					prRed("Disconnect!")
					sys.exit()
				else :
					sys.stdout.write(data.decode('ascii'))
					




			#user entered a message
			else:
				input_str = input("\033[93m YOU: \033[00m")
				string_list = [x.strip() for x in input_str.split('$$')]
				msg_list = pickle.dumps(string_list)
				client_socket.send(msg_list)
				display()


if __name__ == "__main__":
	main()
