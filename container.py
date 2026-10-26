import socket
import sys
import threading

BANNER = r"""
  _  _ ___ _____ ___    _  _____   
 | \| | __|_   _/ __|  /_\|_   _|  
 | .` | _|  | || (__  / _ \ | |    
 |_|\_|\___||_| \___/_/   \_|_|    
                                   
 +---------------------------------------------------------+
 |  [!] NOTICE FOR RECOVERED LOGS                          |
 |  IF YOU MADE IT THIS FAR, CHECK @Project_Lucy24        |
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


def main():
  print(BANNER)
  print("=== Interactive Netcat Client ===")

  # Prompt for host address
  try:
    host = input("Enter NC Host/IP address: ").strip()
    if not host:
      print("[!] Host cannot be empty.")
      sys.exit(1)

    # Prompt for port
    port_input = input("Enter NC Port: ").strip()
    port = int(port_input)
  except KeyboardInterrupt:
    print("\n[!] Exiting...")
    sys.exit(0)
  except ValueError:
    print("[!] Invalid port number. Please enter a valid integer.")
    sys.exit(1)

  print(f"\n[*] Connecting to {host}:{port}...")

  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("[+] Connected! Start typing your input below:\n" + "-" * 40)
  except Exception as e:
    print(f"[!] Connection failed: {e}")
    sys.exit(1)

  # Start background receiving thread
  recv_thread = threading.Thread(target=receive_data, args=(sock,), daemon=True)
  recv_thread.start()

  # Main thread handles user input sending
  send_data(sock)
  sock.close()


if __name__ == "__main__":
  main()
