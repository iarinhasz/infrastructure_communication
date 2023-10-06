from commands import Commands
from sender import Sender
from receiver import Receiver
from common import Socket
from os.path import basename
from utils import extract_msg, broadcast_msg
import os.path
import threading
import random

"""
Cliente UDP

"""

client = Socket(port=random.randrange(10000, 40000))
sender = Sender(socket=client)
receiver = Receiver(socket=client)

# inicializar cliente
CLIENT_DIR = "files_client"

# definir servidor para onde vao ser enviados os arquivos
server_ip = "127.0.0.1"
server_port = 5000
server_address = (server_ip, server_port)
friends = []

# inicializar pasta cliente
if not os.path.exists(CLIENT_DIR):
    os.makedirs(CLIENT_DIR)

username = None

def main():
    global username
    # login
    print(f"Bem vindo à sala de chat. Digite '{Commands.LOGIN_CMD}<nome>' para se conectar")
    
    while True: 
        msg = input()
        if msg.startswith(Commands.LOGIN_CMD):
            username = msg[len(Commands.LOGIN_CMD):]
            if len(username) > 0:
                break
    
    listen_thread = threading.Thread(target=listen)
    send_thread = threading.Thread(target=send)
    rcv_thread = threading.Thread(target=receive)
    
    listen_thread.start()
    send_thread.start()
    rcv_thread.start()
    
    listen_thread.join()
    send_thread.join()
    rcv_thread.join()
    

def listen():
    while True:
        header, packet, address = client.rdt_rcv()
        sender.incoming_pkt = (header, packet, address)
        receiver.incoming_pkt = (header, packet, address)

def receive():
    packet, address = None, []

    while True:
        if packet is None:
            packet = receiver.wait_for_packet()
        else:
            msg = packet.decode()

            if msg == Commands.USER_ALREADY_EXISTS:
                print("ja existe um usuario com este nome, tente novamente")
                os._exit(1)
            
            if msg == Commands.USER_BANNED:
                print("você foi banido!")
                os._exit(1)
            
            sender_address, sender_name, message = extract_msg(msg)

            if sender_name and message:
                if sender_name in friends:
                    msg = msg.replace(sender_name, f"[amigo] {sender_name}")
                print(msg)
            else: 
                print(msg)
            packet = None

def send():
    global username
    print (f"Bem vindo {username}!\n")

    greeting = f"{username}{Commands.USER_ENTERED}"
    sender.rdt_send(greeting, server_address)

    print (f"Digite sua mensagem!")

    while True:
        msg = input("")
        send_msg = f"{username}: {msg}"

        match msg:
            case s if s.startswith(Commands.ADD_FRIEND_CMD):
                friend = s[len(Commands.ADD_FRIEND_CMD):]
                if friend not in friends:
                    friends.append(friend)
                    print (f"add friend: {friend}")
                else:
                    print("este usuario já é seu amigo")
                pass
            case s if s.startswith(Commands.REMOVE_FRIEND_CMD):
                friend = s[len(Commands.REMOVE_FRIEND_CMD):]
                if friend in friends:
                    friends.remove(friend)
                    print (f"remove friend: {friend}")
                else: 
                    print("nao há amigo com este nome")
                pass
            case s if s.startswith(Commands.BAN_CMD):
                sender.rdt_send(send_msg, server_address)
                pass
            case s if s.startswith(Commands.SHOW_LIST_CMD):
                sender.rdt_send(send_msg, server_address)
                pass
            case s if s.startswith(Commands.SHOW_FRIEND_LIST_CMD):
                if len(friends) > 0:
                    print (f"amigos: {', '.join(friends)}")
                else:
                    print ("você não tem amigos!")
                pass
            case s if s.startswith(Commands.LOGOUT_CMD):
                sender.rdt_send(send_msg, server_address)
                print ("Deslogado!")
                os._exit(1)
            case "/help":
                print (f"comandos disponiveis: {Commands.ALL_CMDS}")
            case _:
                sender.rdt_send(send_msg, server_address)

main()