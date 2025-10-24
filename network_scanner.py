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

def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    #Return true if port is open, else false
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #with function closes after it's done
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False
        
def get_service_name(port: int) -> str:
    #adtempt to identify sverice of given port
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"
    
def scan_single_port(host: str):
    port = int(input("Enter the port number to be scanned: "))
    if is_port_open(host, port):
        print(f"Port {port} is open. Service: {get_service_name(port)}")
    else:
        print(f"Port {port} is closed or cannot be reached.")

def scan_multi_ports(host: str, start_port: int, end_port: int):
    for port in range(start_port, end_port + 1):
        if is_port_open(host, port):
            print(f"Port {port} is open. Service: {get_service_name(port)}")
        else:
            print(f"Port {port} is closed or cannot be reached.")


if __name__ == "__main__":
    host = input("Host to scan(ip or hostname, default localhost) or localhost ")
    
    choice = int(input("1. scan a single or 2. scan multiple? "))
    if choice == 1:
        scan_single_port(host)
    elif choice == 2:
        start_port = int(input("Enter start port number: "))
        end_port = int(input("Enter end port number: "))
        scan_multi_ports(host, start_port, end_port)
        
