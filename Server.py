
from socket import *
import threading
import sys

class Client:
  #Intializes ip and port address
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port
    #self.id = ip +","+ {port}
  
  #Print Client object
  def __str__(self):
    return f"\nConnected to client ({self.ip},{self.port}\n)"
  
  #Stores the message received by server 
  messageReceived=''
   
  #For receiving message through port 
  def receiveMsg(self):
    return  self.port.recv(4096).decode()
    
  
  def clientHandler(self):
     #prints info about connected client
     print(self)
     self.messageReceived=self.receiveMsg()
     print(self.messageReceived)
     
     if len(self.messageReceived)<=0 :
        self.port.close()
        return
     
     #If message is received than retrieve File path from message
     #And send the reply of requested file data if exist 
     #And if file doesn't exist than give Error 404
     msg = self.messageReceived.split("\r\n")
     length=len(msg[0])
     filepath = msg[0][4:length-9]
     
     #Try to open requested file 
     try:
        with open(filepath, "rb") as f:
           data = f.read()
           reply = b"HTTP/1.1 200 OK\r\n"
           reply += b"Content-Type: text/html\r\n"
           reply += b"\r\n"
           reply +=data
     except FileNotFoundError:
        reply = b"HTTP/1.1 404 Not Found\r\n"
        reply += b"Content-Type: text/html\r\n"
        reply += b"\r\n"
        reply += b"<h1>404 File Not Found</h1>"
     finally:
        self.port.send(reply)
        self.port.close()

     
#Creates Client object for each connection
def handleClient1(connectionSocket, address):
    client= Client(address, connectionSocket)
    client.clientHandler()

#get ip and port arg passed
def get_ip_and_port():
  if len(sys.argv) != 3:
    raise ValueError("Usage: server.py <ip> <port>")

  ip = sys.argv[1]
  port = int(sys.argv[2])

  return ip, port

def main():
   
   serverSocket = socket(AF_INET, SOCK_STREAM)
   ip, port = get_ip_and_port()
    # Bind the socket to a port
   serverSocket.bind((ip, port))

   #Server starts listening
   serverSocket.listen()
   print(f"Server has started listening to ({ip},{port})")
   
   while True:
    # Accept a connection from a client
    port, ip = serverSocket.accept()

    # Create a new thread to handle the client connection
    thread = threading.Thread(target=handleClient1, args=(port, ip))
    thread.start()



if __name__ == "__main__":
    main()
