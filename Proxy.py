import sys
from socket import *
import threading

# Define proxy configuration
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 8080  # Proxy server port

def get_ip_or_host(hostname_or_ip):
    try:
        # Try to resolve the input as a hostname
        ip_address = gethostbyname(hostname_or_ip)
        return ip_address
    except gaierror:
        # If it's not a valid hostname, assume it's already an IP address
        return hostname_or_ip

def find_host_port(request):
    request_str = request.decode()
    components = request_str.split("\r\n")
    # Get the host and port.
    host = components[1].split(" ")[1]
    host_ip_and_port = host.split(':')
    target_host_name = ""
    target_port = 80
    if len(host_ip_and_port) == 1:
        target_port = 80
        target_host_name = host_ip_and_port[0]
    if len(host_ip_and_port) == 2:
        target_port = int(host_ip_and_port[1])
        target_host_name = host_ip_and_port[0]
    print(target_host_name)

    print(f"Connecting to {target_host_name}:{target_port}")

    target_host = get_ip_or_host(target_host_name)
    return target_host, target_port

def handle_request(client_socket):

    try:
        # Receive the request from the client
        request = client_socket.recv(1024)

        target_host, target_port = find_host_port(request)
        # Create a socket to connect to the target host
        target_socket = socket(AF_INET, SOCK_STREAM)
        target_socket.connect((target_host, target_port))

        # Forward the request to the target host
        target_socket.sendall(request)

        while True:
            response = target_socket.recv(1024)
            if not response:
                break
            client_socket.sendall(response)
            print(response)

    except Exception as e:
        print(f"Error in handling request: {e}")
    finally:
        # Close the client and target sockets in a finally block
        client_socket.close()
        target_socket.close()

def proxy_server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((PROXY_HOST, PROXY_PORT))
    server_socket.listen(15)
    print(f"[*] Listening on {PROXY_HOST}:{PROXY_PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            # Create a new thread to handle the request
            thread = threading.Thread(target=handle_request, args=(client_socket,))
            thread.start()

    except KeyboardInterrupt:
        print("Proxy server stopped.")
    except Exception as e:
        print(f"Proxy server error: {e}")
    finally:
        # Close the server socket in a finally block
        server_socket.close()

if __name__ == "__main__":
    proxy_server()
