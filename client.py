import socket
import threading
import sys
import os
import time

class Client:

    def __init__(self, port = 4321, host = "localhost"):
        self.sock = socket.socket()
        self.host = host
        self.port = port
        self.dataPort = port+1
        self.encoding = "UTF-8"
    
    # This function start connecte the client with the server an continue de execution
    def run(self):
        try:
            self.sock.connect((self.host, self.port))
        except:
            print("Unable to establish a connection with the server.")
            sys.exit(1)
        print(f"Connected to {self.host}:{self.port}")
        try:
            while True:
                cmd = self.readCmd()
                commandStatus = self.interpretCmd(cmd)
                if commandStatus:
                    resp = self.readResp().decode(self.encoding)
                    print(resp[1:])
        except KeyboardInterrupt:
            self.sock.close()
            print("\nThe Client has been closed.")
            sys.exit(1)

    def readCmd(self):
        rawCmd = input(">>> ")
        rawCmd = rawCmd.strip()
        return rawCmd

    def interpretCmd(self, command):
        splitedCmd = command.split(" ")
        cmd = splitedCmd[0]
        args = splitedCmd[1:]
        if (cmd == "mkbk"):
            if (len(args) >= 1):
                self.sendCmd(cmd+" "+args[0])
                return True
            else:
                print("Missing arguments")
                return False
        elif (cmd == "rmbk"):
            if (len(args) >= 1):
                self.sendCmd(cmd+" "+args[0])
                return True
            else:
                print("Missing arguments")
                return False
        elif (cmd == "rmfl"):
            if (len(args) >= 2):
                self.sendCmd(cmd+" "+args[0]+" "+args[1])
                return True
            else:
                print("Missing arguments")
                return False
        elif (cmd == "lsbk"):
            self.sendCmd(cmd)
            return True
        elif (cmd == "lsfl"):
            if (len(args) >= 1):
                self.sendCmd(cmd+" "+args[0])
                return True
            else:
                print("Missing arguments")
                return False
        elif (cmd == "upfl"):
            if (len(args) >= 2):
                x = threading.Thread(target=self.uploadFile, args=(args[0],args[1],args[2]))
                x.start()
                return False
            else:
                print("Missing arguments")
                return False
        elif (cmd == "dwfl"):
            if (len(args) >= 2):
                x = threading.Thread(target=self.downloadFile, args=(args[0],args[1]))
                x.start()
                return False
            else:
                print("Missing arguments")
                return False
        elif (cmd == "help"):
            return False
        else:
            return False
    
    """ Commands
        mkbk: create a new bucket
        rmbk: delete a bucket
        rmfl: delete file
        lsbk: list the buckets
        lsfl: list file in a bucket
        upfl: upload file
        dwfl: download file """

    # This function send the client commands to the server
    def sendCmd(self, command):
        self.sock.sendall(command.encode(self.encoding))

    def readResp(self):
        data = self.sock.recv(1024)
        return data

    def uploadFile(self, bucketName, fileName, filePath):
        if(self.fileExists(filePath)):
            self.sendCmd(f"upfl {bucketName} {fileName}")
            time.sleep(1)
            dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataSock.connect((self.host, self.dataPort))
            with open(os.path.join(filePath), "rb") as file:
                data = file.read(1024)
                while (data):
                    dataSock.sendall(data)
                    data = file.read(1024)
            dataSock.close()
            return "0 Download finished."
        else:
            return "1 File does not exist."

    def downloadFile(self, bucketName, fileName):
        self.sendCmd(f"dwfl {bucketName} {fileName}")
        time.sleep(1)
        dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataSock.connect((self.host, self.dataPort))
        with open(os.curdir+"/"+fileName, "wb") as file:
            data = dataSock.recv(1024)
            while (data):
                file.write(data)
                data = dataSock.recv(1024)
        dataSock.close()
        return "0 Download finished."

    def fileExists(self, filePath):
        return os.path.isfile(filePath)