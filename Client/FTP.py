from socket import *
import os
HOST = '127.0.0.1'
PORT = 12000
directory = "D:/acer/Documents/Academia/UBCO/Y4/COSC328/Labs/L03/Client/"
#filesize = os.path.getsize(filename)

# set up the tcp socket
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((HOST, PORT))

while (True):
    s = input("Message: ")
    sock.sendall(s.encode("utf-8"))
    data = sock.recv(1024).decode("utf-8")

    if "PUT" in data:
        filename = input("Enter file name: ")
        # try statement to handle invalid paths or missing file
        try:
            f = open(os.path.join(directory,filename), "rb")
            # open the file in read mode
            print("File open")
        except IOError as error:
            print(error)
        # begin read data of the file to be sent
        byte = f.read(1024)
        print("Byte read")
        # while there is byte to read, keep sending
        while(byte):
            sock.send(byte)
            print("Sending")
            # read in new byte for sending
            byte = f.read(1024)
        f.close()
        #sock.shutdown(socket.SHUT_RDWR)
        # Tell server file is transferred
        #after sending close resources
        print("File sent")
        sock.close()

    if "GET" in data:
        filename = input("What file do you wish to retreive:")
        f = open(os.path.join(directory,filename), 'wb')
        # Send name as encoded byte format
        name = sock.send(filename.encode("utf-8"))
        print("Transfer begin")
        # Start to receive the packages form server
        byte = sock.recv(1024)
        # Continue until no more packages are sent
        while(byte):
            f.write(byte)
            byte = sock.recv(1024)
            print("Receiving")
        print("Transfer done")
        sock.close()

    if "CLOSE" in data:
        # First close the socket since we don't use it anymore
        sock.close()
        print("Connection closed")
        # take input before establishing new connection
        nHost = input("New host IP:")
        print("Connection to new server")
        sock.connect(nHost,PORT)

    if data == "QUIT":
        break

sock.close()

"""

The base setup code was taken from the lab assignment page
Transfer setup and general references were from:
https://www.thepythoncode.com/code/send-receive-files-using-sockets-python
https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
https://www.binarytides.com/python-socket-server-code-example/
os.join.path command was shown by:
https://stackoverflow.com/questions/29110620/how-to-download-file-from-local-server-in-python

"""
