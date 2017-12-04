import socket
import os
import _thread
import time

def communicate():
    s = socket.socket()
    host = "143.248.158.213"
    #host = "127.0.0.1"
    port = 9000

    s.connect((host, port))
    path = "detector/patches"
    directory = os.listdir(path)
    for files in directory:
        print (files)   
        filename = files
        size = len(filename)
        size = bin(size)[2:].zfill(16) # encode filename size as 16 bit binary
        time.sleep(0.1)
        #size = bytes(size, 'utf-8')
        print(size)
        print(type(size))
        #print(filename)
        s.send(size.encode())
        s.send(filename.encode())

        filename = os.path.join(path,filename)
        filesize = os.path.getsize(filename)
        filesize = bin(filesize)[2:].zfill(32) # encode filesize as 32 bit binary
        s.send(filesize.encode())

        file_to_send = open(filename, 'rb')

        l = file_to_send.read()
        s.sendall(l)
        file_to_send.close()
        print ('File Sent')

    # s.recv(4066)
    s.close()

    # Phase 2

    print("Phase 2")
    g = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    g.connect(("8.8.8.8", 80))
    host2 = g.getsockname()[0]
    #host2 = socket.gethostbyname(socket.getfqdn())
    port = 9100
    print("Making Socket...")
    s = socket.socket()             # Create a socket object
    print("Binding ...")
    s.bind((host2, port))            # Bind to the port
    print("Listening ... ")
    s.listen(1)                     # Now wait for client connection.
    print("End ...")

    while True:
        conn, addr = s.accept()     # Establish connection with client.
        print ("File Created")
        with open('test_result.txt', 'w') as f:
            recv_flag = False
            while True:
    			#print ("A")
                data = conn.recv(4096).decode()
    			#print ("B")
                print('data= %s' % (data))
                print(type(data))
                if (data == ''):
                    break
    			#print ("C")
                f.write(data)
    			#print ("D")
        break
    s.close()

if __name__ == "__main__":
    communicate()
