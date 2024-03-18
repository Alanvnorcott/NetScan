# run.py

import tkinter as tk
from tkinter import filedialog
from ports import scan, choose_ip
from banner_grabber import grab_banner
from network_enumeration import arp_scan, icmp_ping_sweep
from analyze_network_traffic import network_traffic_analysis

def select_file():
    # Create the Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Prompt the user to select a file using a file dialog
    file_path = filedialog.askopenfilename(title="Select Network Traffic Data File")
    return file_path

if __name__ == "__main__":
    target = choose_ip()

    if target:
        # Perform network enumeration (optional)
        choice = input("\nDo you want to perform network enumeration? (y/n): ")
        if choice.lower() == 'y':
            print("\nPerforming network enumeration...")
            subnet = input("Enter the subnet to scan (e.g., 192.168.1.0/24): ")

            # ARP scan
            print("\nPerforming ARP scan...")
            devices = arp_scan()
            if devices:
                print("Devices discovered via ARP scan:")
                for device in devices:
                    print(f"IP Address: {device[0]}, MAC Address: {device[1]}")
            else:
                print("No devices discovered via ARP scan.")

            # ICMP ping sweep
            print("\nPerforming ICMP ping sweep...")
            live_hosts = icmp_ping_sweep(subnet)
            if live_hosts:
                print("Live hosts discovered via ICMP ping sweep:")
                for host in live_hosts:
                    print(host)
            else:
                print("No live hosts discovered via ICMP ping sweep.")

        print(
            """WARNING: Before selecting the network traffic analysis option, please ensure you have a packet capture file (e.g., .pcap, .cap) available. This file should be generated by tools like Wireshark or tcpdump, containing recorded network traffic data.""")
        choice = input("Do you want to perform network traffic analysis? (y/n): ")
        if choice.lower() == 'y':
            file_path = select_file()
            network_traffic_analysis(file_path)

        # Perform port scanning
        ports = [
            (21, "FTP (File Transfer Protocol)"),
            (22, "SSH (Secure Shell)"),
            (25, "SMTP (Simple Mail Transfer Protocol)"),
            (53, "DNS (Domain Name System)"),
            (80, "HTTP (Hypertext Transfer Protocol)"),
            (110, "POP3 (Post Office Protocol version 3)"),
            (143, "IMAP (Internet Message Access Protocol)"),
            (443, "HTTPS (HTTP Secure)"),
            (3389, "RDP (Remote Desktop Protocol)"),
            (3306, "MySQL Database"),
            (5432, "PostgreSQL Database"),
            (1521, "Oracle Database"),
            (8080, "HTTP Alternate")
        ]

        total_points = 0
        for port, context in ports:
            print(f"\nScanning port {port} ({context})")
            if not scan(target, port):
                total_points += 1

        print(f"\nTotal points earned for closed ports: {total_points} / 13. ")

        # Prompt for banner grabbing
        choice = input("\nDo you want to grab banners for open ports? (y/n): ")
        if choice.lower() == 'y':
            for port, _ in ports:
                banner = grab_banner(target, port)
                if banner:
                    print(f"Banner for {target}:{port}:")
                    print(banner)
                else:
                    print(f"Failed to grab banner from {target}:{port}")
        else:
            print("Banner grabbing skipped.")
