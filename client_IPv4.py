import socket
from threading import Thread

#import urllib.request

#globalIPv4 = urllib.request.urlopen('https://ident.me').read().decode('utf8')
#print(globalIPv4)

# localIPv4 = socket.gethostbyname(socket.gethostname())

localIPv4 = "192.168.1.208"
globalIPv4 = "87.92.16.209"

# Remember to Disable firewall for clients in other networks to be able to connect to the server

port_IPv4 = 34000
buffer = 4096
backlog = 5

def receive(clientSocketIPv4):
    while True:
        message = clientSocketIPv4.recv(buffer).decode("utf8")
        if message.startswith("/downloaded"):
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
    address_IPv4 = (globalIPv4, port_IPv4)
    clientSocketIPv4.connect(address_IPv4)

    receive_thread = Thread(target=receive, args=(clientSocketIPv4,))
    send_thread = Thread(target=send, args=(clientSocketIPv4,))
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    main()