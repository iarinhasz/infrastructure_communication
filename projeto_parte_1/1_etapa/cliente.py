from common import Socket
from os.path import basename
import os.path

"""
Cliente UDP

"""

# inicializar cliente
client = Socket(port=1337)

CLIENT_DIR = "files_client"

# inicializar pasta cliente
if not os.path.exists(CLIENT_DIR):
    os.makedirs(CLIENT_DIR)


print("Bem vindo ao transmissor de mensagens 3000")

comandos = [
    "Comandos disponiveis:",
    "- arquivo  | arq     : enviar arquivo",
    "- exit     | ext     : sair do programa",
    "- sdw                : desligar servidor",
]

for comando in comandos:
    print(comando)

while True:
    msg = input("> ")

    match msg:
        case "exit" | "\x18" | "ext":
            break
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
                client.receiveFileUDP(header, path=CLIENT_DIR, append="c_")
            except IOError:
                print("Nome de arquivo inválido!")
        case "sdw":
            client.sendUDP(port=5000, extra="sdw")
        case _:
            print ("Digite um comando válido!")
            for comando in comandos:
                print(comando)

client.sock.close()
