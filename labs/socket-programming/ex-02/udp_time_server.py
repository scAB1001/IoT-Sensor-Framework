import socket
from datetime import datetime

HOST = '127.0.0.1'  # Localhost
PORT = 65433        # Different port for UDP

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print(f"UDP Server listening on {HOST}:{PORT}...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        request = data.decode()
        print(f"Received '{request}' from {addr}")

        if request == "TIME":
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            server_socket.sendto(current_time.encode(), addr)
        else:
            server_socket.sendto(b"Invalid request", addr)