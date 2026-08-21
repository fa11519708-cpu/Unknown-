import socket
import threading

LISTEN_PORT = 8080
DEST_HOST = "127.0.0.1"  # سنستبدله لاحقاً بعنوان سيرفر الـ SSH أو الثغرة
DEST_PORT = 22           # منفذ الاتصال (SSH Port)

def handle_client(client_socket):
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((DEST_HOST, DEST_PORT))
        
        # الـ Payload الترحيبي للحقن
        payload = "CONNECT / HTTP/1.1\r\nHost: example.com\r\n\r\n"
        remote_socket.sendall(payload.encode())

        # توجيه حركة البيانات بين الهاتف والسيرفر
        def forward(source, destination):
            while True:
                data = source.recv(4096)
                if not data:
                    break
                destination.sendall(data)

        t1 = threading.Thread(target=forward, args=(client_socket, remote_socket))
        t2 = threading.Thread(target=forward, args=(remote_socket, client_socket))
        t1.start()
        t2.start()
    except Exception as e:
        print(f"Error: {e}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', LISTEN_PORT))
server.listen(5)
print(f"[*] Engine Running on Port {LISTEN_PORT}...")

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_client, args=(client,)).start()

