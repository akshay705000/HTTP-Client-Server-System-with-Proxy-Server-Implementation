
# HTTP Client-Server System with Proxy Server

## Project Overview

This project implements a multithreaded HTTP client-server system, enhanced with a proxy server. The proxy server acts as an intermediary, forwarding HTTP requests and responses between the client and the main server, while providing additional features such as English-to-Hindi translation and usage statistics visualization.

### Key Features:
- **Multithreaded HTTP Server**: Handles multiple simultaneous client requests efficiently using threading.
- **Multithreaded Proxy Server**: Intercepts and forwards HTTP requests and responses while logging all interactions.
- **Page Translation**: The proxy server can translate web pages from English to Hindi before delivering them to the client.
- **Usage Statistics**: Collects and stores detailed logs of client requests and server responses, which can be visualized using graphs.
  
## Project Architecture

1. **HTTP Client**: 
   - Sends requests to the server and receives complete web pages (HTML content).
   
2. **HTTP Server**:
   - Processes requests from the client and responds with the requested web page data.
   - Multi-threaded to handle multiple client requests at the same time.

3. **Proxy Server**:
   - Acts as an intermediary between the client and the server.
   - Logs HTTP requests/responses into JSON format.
   - Supports English-to-Hindi page translation using `BeautifulSoup` and a translation API.
   - Provides graphical representation of usage statistics (e.g., number of requests, response times) using `matplotlib`.

## Tech Stack

- **Socket Programming**: Used for TCP-based client-server communication.
- **Python**: The primary programming language used to implement the client, server, and proxy server.
- **TCP**: Ensures reliable communication between the client and server.
- **BeautifulSoup (bs4)**: For parsing and manipulating HTML to facilitate page translation.
- **Matplotlib**: For visualizing the proxy server's usage statistics (e.g., requests per second, data volume).

## Features

### 1. **Multithreaded HTTP Server**
   - The server is designed to handle multiple client requests concurrently.
   - Each client request is handled in a separate thread, improving the efficiency of handling multiple users.

### 2. **Multithreaded Proxy Server**
   - Forwards client requests to the main server and returns the responses.
   - Maintains a log of all transactions (client requests and server responses) in JSON files, which include details such as:
     - Request type (e.g., GET, POST)
     - Requested URL
     - Timestamp
     - Response status code
   - Each interaction is processed in a separate thread to handle simultaneous requests.

### 3. **Page Translation**
   - The proxy server translates web pages from English to Hindi using an API and `BeautifulSoup` for HTML manipulation.
   - This feature allows clients to request translated versions of the pages.

### 4. **Usage Statistics Visualization**
   - All request and response logs are stored in JSON format and can be used to generate usage statistics.
   - `matplotlib` is used to create graphs showing:
     - Total number of requests over time
     - Response times
     - Data volume exchanged between client and server

## Installation and Setup

### Prerequisites:
- Python 3.x
- Required Python libraries:
  - `socket`
  - `threading`
  - `json`
  - `BeautifulSoup4` (`bs4`)
  - `matplotlib`
  - Any additional libraries for translation (e.g., `googletrans`)

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setting up the environment:
   - Check the IP address of your container using the following commands:
     - `ifconfig` (for Ubuntu)
     - `ipconfig` (for Windows Command Prompt)
   - Example:
     ```
     ip = '172.31.0.4'
     port = 8080
     ```

## Execution

### Client
   - Run the client to request pages from the server or through the proxy server.

   **Direct request to server:**
   ```bash
   python Client.py <server_ip> <server_port> <path>
   ```

   **Request via proxy server:**
   ```bash
   python Client.py <proxy_ip> <proxy_port> <server_ip> <server_port> <path>
   ```

### Web Proxy
   - Run the proxy server using the command:
   ```bash
   python3 Proxy.py
   ```

### HTTP Server
   - Run the HTTP server using the following command with the IP address and port:
   ```bash
   python3 Server.py <ip_address> <port>
   ```
   - Example:
   ```bash
   python3 Server.py 172.31.0.4 8080
   ```

### Extended Proxy
   - To run the extended proxy with additional features, use the command:
   ```bash
   python3 ExtendedProxy.py
   ```

## Usage

1. **Starting the server**: The HTTP server listens for incoming client requests and processes them.
2. **Starting the proxy server**: The proxy server will forward the client's request to the HTTP server and return the response.
3. **Requesting translation**: The client can request translated pages via the proxy server, which will return the page translated into Hindi.
4. **Viewing usage statistics**: Use the proxy server logs to generate graphs using `matplotlib`.

## Future Enhancements

- Support for additional languages beyond Hindi.
- Advanced caching in the proxy server to reduce redundant requests.
- Security enhancements such as encryption of client-server communications.
