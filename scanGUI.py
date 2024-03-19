# scanGUI.py

# import tkinter as tk
# from tkinter import filedialog
# from ports import choose_ip, scan
# from banner_grabber import grab_banner
# from network_enumeration import arp_scan, icmp_ping_sweep
# from analyze_network_traffic import network_traffic_analysis
# from monitor import start_monitoring
# from validate_cve_data import perform_vulnerability_scan
# import socket
# import subprocess

# def get_machine_ip():
#     # Get the machine's IP address
#     return socket.gethostbyname(socket.gethostname())

# def get_network_ip():
#     try:
#         result = subprocess.run(['ipconfig'], capture_output=True, text=True)
#         lines = result.stdout.split('\n')
#         for line in lines:
#             if "Default Gateway" in line:
#                 network_ip = line.split(':')[-1].strip()
#                 return network_ip
#     except Exception as e:
#         print(f"Error getting network IP: {e}")
#     return None

# def select_file():
#     root = tk.Tk()
#     root.withdraw()
#     file_path = filedialog.askopenfilename(title="Select Network Traffic Data File")
#     return file_path

# def perform_scan(scan_type, target, subnet=None):
#     if scan_type == "arp":
#         devices = arp_scan()
#         return devices
#     elif scan_type == "icmp":
#         live_hosts = icmp_ping_sweep(subnet)
#         return {host: True for host in live_hosts}  # Return dictionary with live hosts
#     elif scan_type == "traffic_analysis":
#         file_path = select_file()
#         results = network_traffic_analysis(file_path)
#         return results
#     elif scan_type == "vulnerability":
#         perform_vulnerability_scan(target)
#         return {}  # Return empty dictionary as there are no specific scan results
#     elif scan_type == "port":
#         ports = [
#             (21, "FTP (File Transfer Protocol)"),
#             (22, "SSH (Secure Shell)"),
#             (25, "SMTP (Simple Mail Transfer Protocol)"),
#             (53, "DNS (Domain Name System)"),
#             (80, "HTTP (Hypertext Transfer Protocol)"),
#             (110, "POP3 (Post Office Protocol version 3)"),
#             (143, "IMAP (Internet Message Access Protocol)"),
#             (443, "HTTPS (HTTP Secure)"),
#             (3389, "RDP (Remote Desktop Protocol)"),
#             (3306, "MySQL Database"),
#             (5432, "PostgreSQL Database"),
#             (1521, "Oracle Database"),
#             (8080, "HTTP Alternate")
#         ]
#         results = {}
#         for port, context in ports:
#             results[port] = scan(target, port)
#         return results

# def create_gui():
#     window = tk.Tk()
#     window.title("Network Scanner")
#     window.geometry("500x300")  # Set the window size to 500x300 pixels

#     label = tk.Label(window, text="Welcome to the Network Scanner")
#     label.pack()

#     # Function to handle button click and display scan results
#     def perform_and_display_scan(scan_type, target):
#         if target:
#             if scan_type == "icmp":
#                 subnet = input("Enter the subnet to scan (e.g., 192.168.1.0/24): ")
#                 results = perform_scan(scan_type, target, subnet=subnet)
#             else:
#                 results = perform_scan(scan_type, target)

#             if results is not None:
#                 display_results(results)

#     # Function to display scan results
#     def display_results(results):
#         result_window = tk.Toplevel(window)
#         result_window.title("Scan Results")

#         for key, value in results.items():
#             result_label = tk.Label(result_window, text=f"Port {key}: {'Open' if value else 'Closed'}")
#             result_label.pack()

#     # Function to handle IP selection
#     def select_ip(choice):
#         target_ip = ""
#         if choice == '1':
#             target_ip = get_network_ip()
#         elif choice == '2':
#             target_ip = get_machine_ip()
#         elif choice == '3':
#             target_ip = input("Input IP number: ")
#         print(f"Selected IP: {target_ip}")
#         return target_ip

#     # Function to handle IP choice buttons
#     def handle_ip_choice(choice):
#         target_ip = select_ip(choice)
#         if target_ip:
#             for scan_type in ["arp", "icmp", "traffic_analysis", "vulnerability", "port"]:
#                 perform_and_display_scan(scan_type, target_ip)

#     # Buttons for selecting IP address
#     network_ip_button = tk.Button(window, text="Select Network IP", command=lambda: handle_ip_choice('1'))
#     network_ip_button.pack()

#     machine_ip_button = tk.Button(window, text="Select Machine IP", command=lambda: handle_ip_choice('2'))
#     machine_ip_button.pack()

#     custom_ip_button = tk.Button(window, text="Input Custom IP", command=lambda: handle_ip_choice('3'))
#     custom_ip_button.pack()

#     window.mainloop()

# if __name__ == "__main__":
#     create_gui()
