from sender import Sender
from receiver import Receiver
from common import Socket
from os.path import basename
import os.path
import threading

"""
Cliente UDP

"""

client = Socket(port=1337)
sender = Sender(socket=client)
receiver = Receiver(socket=client)

# inicializar cliente
CLIENT_DIR = "files_client"

# definir servidor para onde vao ser enviados os arquivos
server_ip = "localhost"
server_port = 5000
server_address = (server_ip, server_port)

# inicializar pasta cliente
if not os.path.exists(CLIENT_DIR):
    os.makedirs(CLIENT_DIR)

def main():
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
    print ("Iniciando receiver...")

    packet, address = None, []
    isReceivingFile = False
    header = ""

    try:
        while True:
            if packet is None:
                packet = receiver.wait_for_packet()
            else:
                print(f"Novo pacote: {packet}")

                if not isReceivingFile and packet[:len(Socket.HEADER_START)] == Socket.HEADER_START.encode():
                    header = packet.decode().split(",")
                    isReceivingFile = True
                    print(f"Header recebido: {header}")
                if isReceivingFile:
                    filename = receiver.sock.receive_file(receiver=receiver, header=header, path=CLIENT_DIR, append="c_")
                    isReceivingFile = False

                packet = None
    except TimeoutError:
        client.sock.settimeout(None)

def send():
    print ("Iniciando sender...")
    print("Bem vindo ao transmissor de mensagens 3000")

    comandos = [
        "Comandos disponiveis:",
        "- arquivo  | arq     : enviar arquivo",
        "- {qualquer string}  : enviar string"
    ]

    arquivos = [
        "Arquivos de teste:",
        "- cheems       : arquivo .png (66 kB)", 
        "- declaration  : arquivo .txt longo (8182 bytes)", 
        "- short        : arquivo .txt curto (28 bytes)", 
        "- empty        : arquivo .txt vazio (0 bytes)", 
    ]

    for comando in comandos:
        print(comando)

    while True:
        msg = input("Digite um comando:  ")

        match msg:
            case "exit" | "\x18" | "ext":
                break
            case "arq" | "arquivo":
                print ("> Digite o nome do arquivo de teste, ou o caminho para um arquivo:")

                for arquivo in arquivos:
                    print(arquivo)

                filename = input("> ")                

                match filename:
                    case "cheems":
                        filename = "../test_files/cheems.png"
                    case "declaration":
                        filename = "../test_files/declaration.txt"
                    case "short":
                        filename = "../test_files/short.txt"
                    case "empty":
                        filename = "../test_files/empty.txt"

                try:
                    # enviar o arquivo
                    with open(filename, "rb") as f:
                        sender.sock.send_file(
                            sender=sender,
                            ip=server_ip,
                            port=server_port,
                            msg=f.read(),
                            filename=basename(filename)
                        )

                except IOError:
                    print("Nome de arquivo inválido!")
                except:
                    print("Algum erro ocorreu")

            case _:
                sender.rdt_send(msg, server_address)

main()