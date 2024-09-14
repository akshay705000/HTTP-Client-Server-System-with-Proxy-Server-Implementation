import sys
from socket import *
import threading
import json
import time
from datetime import datetime
import matplotlib.pyplot as plt

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

    print(f"Connecting to {target_host_name}:{target_port}")

    target_host = get_ip_or_host(target_host_name)
    return target_host, target_port, target_host_name

def handle_request(client_socket, user_data):
    try:
        # Receive the request from the client
        request = client_socket.recv(1024)

        target_host, target_port, target_host_name = find_host_port(request)
        # Create a socket to connect to the target host
        target_socket = socket(AF_INET, SOCK_STREAM)
        target_socket.connect((target_host, target_port))

        # Forward the request to the target host
        target_socket.sendall(request)
        exclude_urls = ['detectportal.firefox.com']
        user_ip = client_socket.getpeername()[0]  # Get user's IP address
        # Get the current date and time
        current_datetime = datetime.now().isoformat()
        if target_host_name not in exclude_urls:
            if user_ip in user_data:
                user_data[user_ip].append({"url": target_host_name, "datetime": current_datetime})
            else:
                user_data[user_ip] = [{"url": target_host_name, "datetime": current_datetime}]

        while True:
            response = target_socket.recv(1024)
            if not response:
                break
            client_socket.sendall(response)

    except Exception as e:
        print(f"Error in handling request: {e}")
    finally:
        # Close the client and target sockets in a finally block
        if target_socket:
            target_socket.close()
        client_socket.close()

def proxy_server():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((PROXY_HOST, PROXY_PORT))
    server_socket.listen(15)
    print(f"[*] Listening on {PROXY_HOST}:{PROXY_PORT}")

    user_data = load_user_data()  # Load user data from file

    try:
        while True:
            client_socket, client_address = server_socket.accept()

            # Create a new thread to handle the request
            thread = threading.Thread(target=handle_request, args=(client_socket, user_data))
            thread.start()
    except KeyboardInterrupt:
        print("Proxy server stopped.")
    except Exception as e:
        print(f"Proxy server error: {e}")
    finally:
        # Save user data to a file before closing the server socket
        save_user_data(user_data)
        server_socket.close()
        generate_pie_chart(user_data)


def generate_pie_chart(user_data):
    website_hits = {}
    for user_ip, visits in user_data.items():
        for visit in visits:
            url = visit["url"]
            if url in website_hits:
                website_hits[url] += 1
            else:
                website_hits[url] = 1

    labels = list(website_hits.keys())
    values = list(website_hits.values())

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Website Hits")
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the pie chart to a file or display it
    #plt.savefig('website_hits_pie_chart.png')
    plt.show()  # Uncomment this line if you want to display the chart
    plt.close()

def save_user_data(user_data):
    # Save user data to a file
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)

def load_user_data():
    user_data = {}
    try:
        with open("user_data.json", "r") as file:
            user_data = json.load(file)
        return user_data
    except FileNotFoundError:
        return {}

if __name__ == "__main__":
    proxy_server()

