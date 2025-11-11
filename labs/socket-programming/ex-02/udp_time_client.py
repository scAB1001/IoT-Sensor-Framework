import socket

HOST = '127.0.0.1'  # Server IP
PORT = 65433        # UDP port

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.sendto(b"TIME", (HOST, PORT))
    data, _ = client_socket.recvfrom(1024)

print("Current time from UDP server:", data.decode())