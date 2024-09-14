Table of Contents:
-------------------
1. Introduction
2. Usage Instruction
3. Setting up the environment
4. Execution


1. Introduction:
-----------------
This code is designed to demonstrate functioning of client, multithreaded server, multithreaded web proxy, and the extended multithreaded web proxy.

2. Usage Instructions:
-----------------------
Make sure to install all requried librares.

sudo apt-get install python3-bs4
pip install translate
sudo apt-get install python3-matplotlib
sudo apt-get install python3-urllib3

Note: The installation of library depends on the environment where python is installed and its command can vary.

- File on the server should be in the same directory where server.py is kept.

3. Setting up the environment:
-----------------------------
- check ip address of container using 
  ifconfig (Ubuntu)
  ipconfig (Command Prompt)
- ip= '172.31.0.4'
  port = 8080 

4. Execution
------------
Client:

- python Client.py <server_ip or name> <server_port> <path>
- python Client.py <proxy_ip> <proxy_port> <server_ip> <server_port> <path>

Web proxy:

-python3 Proxy.py

Server:

- python3 Server.py <ip_address> <port>
- python3 Server.py 172.31.0.4 8080

ExtendedProxy:

-python3 ExtendedProxy.py
