#banner_grabber.py

import socket

def grab_banner(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(20)  # Set a timeout for connection attempts
            sock.connect((target, port))
            # Send a request to trigger the service banner
            sock.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            # Receive the response (service banner)
            banner = sock.recv(1024).decode()
            return banner
    except ConnectionRefusedError:
        return f"Connection refused by {target}:{port} port is closed."
    except socket.timeout:
        return f"Connection to {target}:{port} timed out"
    except Exception as e:
        return f"Error grabbing banner from {target}:{port}: {e}"
