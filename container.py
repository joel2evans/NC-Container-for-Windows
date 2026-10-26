import os
import subprocess
import socket
import sys
import threading

BANNER = r"""
  _  _ ___ _____ ___    _  _____   
 | \| | __|_   _/ __|  /_\|_   _|  
 | .` | _|  | || (__  / _ \ | |    
 |_|\_|\___||_| \___/_/   \_|_|    
                                   
 +---------------------------------------------------------+
 |  SYSTEM CONSOLE -- SELECT OPERATIONAL MODE               |
 +---------------------------------------------------------+
"""


def receive_data(sock):
    """Continuously listens for data from the server and prints it."""
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("\n[-] Connection closed by server.")
                break
            sys.stdout.write(data.decode("utf-8", errors="ignore"))
            sys.stdout.flush()
        except Exception as e:
            print(f"\n[!] Read error: {e}")
            break


def send_data(sock):
    """Continuously reads interactive user input and sends it to the server."""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            sock.sendall(line.encode("utf-8"))
        except Exception as e:
            print(f"\n[!] Send error: {e}")
            break


def start_nc_session(host, port):
    """Establishes connection to specified host and port."""
    print(f"\n[*] Connecting to {host}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("[+] Connected! Start typing your input below:\n" + "-" * 50)
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        return

    # Start background thread for receiving data
    recv_thread = threading.Thread(target=receive_data, args=(sock,), daemon=True)
    recv_thread.start()

    # Main thread handles sending input
    send_data(sock)
    sock.close()


def menu_enter_nc():
    """Option 1: Prompt user for Host/IP and Port directly."""
    try:
        host = input("Enter NC Host/IP address: ").strip()
        if not host:
            print("[!] Host cannot be empty.")
            return

        port_input = input("Enter NC Port: ").strip()
        port = int(port_input)
        start_nc_session(host, port)
    except ValueError:
        print("[!] Invalid port number.")


def menu_connect_docker():
    """Option 2: Connect via Docker container context/environment."""
    print("\n[*] Initializing Docker Client Environment...")
    target_host = os.getenv("TARGET_HOST", "host.docker.internal")
    target_port = os.getenv("TARGET_PORT", "1337")

    print(f"[*] Detected Docker Target Config: {target_host}:{target_port}")
    try:
        start_nc_session(target_host, int(target_port))
    except ValueError:
        print("[!] Invalid port configuration in Docker environment.")


def main():
    while True:
        print(BANNER)
        print("1. Enter nc address")
        print("2. Connect to docker")
        print("3. Exit\n")

        try:
            choice = input("Select an option (1-3): ").strip()

            if choice == "1":
                menu_enter_nc()
            elif choice == "2":
                menu_connect_docker()
            elif choice == "3":
                print("\n[*] Exiting... Goodbye!")
                sys.exit(0)
            else:
                print("\n[!] Invalid choice. Please enter 1, 2, or 3.")

        except KeyboardInterrupt:
            print("\n\n[*] Exiting system...")
            sys.exit(0)


if __name__ == "__main__":
    main()
