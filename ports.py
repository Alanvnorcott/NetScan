#ports.py
import socket
import subprocess
import ipaddress


def get_network_ip():
    try:
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if "Default Gateway" in line:
                network_ip = line.split(':')[-1].strip()
                return network_ip
    except Exception as e:
        print(f"Error getting network IP: {e}")
    return None


def get_machine_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        machine_ip = s.getsockname()[0]
        s.close()
        return machine_ip
    except Exception as e:
        print(f"Error getting machine IP: {e}")
    return None


def choose_ip():
    print("\nChoose IP address:")
    print("1. Network IP")
    print("2. Machine IP")
    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        network_ip = get_network_ip()
        print(f"Selected Network IP: {network_ip}")
        return network_ip
    elif choice == '2':
        machine_ip = get_machine_ip()
        print(f"Selected Machine IP: {machine_ip}")
        return machine_ip
    else:
        print("Invalid choice. Defaulting to machine IP.")
        machine_ip = get_machine_ip()
        print(f"Selected Machine IP: {machine_ip}")
        return machine_ip


def scan(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
            print(f"Port {port} should be closed.")
            return True
        else:
            print(f"Port {port} is closed")
            return False
        sock.close()
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
        return False






