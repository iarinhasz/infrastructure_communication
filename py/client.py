import socket
import time
import sys
import select
#GRUPO : LL2, PSGS, RNM4
UDP_IP = "127.0.0.1" #localhost
UDP_PORT = 5005
buf = 1024
file_name = str(input("Digite o nome do seu arquivo: "))
timeout = 3

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(file_name.encode(), (UDP_IP, UDP_PORT))
print (f"Enviando {file_name}")

f = open(file_name, "rb")
data = f.read(buf)
while(data):
    if(sock.sendto(data, (UDP_IP, UDP_PORT))):
        data = f.read(buf)
        time.sleep(0.02) 
        

        
#Cliente recebendo o arquivo...
dado_cliente, addr = sock.recvfrom(1024)
if dado_cliente:
    print ("Nome do arquivo:", dado_cliente)
    file_name_recebido_cliente = str(dado_cliente).split("'")[1].replace("sentbyclient", "sentbackbyserver")


    f = open(file_name_recebido_cliente, 'wb')

    while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            dado_cliente, addr = sock.recvfrom(1024)
            f.write(dado_cliente)
        else:
            print ("%s Terminou!" % file_name_recebido_cliente )
            f.close()
            break

sock.close()
f.close()

