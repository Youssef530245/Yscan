import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import threading
import os
import pyfiglet

print()
def display_center(text):
    # Get terminal width
    terminal_width = os.get_terminal_size().columns
    
    # Calculate left padding to center the text
    left_padding = (terminal_width - len(text)) // 3
    
    # Display text with padding
    print(" " * left_padding + text)

def main():
    text = "  >> Y-SCAN << "
    banner = pyfiglet.figlet_format(text)
    display_center(banner)
    display_center("------------------------------------")
    display_center("---- Made by: Eng Youssef Mohamed ---")
    display_center("------------------------------------")
    display_center("------------------------------------")
    display_center("----   github.com/Youssef530245 ----")
    display_center("------------------------------------")
    print() 
    print()
    print()

if __name__ == "__main__":
    main()
##-----------------------------------------------------------

# Function to check a single port
def check_port(ip, port, result_callback):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = identify_service(port)
            version = get_service_version(ip, port)  # Get service version
            result_callback(port, True, service, version)
        else:
            result_callback(port, False, None, None)
    except Exception as e:
        result_callback(port, False, str(e), None)
    finally:
        sock.close()

# Function to identify service based on port number
def identify_service(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown Service"

# Function to get the service version by banner grabbing
def get_service_version(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((ip, port))
        sock.sendall(b'HEAD / HTTP/1.1\r\nHost: ' + ip.encode() + b'\r\n\r\n')
        response = sock.recv(1024).decode('utf-8', errors='ignore')
        sock.close()
        return response.split('\r\n')[0]  # Simple example, may need more parsing
    except Exception:
        return "Unknown Version"

# Function to scan ports within a range
def scan_ports(ip, start_port, end_port, max_threads=100):
    results = []
    lock = threading.Lock()
    
    def result_callback(port, is_open, service, version):
        if is_open:
            with lock:
                results.append((port, is_open, service, version))
                print_result(ip, port, is_open, service, version)
    
    with ThreadPoolExecutor(max_threads) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(check_port, ip, port, result_callback)
    
    return results

# Function to print result for a single port
def print_result(ip, port, is_open, service, version):
    if is_open:
        status = "Open"
        print(f" {port}\t{status}\t\t{service}\t{version}")

# Main function to handle user input and initiate scanning
def main():
    ip = input("Enter the target IP address: ")
    start_port = int(input("Enter the start port: "))
    end_port = int(input("Enter the end port: "))
    max_threads = int(input("Enter the number of threads: "))

    print(f"Starting scan on {ip} from port {start_port} to {end_port} with {max_threads} threads")
    print(" Port\tStatus\t\tService\t\tVersion")
    print(" ----\t------\t\t-------\t\t-------")

    start_time = datetime.now()

    scan_ports(ip, start_port, end_port, max_threads)

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Scan completed in {duration}")

if __name__ == "__main__":
    main()
