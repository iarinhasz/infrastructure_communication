from common import Socket
from os.path import join as pathjoin
import os.path

"""
Servidor UDP

"""


server = Socket(port=5000, server=True)

SERVER_DIR = "files_server"

# inicializar pasta sever
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)


header, address = None, []

while True:
    if header is None:
        header, address = server.receiveHeaderUDP()

    else:
        # comando de debug para desligar o servidor remotamente
        if header[Socket.Header.EXTRA] == "sdw":
            break

        # receber o arquivo
        server.receiveFileUDP(header, path=SERVER_DIR)
        # enviar de volta
        with open(pathjoin(SERVER_DIR, header[Socket.Header.FILENAME]), "rb") as f:
            server.sendUDP(
                ip=address[0],
                port=address[1],
                msg=f.read(),
                filename=header[Socket.Header.FILENAME],
            )
        # resetar o estado de header para receber outro arquivo
        header = None


server.sock.close()
