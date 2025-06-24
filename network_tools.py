import socket
import threading

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((ip, port))
            print(f"Port ouvert : {port}")
    except:
        pass

def scan_ports(ip, port_range):
    for port in port_range:
        threading.Thread(target=scan_port, args=(ip, port)).start()