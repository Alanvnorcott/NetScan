#validate_cve_data.py
import json
from ports import choose_ip
import socket
import threading
import time

def load_cve_database(file_path):
    try:
        with open(file_path, 'r') as file:
            cve_data = json.load(file)
        return cve_data
    except Exception as e:
        print(f"Error loading CVE database: {e}")
        return None

def lookup_cve(service_name, version, cve_data):
    vulnerabilities = []
    for cve_entry in cve_data:
        if 'vulnerable_products' in cve_entry:
            for product in cve_entry['vulnerable_products']:
                if service_name.lower() in product.lower() and version in cve_entry.get('version', ''):
                    vulnerabilities.append({
                        'cve_id': cve_entry['cve_id'],
                        'description': cve_entry['description'],
                        'references': cve_entry.get('references', [])
                    })
    return vulnerabilities

IMPORTANT_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 123, 143, 443, 445, 465, 514, 993, 995, 1080, 3306, 5432, 5900, 5901, 8080, 8443]

def scan_port(target, port, services):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(7)  # Increase timeout duration to 7 seconds (adjust as needed)
            result = s.connect_ex((target, port))
            if result == 0:
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                services.append((banner.split()[0], banner.split()[1]))
            elif result == 113:  # No route to host
                print(f"Warning: No route to host on port {port}")
            elif result == 11004:  # Valid IP address but no response from the target
                print(f"Warning: No response from the target on port {port}")
            else:
                print(f"Error scanning port {port}: {result}")
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

def get_services_on_machine(target):
    services = []
    total_ports = len(IMPORTANT_PORTS)
    scanned_ports = 0
    threads = []
    for port in IMPORTANT_PORTS:
        scanned_ports += 1
        print(f"Scanning port {port} ({scanned_ports}/{total_ports})...")
        thread = threading.Thread(target=scan_port, args=(target, port, services))
        threads.append(thread)
        thread.start()
        # Introduce a small delay between thread starts to control the scan speed
        time.sleep(0.1)
    for thread in threads:
        thread.join()
    return services

def perform_vulnerability_scan(target):
    if not target:
        print("No target selected. Exiting.")
        return

    print(f"Selected Machine IP: {target}")

    cve_data = load_cve_database('cve_schema.json')
    if not cve_data:
        print("CVE database not found. Exiting.")
        return

    services_on_machine = get_services_on_machine(target)
    if not services_on_machine:
        print("No services for vulnerabilities found on the target machine.")
        return

    print("Services found on the target machine:")
    for service_name, version in services_on_machine:
        vulnerabilities = lookup_cve(service_name, version, cve_data)
        if vulnerabilities:
            print(f"Vulnerabilities found for service {service_name} version {version}:")
            for vulnerability in vulnerabilities:
                print(f"CVE ID: {vulnerability['cve_id']}")
                print(f"Description: {vulnerability['description']}")
                print(f"References: {', '.join(vulnerability['references'])}")
        else:
            print(f"No vulnerabilities found for service {service_name} version {version}")


if __name__ == '__main__':
    perform_vulnerability_scan()
