#network.enumeration.py

import subprocess
import ipaddress
import platform
import os


def arp_scan():
    try:
        if platform.system().lower() == "windows":
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            devices = []
            for line in lines:
                if "dynamic" in line.lower():
                    parts = line.split()
                    ip_address = parts[0]
                    mac_address = parts[1]
                    devices.append((ip_address, mac_address))
            return devices
        elif platform.system().lower() == "linux":
            result = subprocess.run(["arp", "-n"], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            devices = []
            for line in lines:
                parts = line.split()
                if len(parts) == 3 and parts[2] != "(incomplete)":
                    ip_address = parts[0]
                    mac_address = parts[2]
                    devices.append((ip_address, mac_address))
            return devices
        else:
            print("Unsupported operating system for ARP scan.")
            return []
    except Exception as e:
        print(f"Error performing ARP scan: {e}")
        return []


def icmp_ping_sweep(subnet):
    try:
        if platform.system().lower() == "windows":
            result = subprocess.run(["ping", "-n", "1", str(subnet)], capture_output=True, text=True)
        elif platform.system().lower() == "linux":
            result = subprocess.run(["ping", "-c", "1", str(subnet)], capture_output=True, text=True)
        else:
            print("Unsupported operating system for ICMP ping sweep.")
            return []

        if "TTL=" in result.stdout:
            return str(subnet)
        else:
            return None
    except Exception as e:
        print(f"Error performing ICMP ping sweep: {e}")
        return []


if __name__ == "__main__":
    subnet = input("Enter the subnet to scan (e.g., 192.168.1.0/24): ")

    # Perform ARP scan
    print("\nPerforming ARP scan...")
    devices = arp_scan()
    if devices:
        print("Devices discovered via ARP scan:")
        for device in devices:
            print(f"IP Address: {device[0]}, MAC Address: {device[1]}")
    else:
        print("No devices discovered via ARP scan.")

    # Perform ICMP ping sweep
    print("\nPerforming ICMP ping sweep...")
    network = ipaddress.ip_network(subnet)
    live_hosts = []
    for ip in network.hosts():
        result = icmp_ping_sweep(ip)
        if result:
            live_hosts.append(result)
    if live_hosts:
        print("Live hosts discovered via ICMP ping sweep:")
        for host in live_hosts:
            print(host)
    else:
        print("No live hosts discovered via ICMP ping sweep.")
