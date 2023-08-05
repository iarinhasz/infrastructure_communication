from common import Socket
from os.path import basename
import os.path

"""
Cliente UDP

"""

# inicializar cliente
client = Socket(port=1337, server=True)

CLIENT_DIR = "files_client"

# inicializar pasta cliente
if not os.path.exists(CLIENT_DIR):
    os.makedirs(CLIENT_DIR)


print("Bem vindo ao transmissor de mensagens 3000\nDigite CTRL+X para sair")
print("Comandos disponiveis:")
print("- arquivo  | arq     : enviar arquivo")
print("- mensagem | msg     : enviar mensagem")
print("- shutdown | sdw     : desligar servidor")
print("- exit     | ext     : sair do programa\n\n")

while True:
    msg = input("> ")

    match msg:
        case "exit" | "\x18" | "ext":
            break
        case "mensagem" | "msg":
            mensagem = input("> Digite sua mensagem:\n> ")
            # enviar mensagem com o header mensagem
            client.sendUDP(mensagem.encode())
        case "arquivo" | "arq":
            filename = input("> Digite o nome do arquivo:\n> ")
            try:
                # enviar o arquivo
                with open(filename, "rb") as f:
                    client.sendUDP(
                        port=5000,
                        msg=f.read(),
                        filename=basename(filename),
                    )

                # receber de volta
                header, _ = client.receiveHeaderUDP()
                client.receiveFileUDP(header, path=CLIENT_DIR)
            except IOError:
                print("Nome de arquivo inválido!")
        case "sdw":
            client.sendUDP(port=5000, extra="sdw")

client.sock.close()
