import socket

class Client:

    def __init__(self, port = 4321, host = "localhost"):
        self.sock = socket.socket()
        self.host = host
        self.port = port
        self.encoding = "UTF-8"
    
    # This function start connecte the client with the server an continue de execution
    def run(self):
        self.sock.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")
        self.sendCmd("lsfl pruebita")
        x = self.readResp()
        print(x)
    
    """ Commands
        mkbk: create a new bucket
        rmbk: delete a bucket
        lsbk: list the buckets
        lsfl: list file in a bucket
        upfl: upload file
        dwfl: download file
        rmfl: delete file """
    # This function send the client commands to the server
    def sendCmd(self, command):
        self.sock.sendall(command.encode(self.encoding))

    def readResp(self):
        data = self.sock.recv(1024)
        return data.decode(self.encoding)

c = Client()
c.run()
