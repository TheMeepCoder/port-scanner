# Network Scanner

## Group Members

- [Linea]
- [Linus]
- [MattiasLavsund]
- [Magnus]

## Description

[This portscanner allows you to scan a destination host and a range of ports. Checks what port are open and what service are connected to it. Results are log in a .txt file]

## Installation

Python 3.6+
PowerShell
Visual Studio Code


## Usage

In VS code terminal write python3 network_scanner.py

## Features

- [x] Single port check
- [x] Multi-port scanning
- [x] Service identification
- [] [Additional features you implemented]

## Testing

[We tested the portscanner on localhost and scanme.nmap.org, for single and multiple ports, result showed open/closed ports and service. Created a logfile with timestamp.]

## Known Limitations

[Unable to scan multiple IPs at the same time, Unable to read if a port are closed or filtered, Unable to scan multiple specific ports ex. port 22,80,443 only]

## What We Learned

[Dont scan ports that you dont have premission to. We have discovered how to use the socket library]