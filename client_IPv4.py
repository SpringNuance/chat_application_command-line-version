import socket
from threading import Thread
#import urllib.request

#globalIPv4 = urllib.request.urlopen('https://ident.me').read().decode('utf8')
#print(globalIPv4)

#localIPv4 = socket.gethostbyname(socket.gethostname())
localIPv4 = "192.168.1.208"
globalIPv4 = "78.27.114.0"
# 192.168.1.208
# public ipv4 address of my local computer 78.27.114.0 Disable firewall
# punch a hole through my router 
# client would run on any laptop
port_IPv4 = 34000
buffer = 4096
backlog = 5

def receive(clientSocketIPv4):
    while True:
        message = clientSocketIPv4.recv(buffer).decode("utf8")
        if message.startswith("The file has been successfully saved"):
            fileData = message.split("\n")[1]
            fileName = message.split("\n")[2]
            newFile = open(fileName, "a")
            newFile.write(fileData)
            newFile.close()
        else:
            print(message)

def send(clientSocketIPv4):
    message = input(">>> ")
    while message != "/quit":
        clientSocketIPv4.send(bytes(message, "utf8"))
        message = input(">>> ")
    print("You have quitted from the server. See you again")
    clientSocketIPv4.send(bytes(message, "utf8"))

def main():
    clientSocketIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address_IPv4 = (localIPv4, port_IPv4)
    clientSocketIPv4.connect(address_IPv4)
    # instead of connecting local host ipv4, actually connect to the public ipv4 of this local computer
    receive_thread = Thread(target=receive, args=(clientSocketIPv4,))
    send_thread = Thread(target=send, args=(clientSocketIPv4,))
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    main()