from os.path import basename
from time import sleep
from datetime import datetime
from typing import Dict
from commands import Commands, Ban
from receiver import Receiver
from sender import Sender
from common import Socket
from utils import extract_msg_server, broadcast_msg
import socket
from os.path import join as pathjoin
import os.path
import threading

"""
Servidor UDP

"""

server = Socket(port=5000)
receiver = Receiver(socket=server)
sender = Sender(socket=server)

g_address = None

SERVER_DIR = "files_server"

connected_users = {}
ongoing_bans: 'Dict[str, Ban]' = {}

# inicializar pasta server
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)

def main():
    listen_thread = threading.Thread(target=listen)
    rcv_thread = threading.Thread(target=receive)
    
    listen_thread.start()
    rcv_thread.start()
    
    listen_thread.join()
    rcv_thread.join()

def listen():
    while True:
        header, packet, address = server.rdt_rcv()
        global g_address
        g_address = address
        
        sender.incoming_pkt = (header, packet, address)
        receiver.incoming_pkt = (header, packet, address)

def receive():
    print ("Iniciando receiver...")
    global g_address

    packet, address = None, []
    isReceivingFile = False
    header = ""

    while True:
        if packet is None:
            packet = receiver.wait_for_packet()
        else:
            print(f"Novo pacote: {packet}")
            print(f"from: {g_address}")

            receive_time = datetime.now().strftime('%H:%M:%S, %m/%d/%Y')

            # so enviar se souber de onde veio
            if g_address:
                msg = packet.decode()
                sender_address = g_address
                formatted_msg = ""


                sender_name, sender_msg = extract_msg_server(msg)

                # mostrar lista para quem requisitou
                if sender_msg == Commands.SHOW_LIST_CMD:
                    sender.rdt_send(f"Usuarios conectados: {connected_users}".encode(), sender_address)
                    packet = None
                    continue # prox loop

                # banir usuario
                if sender_msg and sender_msg.startswith(Commands.BAN_CMD):
                    banned_user = sender_msg[len(Commands.BAN_CMD):]
                    if banned_user not in connected_users:
                        sender.rdt_send(f"este usuario nao existe, ou nao está mais conectado".encode(), sender_address)
                    elif banned_user not in ongoing_bans:
                        votes_needed = (len(connected_users) // 2) + 1
                        ban = Ban(
                            banned_user=banned_user, 
                            votes_needed=votes_needed, 
                            caller=sender_name
                            )
                        ongoing_bans[banned_user] = ban
                        msg = f"{sender_name} abriu uma votação para banir {banned_user}: 1/{votes_needed}"
                        broadcast_msg(connected_users, sender, sender_address, msg, include_sender=True)
                    else:
                        # checar se quem pediu o ban ja votou
                        if sender_name not in ongoing_bans[banned_user].voters:
                            ongoing_bans[banned_user].votes_count += 1
                            ongoing_bans[banned_user].voters.append(sender_name)
                            msg = f"{sender_name} votou para banir {banned_user}: {ongoing_bans[banned_user].votes_count}/{ongoing_bans[banned_user].votes_needed}"
                            broadcast_msg(connected_users, sender, sender_address, msg, include_sender=True)
                        else:
                            sender.rdt_send(f"voce ja votou para banir este usuario!".encode(), sender_address)

                        # checar se o usuario pode ser banido
                        if ongoing_bans[banned_user].votes_count >= ongoing_bans[banned_user].votes_needed:
                            # banir
                            sender.rdt_send(Commands.USER_BANNED.encode(), connected_users[banned_user])
                            del connected_users[banned_user]
                            msg = f"{banned_user} foi banido!"
                            broadcast_msg(connected_users, sender, sender_address, msg, include_sender=True)

                    packet = None
                    continue # prox loop

                # anunciar usuario
                if msg.endswith(Commands.USER_ENTERED):
                    sender_name = msg[:-len(Commands.USER_ENTERED)]
                    formatted_msg = f"servidor: {msg}"
                    # adicionar usuario conectado
                    if sender_name not in connected_users:
                        connected_users[sender_name] = sender_address
                    else: # ja existe usuario com este nome
                        sender.rdt_send(Commands.USER_ALREADY_EXISTS.encode(), sender_address)
                        packet = None
                        continue              

                formatted_msg = f"{sender_address[0]}:{sender_address[1]}/~{msg} <{receive_time}>"

                # deslogar usuario
                if sender_msg == Commands.LOGOUT_CMD:
                    if sender_name in connected_users:
                        del connected_users[sender_name]
                        formatted_msg = f"Usuario desconectado: {sender_name}"  

                broadcast_msg(connected_users, sender, sender_address, formatted_msg)

            packet = None

main()