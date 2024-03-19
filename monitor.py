#monitor.py

import os
import socket
import sys

def check_permissions():
    if os.name != 'posix':
        return True  # Skip permission check on non-Unix systems

    if os.geteuid() != 0:
        print("Error: This script requires root privileges to capture network packets.")
        print("Please run the script with elevated permissions (e.g., using sudo).")
        print("Note: If this is a public network you may not be able to run this.")
        return False

    return True

def start_monitoring(interface):
    try:
        print("Monitoring network traffic. Press Ctrl+C to exit.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        sock.bind((interface, 0))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        while True:
            packet = sock.recvfrom(65565)[0]
            # Process the packet here
    except KeyboardInterrupt:
        print("\nNetwork traffic monitoring stopped.")
    except PermissionError:
        print("Error: Permission denied. Please run the script with elevated privileges.")
    except OSError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if not check_permissions():
        sys.exit(1)

    interface = input("Enter the network interface to monitor (e.g., eth0): ")
    start_monitoring(interface)
