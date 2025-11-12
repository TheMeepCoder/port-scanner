#!/usr/bin/env python3
"""
Network Scanner Project
Students: [Linea, Linus, Mattias Lavsund, Magnus]
Date: [20-10-2025]
"""
# To test the program: scanme.nmap.org

# Excample Ports
# 22 - is a port that is open
# 25 - is a port that is closed
# 21 - is a port that cannot be reached/filtered

import ipaddress # import to help validate IP format
import socket # allows the program to create network sockets, connect to host:port, and look up serivce names
import datetime # logs time 
import sys # adds a little flair
import time

def is_port_open(host: str, port: int, timeout: float = 1.0) -> str: # "->" just what is expected, dosen't do anything on it's without an mypy libarey, same with the classes. here it just acts like a simple comment
    #Return True if port is open, else False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # the with statement closes connection after it's done scaning which is after it has printed out the last port in the treminal and txt
        s.settimeout(timeout) # sets a timeout of 1 secound
        try:
            s.connect((host, port)) # adtempts to connect and scan a port
            return "open"
        except socket.timeout:
            return "closed"
        except (ConnectionRefusedError, OSError):
            return "filtered"

def validate_host(prompt: str = "Host to scan (IP or hostname): ") -> str:
    #Prompt until a valid IP address or hostname is provided; return to host.
    while True:
        user_input = input(prompt).strip() # strip removes empty spaces which could mess with scanning
        if not user_input:
            print("Input cannot be empty.")
            continue
        try:
            # Check if it’s a valid IPv4 or IPv6
            ipaddress.ip_address(user_input)
            return user_input  # valid IP
        except ValueError:
            # Not a valid IP — try resolving as hostname
            try:
                socket.gethostbyname(user_input)
                return user_input  # valid hostname
            except socket.gaierror: # if input is a invailed format
                print("Invalid host. Please enter a valid IP address or hostname (e.g. 192.168.1.1 or localhost).") 
        
def get_service_name(port: int) -> str:
    #adtempt to identify sverice of given port
    try:
        return socket.getservbyport(port)
    except OSError: # OSError means when it cannot find any value
        return "unknown"
    
def log_result(port: int, service: str, state: str, host: str):
    #logs result into a txt file
    with open("results.txt", "a") as file:
        light_status = {"open": "🟢", "closed": "🔴", "filtered": "⚫"}.get(state, "❔")  # Open in append mode, which adds new lines for each scanned port
        file.write(f"{light_status}Port {port} is {state}. Service: {service}. Time: {datetime.datetime.now().strftime('%H:%M:%S')}. Hostname/IP: {host}\n")
        file.write("-------\n")
    
def scan_single_port(host: str):
    port = int(input("Enter the port number to be scanned: "))
    state = is_port_open(host, port)
    service = get_service_name(port)
    light_status = {"open": "🟢", "closed": "🔴", "filtered": "⚫"}.get(state, "❔")
    log_result(port, service, state, host)  # calls funtion to Log the result and sends the value of the varibles

    print(f"{light_status} Port {port} is {state}. Service: {service}.")
    print("-------")
    
    print("results have been saved in results.txt")
    print("-------")

def scan_multi_ports(host: str, start_port: int, end_port: int):
    #Scan a range of ports between start_port and end_port
    for port in range(start_port, end_port + 1): # 
        state = is_port_open(host, port)
        service = get_service_name(port)
        light_status = {"open": "🟢", "closed": "🔴", "filtered": "⚫"}.get(state, "❔")
        log_result(port, service, state, host)  # calls funtion to Log the result and sends the value of the varibles

        print(f"{light_status} Port {port} is {state}. Service: {service}.")
        print("-------")
    
    print("Results have been saved in results.txt")
    print("-------")

def normal_scan():
    host = validate_host("Host to scan (ip or hostname): ") # Asks user for IP/Hostname
    print("-------")

    while True:
        try: 
            choice = int(input("Select scanning mode: (1) Single-port (2) Multi-port: "))
            print("-------")
            
            if choice == 1:
                with open("results.txt", "a") as file:
                    file.write(f"Scan done to {host} at {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
                    file.write("-------\n")
                scan_single_port(host)
                break
            elif choice == 2:
                with open("results.txt", "a") as file:
                    file.write(f"Scan done to {host} at {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
                    file.write("-------\n")
                start_port = int(input("Enter start port number: "))
                end_port = int(input("Enter end port number: "))
                scan_multi_ports(host, start_port, end_port)
                break
            else:
                print("Invailed input. Please enter 1 or 2")
                print("-------")
        except ValueError:
            print("Invailed input. Please enter a number")
            print("-------")


def sum_scan():
    host = validate_host("Host to scan (ip or hostname): ")
    start_port = int(input("which port would you like to start on?: "))
    end_port = int(input("which port would you like to end on?: "))
    open_count = 0
    closed_count = 0
    filtered_count = 0
    unknown_count = 0
    spinner = ["|", "/", "-","\\"]

    for i, port in enumerate(range(start_port, end_port + 1), start = 1):
        try:
            state = is_port_open(host, port)
            if state == "open":
                open_count += 1
            elif state == "closed":
                closed_count += 1
            elif state == "filtered":
                filtered_count += 1
            else:
                unknown_count += 1
        except Exception:
            unknown_count += 1

        total_count = open_count + closed_count + filtered_count + unknown_count
        spin_char = spinner[i % len(spinner)]
        sys.stdout.write(f"\r{spin_char} Scanning ... {total_count - 1}/{end_port - start_port}")
        sys.stdout.flush()
        time.sleep(0.05)
                
    print(f"\n Scan Summery: 🟢 Open ports: {open_count} | 🔴 Closed ports: {closed_count} | ⚫ Filtered ports: {filtered_count} | ❔ Unknown errors: {unknown_count}")

    with open("results.txt", "a") as file:
        file.write(f"Scan done on {host} at {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
        file.write(f"Scan Summery: 🟢 Open ports: {open_count} | 🔴 Closed ports: {closed_count} | ⚫ Filtered ports: {filtered_count} | ❔ Unknown errors: {unknown_count}\n ")
        file.write("-------\n")
    print("summery has been logged to results.txt")

def quick_scan():
    print("Disclaimer! this mode will not log to any txt file, only print out in terminal!")
    print("-------")
    host = validate_host("Host to scan (ip or hostname): ") # Asks user for IP/Hostname
    print("-------")

    while True:
        try: 
            choice = int(input("Select scanning mode: (1) Single-port (2) Multi-port: "))
            print("-------")
            if choice == 1:
                port = int(input("Enter the port number to be scanned: "))
                state = is_port_open(host, port)
                light_status = {"open": "🟢", "closed": "🔴", "filtered": "⚫"}.get(state, "❔")
                print(f"{light_status} Port {port} is {state}")
                break
            elif choice == 2:
                start_port = int(input("Enter start port number: "))
                end_port = int(input("Enter end port number: "))

                for port in range(start_port, end_port + 1):
                    state = is_port_open(host, port)
                    state = is_port_open(host, port)
                    light_status = {"open": "🟢", "closed": "🔴", "filtered": "⚫"}.get(state, "❔")
                    print(f"{light_status} Port {port} is {state}")
                break
            else:
                print("Input out of range")
        except ValueError:
            print("invailed input")
    

def test_localhost():
    pass

def menu():
    print("🛑Remeber to ONLY scan on networks you have permission to🛑")
    while True:
        print("-------")
        print("Pick yhe selection between 1 to 3")
        print("1. Normal Scan")
        print("2. Summery Scan")
        print("3. Quick scan")
        print("4. Test Localhost")
        print("-------")
        try:
            selection = int(input(""))
            if selection == 1:
                normal_scan()
                break
            elif selection == 2:
                sum_scan()
                break
            elif selection ==3:
                quick_scan()
                break
            elif selection == 4:
                test_localhost()
                break
            else:
                print("input out of range, pick a number between 1-3")
        except ValueError:
            print("Invailed input, please pick a number between 1-3")

def close_program():
        
    while True:
        try:
            done = input("do you want to go back to selection?(y/n): ")
            if done == "y":
                menu()
            elif done == "n":
                print("-------")
                print("Thank you for using my port scanner")
                break
            else:
                print("invailed input, type either in (y) for yes or (n) for no")
        except ValueError:
            print('invailed input, type either in (y) for yes or (n) for no')

menu()

close_program()

"""
TODO: 
dynamic sys loading bar
localhost test option
qucik scan option
timer

"""
#DONE: filtered service state, summery