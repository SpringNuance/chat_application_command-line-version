import client_IPv4, client_IPv6

def main():
    IPv4or6 = input("Which version of IP would you like to connect, IPv4 or IPv6? Please type 4/6\n>>> ")
    while IPv4or6 != "4" and IPv4or6 != "6":
        IPv4or6 = input("Unknown IP version. Please type 4/6\n>>> ")
    if IPv4or6 == "4":
        client_IPv4.main()
    else:
        client_IPv6.main()

if __name__ == "__main__":
    main()