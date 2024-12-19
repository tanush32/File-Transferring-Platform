import socket
import os

# Define server host and port
HOST = '192.168.248.86'  # Ensure this is the local IP of PC 1
PORT = 8000

def send_video(file_path, conn):
    try:
        with open(file_path, 'rb') as video_file:
            chunk = video_file.read(1024)  # Send 1024 bytes at a time
            while chunk:
                conn.send(chunk)
                chunk = video_file.read(1024)
        # Indicate end of file transfer
        conn.send(b"EOF")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        conn.send(b"ERROR: File not found")
    except Exception as e:
        print(f"Error: {e}")
        conn.send(b"ERROR: An unexpected error occurred")
    finally:
        print("Finished sending video.")
        conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr} established")  # Connected message on server side
        
        # Receive request from client
        file_request = conn.recv(1024).decode()
        print(f"Client requested: {file_request}")

        # Specify the absolute path of the video file requested by the client
        base_directory = r"D:\desktop files\Mine Dont Touch\Videos\NEW viDEo"
        video_file_path = os.path.join(base_directory, file_request)

        # Send video to client
        send_video(video_file_path, conn)

if __name__ == "_main_":
    start_server()