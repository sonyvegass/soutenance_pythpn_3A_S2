import socket
import threading

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((ip, port))
            print(f"✅ Port OUVERT : {port}")
    except:
        print(f"❌ Port FERMÉ : {port}")


def scan_ports(ip, port_range):
    threads = []
    for port in port_range:
        t = threading.Thread(target=scan_port, args=(ip, port))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()  # Attendre que chaque thread finisse
