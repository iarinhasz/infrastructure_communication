import socket
import select
import time
UDP_IP = "127.0.0.1" #localhost
IN_PORT = 5005
timeout = 3
#GRUPO : LL2, PSGS, RNM4
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, IN_PORT))

print("Aguardando...")

while True:
    #Receber do cliente
    data, addr = sock.recvfrom(1024)
    if data:
        file_name = "sentbyclient_" + str(data).split("'")[1]
        print ("Nome do arquivo:", data)
       


    f = open(file_name, 'wb')

    while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            f.write(data)
        else:
            print ("%s Terminou!" % file_name)
            f.close()
            break
    

    #Server enviando para o cliente 
    
    sock.sendto(file_name.encode(),(addr))
    print (f"Servidor está enviando {file_name}...")
    f = open(file_name, "rb")
    dado_servidor = f.read(1024)
    while(dado_servidor):
        if(sock.sendto(dado_servidor, (addr))):
            dado_servidor = f.read(1024)
            time.sleep(0.02)
    f.close()
            



