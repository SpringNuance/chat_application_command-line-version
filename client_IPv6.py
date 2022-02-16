import socket
from socket import AF_INET6, SOCK_STREAM
from threading import Thread

localIPv6 = "fe80::c10c:de5e:2cbf:132c%9"
globalIPv6 = "2001:14ba:a0bd:dd00:c10c:de5e:2cbf:132c"

# Remember to Disable firewall for clients in other networks to be able to connect to the server

portIPv6 = 36000
buffer = 1024
backlog = 5

def receive(clientSocketIPv6):
    while True:
        message = clientSocketIPv6.recv(buffer).decode("utf8")
        if message.startswith("/downloaded"):
            fileData = message.split("\n")[1]
            fileName = message.split("\n")[2]
            newFile = open(fileName, "a")
            newFile.write(fileData)
            newFile.close()
        else:
            print(message)

def send(clientSocketIPv6):
    message = input(">>> ")
    while message != "/quit":
        clientSocketIPv6.send(bytes(message, "utf8"))
        message = input(">>> ")
    print("You have quitted from the server. See you again")
    clientSocketIPv6.send(bytes(message, "utf8"))

def main():
    clientSocketIPv6 = socket.socket(AF_INET6, SOCK_STREAM)
    addressIPv6 = (globalIPv6, portIPv6)
    clientSocketIPv6.connect(addressIPv6)
        
    receive_thread = Thread(target=receive, args=(clientSocketIPv6,))
    send_thread = Thread(target=send, args=(clientSocketIPv6,))
    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    main()