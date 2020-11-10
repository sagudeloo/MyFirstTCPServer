import sys
import client
import server

def main ():
    serverMode = False
    host = "localhost"
    port = 4321
    path = "."
    for i in sys.argv:
        if(i == "-s"):
            serverMode = True
        elif(i[:4] == "port"):
            port = int(i[5:])
        elif(i[:4] == "host"):
            host = i[5:]
        elif(i[:4] == "path"):
            path = i[5:]
    if (serverMode):
        s = server.Server(port=port, host=host, path=path)
        s.run()
    else:
        c = client.Client(port = port, host = host)
        c.run()


if __name__ == "__main__":
    main()