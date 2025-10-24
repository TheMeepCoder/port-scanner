#!/usr/bin/env python3
"""
Network Scanner Project
Students: [Linea, Linus, Mattias Lavsund, Magnus]
Date: [20-10-2025]
"""
#To test the program: scanme.nmap.org

#22 is a port that is open
#21 is a port that is closed
#33 is a port that dose not exist/cannot be reached

import socket
import sys



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
target = input('What you want to scan?: ')

# getting the ip address using gethostbyname
# function
t_IP = socket.gethostbyname(target)
print("Starting scan on host: ", t_IP)


def port_scan(port):
    try:
        s.connect((t_IP, port))
        return True
    except:
        print("connection failed")
        return False


choice = int(input("do you wish to scan 1. a single or 2. multiple ports?" ))

def port_scan_single():

    port = int(input("Enter the port number to be scanned: "))

    if port_scan(port):
        print('Port', port, 'is open')
    else:
        print("port", port, "is closed")

def port_scan_multi():
    port = int(input("which port? "))
    inter = int(input("how many ports? "))
    port_inter = port + inter

    for port in range(port, port_inter):
        if port_scan(port):
            print(f"port {port} is open")
        else:
            print(f"port {port} is closed")

if choice == 1:
    port_scan_single()
elif choice == 2:
    port_scan_multi()



s.close()

if __name__ == "__main__":
    pass
