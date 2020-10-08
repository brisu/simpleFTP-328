from socket import *
import os

HOST = '127.0.0.1'
PORT = 12000

# set up the tcp socket
sock = socket(AF_INET, SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
directory = "D:/acer/Documents/Academia/UBCO/Y4/COSC328/Labs/L03/Server/"
f = open("D:/acer/Documents/Academia/UBCO/Y4/COSC328/Labs/L03/Server/Hello.txt", "wb")

# listen for a connection
conn, addr = sock.accept()
print("Connected to " , addr)
while (True):
    data = conn.recv(1024).decode("utf-8").upper()
    print(data)
    conn.sendall(data.encode("utf-8"))

    if "PUT" in data:
        print("Begin transmission")
        # start to receive file from clients
        byte = conn.recv(1024)
        print("Byte read")
        # as long as client is sending data, receive
        while(byte):
            f.write(byte)
            byte = conn.recv(1024)
            print("Receiving")
        # exits receive once client has finished transmission
        print("Done transfer")
        conn.close()

    if "GET" in data:
        print("Has GET")
        filename = conn.recv(1024).decode("utf-8")
        print("Received name")
        try:
            f = open(os.path.join(directory,filename),'rb')
            print("Opening the file")
        except IOError as error:
            print(error)
        filesize = f.read(1024)
        while(filesize):
            conn.send(filesize)
            print("Transferring")
            filesize = f.read(1024)
        # Sending file as the same method via client side
        f.close()
        print("Transfer complete")
        conn.close()

    if data == "QUIT":
        break
conn.close()
sock.close()
