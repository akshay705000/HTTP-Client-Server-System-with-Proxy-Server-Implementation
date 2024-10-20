#Importing required Library
import sys
from socket import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_ip_or_host(hostname_or_ip):
    try:
        # Try to resolve the input as a hostname
        ip_address = gethostbyname(hostname_or_ip)
        return ip_address
    except gaierror:
        # If it's not a valid hostname, assume it's already an IP address
        return hostname_or_ip

def new_connect(proxy_port, proxy_ip, host_port, host_ip):
    try:
        if proxy_ip is not None:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((proxy_ip, proxy_port))
        else:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((host_ip, host_port))
        return sock
    except Exception as e:
        print("Error while creating a socket:", str(e))
        sys.exit(1)

def send_request(sock, path, host_ip, host_port):
    try:
        request = f"GET {path} HTTP/1.1\r\nHost: {host_ip}:{host_port}\r\n\r\n"
        sock.sendall(request.encode())
        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        return response
    except Exception as e:
        print("Error while sending a request:", str(e))
        sys.exit(1)

def parse_html_and_fetch_resources(html, base_url):
    # Create a BeautifulSoup object to parse the HTML.
    soup = BeautifulSoup(html, "html.parser")

    # Find all types of objects required to completely load the web page.
    objects = []

    # Find all images.
    for img in soup.find_all("img"):
        src = img.get("src")
        resource_url = urljoin(base_url, src)
        objects.append(resource_url)

    # Find all CSS files.
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href")
        resource_url = urljoin(base_url, href)
        objects.append(resource_url)

    # Find all JavaScript files.
    for script in soup.find_all("script", src=True):
        src = script.get("src")
        resource_url = urljoin(base_url, src)
        objects.append(resource_url)

    return objects

def close_socket(sock):
    try:
        sock.close()
    except Exception as e:
        print("Error while closing the socket:", str(e))

def main():
    if len(sys.argv) < 4 or len(sys.argv) > 6 or len(sys.argv) == 5:
        print("Usage: python client.py <proxy_ip> <proxy_port> <server_ip or name> <server_port> <path>")
        return

    if len(sys.argv) == 4:
        # No proxy arguments provided, connect directly to the server
        host_ip = get_ip_or_host(sys.argv[1])
        host_port = int(sys.argv[2])
        path = sys.argv[3]
        proxy_ip = None
        proxy_port = None
    elif len(sys.argv) == 6:
        # Proxy arguments provided, connect through the proxy
        proxy_ip = sys.argv[1]
        proxy_port = int(sys.argv[2])
        host_ip = get_ip_or_host(sys.argv[3])
        host_port = int(sys.argv[4])
        path = sys.argv[5]

    try:
        sock = new_connect(proxy_port, proxy_ip, host_port, host_ip)
        response = send_request(sock, path, host_ip, host_port)

        if response.decode().startswith("HTTP/1.1 200 OK"):
            print(response.decode())
            references = parse_html_and_fetch_resources(response, path)
            print(references)
            for reference in references:
                sock1 = new_connect(proxy_port, proxy_ip, host_port, host_ip)
                response1 = send_request(sock1, reference, host_ip, host_port)
                print(response1)
                close_socket(sock1)
        else:
            raise Exception("Failed to fetch object")
    except Exception as e:
        print("Error:", str(e))
    finally:
        close_socket(sock)

if __name__ == "__main__":
    main()
