import socket, select
from random import randint
import pickle

from simplecrypt import encrypt, decrypt
cipher_key = 'secret ingredient'

# COLORED TEXT FUNCTIONS
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

connected_list =[]

def main():
    name=""
    global connected_list
    #dictionary to store socket object and uniqure ID corresponding to address
    connected_dict = {}


    buffer = 4096
    port = 5000

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
                name = decrypt(cipher_key, name)
                name = name.decode('ascii')

                #assign unique_ID:
                random_num = generate_random_number(3) #Generate random string number with length 3
                unique_ID = random_num + '[' + name + ']'

                #add new socket to connected list
                connected_list.append(new_sock)
                #add new socket & unique_ID with its coresponding address to dictionary
                connected_dict[address]= [new_sock,unique_ID]

                print("Client \033[96m{}\033[00m with addess {} connected.".format(unique_ID,address))
                tem_msg = "\33[32m\r\33[1m Welcome to chatApp. Enter '.exit' anytime to exit\n\33[0m"
                tem_msg_encrypted = encrypt(cipher_key, tem_msg)
                #new_sock.send(tem_msg.encode("ascii"))
                new_sock.send(tem_msg_encrypted)

                # list of online clients (unique_ID)
                online_clients = online_list(connected_dict)
                online_clients_string = '  '.join(online_clients)
                # Send client their unique ID
                ID_notification_msg = "\033[96m {}\033[00m" .format("Your ID is "+ unique_ID + "\nConnected client: " + online_clients_string +"\n")
                #ID_notification_msg = "\033[96m {}\033[00m" .format("Your ID is "+ unique_ID +"\n")
                ID_notification_msg_encrypted = encrypt(cipher_key,ID_notification_msg)
                #new_sock.send(ID_notification_msg.encode('ascii'))
                new_sock.send(ID_notification_msg_encrypted)

                message = "\033[95m " + unique_ID + " joined the room\n\033[00m"
                #message_encrypted = encrypt(cipher_key,message)
                send_to_all(new_sock, server_socket, message.encode("ascii"))
                #send_to_all(new_sock, server_socket, message_encrypted)


            #Handle message from other clients:
            else:

                data1 = sock.recv(buffer)
                data_list = pickle.loads(data1) #list = ["message","uniqueID"]

                #Find address of the client
                address = sock.getpeername()

                #Send message to particular client by getting their unique ID:
                if len(data_list)== 2:
                    #print(data_list)
                    clientID = data_list[1]
                    if clientID in online_clients:
                        sender_ID = connected_dict[address][1]
                        #print(sender_ID)
                        msg="\r\33[1m"+"\33[35m "+sender_ID+": "+"\33[0m"+data_list[0]+"\n"
                        target_address = find_add_from_ID(clientID, connected_dict)
                        #send_to_clientID(target_address, connected_dict, msg.encode('ascii'))
                        send_to_clientID(target_address, connected_dict, msg)
                    else:
                        msg = "\033[91m {} is not online\033[00m" .format(clientID)
                        msg_encrypted = encrypt(cipher_key, msg)
                        #sock.send(msg.encode('ascii'))
                        sock.send(msg_encrypted)

                # handle when client exit:
                elif len(data_list) == 1 and data_list[0] == ".exit":
                    sender_ID = get_unique_ID(address, connected_dict)
                    msg="\r\33[1m"+"\33[31m "+sender_ID+" left the conversation \33[0m\n"
                    #send_to_all(sock,server_socket, msg.encode('ascii'))
                    send_to_all(sock,server_socket, msg)
                    ID = connected_dict[address]
                    print("Client (%s) is offline" % ID[1])
                    del connected_dict[address]
                    connected_list.remove(sock)
                    sock.close()
                    continue

                #send message to chat room
                else:
                    sender_ID = get_unique_ID(address, connected_dict)
                    msg="\r\33[1m"+"\33[35m " + sender_ID +": "+"\33[0m"+data_list[0]+"\n"
                    #send_to_all(sock,server_socket, msg.encode('ascii'))
                    send_to_all(sock,server_socket, msg)

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
    message_encrypted = encrypt(cipher_key, message)
    for socket in connected_list:
        if socket != server_sock and socket != sock :
            try :
                socket.send(message_encrypted)
            except :
                # if connection not available
                socket.close()
                connected_list.remove(socket)

def send_to_clientID(add,dict,msg):
    value = dict[add]
    sock = value[0]
    msg_encrypted = encrypt(cipher_key, msg)
    try:
        sock.send(msg_encrypted)
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
