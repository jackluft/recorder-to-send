import socket
import pickle
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 4579
s.bind((host,port))
s.listen(2)
client = []
chunk_size = 4096
def recv_data(conn):
    while True:
        data = b""
        data_size = 0
        size = conn.recv(10).decode('UTF-8')
        print("Size recieved")
        while data_size < int(size):
            if(data_size+chunk_size) > int(size):
                re = conn.recv(int(size)-data_size)
            else:
                re = conn.recv(chunk_size)
            data+=re
            data_size+=len(re)
        print("All Data recieved")
        for c in client:
            if c!= conn:
                c.send(size.encode('UTF-8'))
                c.send(data)
                print("Data sent to client")
        print("Done")
    conn.close()


while True:
    print("Waiting for Connections.....")
    conn, adr = s.accept()
    client.append(conn)
    print("Connection from "+str(adr))
    threading.Thread(target=recv_data,args=(conn,)).start()

