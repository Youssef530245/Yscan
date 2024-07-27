import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import threading
import os
import pyfiglet
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Function to display a banner in the terminal
def display_center(text):
    terminal_width = os.get_terminal_size().columns
    left_padding = (terminal_width - len(text)) // 3
    print(" " * left_padding + text)

def main_banner():
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

# Function to check a single port
def check_port(ip, port, result_callback):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            service = identify_service(port)
            version = get_service_version(ip, port)
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
        result_text = f"Port {port}: {status} - {service} - {version}\n"
        result_text_area.insert(tk.END, result_text)
        result_text_area.yview(tk.END)

# Function to start the scan from GUI
def start_scan():
    ip = ip_entry.get()
    start_port = int(start_port_entry.get())
    end_port = int(end_port_entry.get())
    max_threads = int(max_threads_entry.get())

    if not ip or start_port <= 0 or end_port <= 0 or max_threads <= 0:
        messagebox.showerror("Input Error", "Please provide valid inputs.")
        return

    result_text_area.delete(1.0, tk.END)  # Clear previous results

    status_label.config(text="Scanning...")
    start_time = datetime.now()
    scan_ports(ip, start_port, end_port, max_threads)
    end_time = datetime.now()
    duration = end_time - start_time
    status_label.config(text=f"Scan completed in {duration}")

# Create the GUI
root = tk.Tk()
root.title("Y-SCAN Port Scanner")

# Banner display in GUI
banner_frame = tk.Frame(root)
banner_frame.pack(pady=10)

banner_label = tk.Label(banner_frame, text="  >> Y-SCAN << ", font=("Helvetica", 16, "bold"))
banner_label.pack()

# Input fields
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Target IP:").grid(row=0, column=0, padx=5, pady=5)
ip_entry = tk.Entry(input_frame, width=20)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Start Port:").grid(row=1, column=0, padx=5, pady=5)
start_port_entry = tk.Entry(input_frame, width=20)
start_port_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="End Port:").grid(row=2, column=0, padx=5, pady=5)
end_port_entry = tk.Entry(input_frame, width=20)
end_port_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Max Threads:").grid(row=3, column=0, padx=5, pady=5)
max_threads_entry = tk.Entry(input_frame, width=20)
max_threads_entry.grid(row=3, column=1, padx=5, pady=5)

# Start button
start_button = tk.Button(root, text="Start Scan", command=start_scan)
start_button.pack(pady=10)

# Results text area
result_text_area = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
result_text_area.pack(pady=10)

# Status label
status_label = tk.Label(root, text="Ready", font=("Helvetica", 12))
status_label.pack(pady=10)

if __name__ == "__main__":
    main_banner()
    root.mainloop()
