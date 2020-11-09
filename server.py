import os
import shutil
import socket
import threading

class Server:

    def __init__(self, port=4321, host="localhost", path=".", encoding="UTF-8"):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.path = path
        self.connections = list()
        self.sock.bind((self.host, self.port))
        self.encoding = encoding
    
    def run(self):
        try:
            self.sock.listen(10)
            print("Server started...")
            i = 0
            while True:
                conn, addr = self.sock.accept()
                print(f"Accepted connection from {addr}.")
                # connType = self.read(conn).decode(self.encoding)
                x = threading.Thread(target=self.runClient, args=(conn, addr,))
                x.start()
                self.connections.append(x)
            for x in connections:
                x.join()
        except KeyboardInterrupt:
            self.sock.close()

    # This funtion run a thread with the client connection
    def runClient(self, conn, addr): 
        connState = True
        print("Connection thread created.")
        while connState:
            cmd = self.read(conn).decode(self.encoding)
            if cmd:
                print(f"Command: {cmd}, from {addr}")
                cmdResponse = self.interpretCmd(cmd)
                print(f"Response: {cmdResponse}, to {addr}")
                self.send(conn, bytes(cmdResponse, self.encoding))

    # This funtion wait for a command from client connection
    def read(self, conn):
        data = ""
        data = conn.recv(1024)
        return data

    def send(self, conn, data):
        conn.sendall(data)

    """ Commands
        mkbk: create a new bucket
        rmbk: delete a bucket
        lsbk: list the buckets
        lsfl: list file in a bucket
        upfl: upload file
        dwfl: download file
        rmfl: delete file """
    # This function interpret a command and execute respective instruction
    def interpretCmd(self, cmd):
        cmdKey = cmd[:4]
        args = cmd[4:].split(" ")
        if (cmdKey == "mkbk"):
            return self.makeBucket(args[1])
        elif (cmdKey == "rmbk"):
            return self.removeBucket(args[1])
        elif (cmdKey == "lsbk"):
            return self.listBuckets()
        elif (cmdKey == "lsfl"):
            return self.listFiles(args[1])
        elif (cmdKey == "upfl"):
            return self.recv(args[1], args[2])
        elif (cmdKey == "dwfl"):
            return self.sendFile(args[1], args[2])
        elif (cmdKey == "rmfl"):
            return self.removeFile(args[1], args[2])
        else:
            return "Command not found."

    def makeBucket(self, bucketName):
        if (not self.bucketExists(bucketName)):
            os.mkdir(self.path+"/"+bucketName)
            return "0 Bucket successfully created."
        else:
            return "1 Bucket already exist."

    def removeBucket(self, bucketName):
        if (self.bucketExists(bucketName)):
            shutil.rmtree(self.path+"/"+bucketName)
            return "0 Bucket successfully removed."
        else:
            return "1 Bucket does not exist."
    
    def listBuckets(self):
        buckets = ""
        with os.scandir(self.path) as it:
            for entry in it:
                if (not entry.name.startswith('.')) and (not entry.is_file()):
                    buckets += entry.name + "\n"
        return "0 " + buckets

    def listFiles(self, bucketName):
        files = ""
        if (self.bucketExists(bucketName)):
            with os.scandir(self.path+"/"+bucketName) as it:
                for entry in it:
                    if (not entry.name.startswith('.')) and (entry.is_file()):
                        files += entry.name + "\n"
            return "0 " + files
        else:
            return "1 Bucket does not exist."
    
    def recvFile(self):
        pass
    
    def sendFile(self, conn):

        if (bucketExists(bucketName)):
            if(fileExists(bucketName, fileName)):
                send(conn, b"0 Okay")
                with open(self.path+"/"+bucketName+"/"+fileName, "rb") as file:
                    data = file.read(1024)
                while (data):
                    send(conn, data)
                    data = file.read(1024)
            else:
                return "1 File does not exist."
        else:
            return "1 Bucket does not exist."
        return "0 Transmission finished."
    
    def removeFile(self, bucketName, fileName):
        if (os.path.exists(self.path+"/"+bucketName+"/"+fileName)):
            os.remove(self.path+"/"+bucketName+"/"+fileName)
            return "0 File successfully removed."
        else:
            return "1 File does not exist."

    def bucketExists(self, bucketName):
        return os.path.isdir(self.path+"/"+bucketName)
    
    def fileExists(self, bucketName, fileName):
        return os.path.isfile(self.path+"/"+bucketName+"/"+fileName)

s = Server()
s.run()