import socket
import os

# Define server host and port
HOST = '192.168.248.86'  # Update to server IP if running on a different machine
PORT = 8000

def request_video(video_name):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(60)  # Set a timeout of 10 seconds
        client_socket.connect((HOST, PORT))
        
        # Send request for the video file
        client_socket.sendall(video_name.encode())
        print(f"Requested file: {video_name}")

        # Dynamically create a unique save path
        base_save_path = 'received_videos'
        os.makedirs(base_save_path, exist_ok=True)  # Create directory if it doesn't exist
        save_path = os.path.join(base_save_path, video_name)  # Save with the same filename as requested

        # Open the file to write the received data
        with open(save_path, 'wb') as video_file:
            print("Waiting to receive data from server...")
            while True:
                data = client_socket.recv(1024)  # Receive 1024 bytes at a time
                if not data:
                    break
                if b"ERROR:" in data:
                    print(data.decode())  # Display error message if file not found
                    break
                elif data == b"EOF":  # End of file received
                    print(f"File {save_path} transfer complete!")  # Notify the client about completion
                    break
                video_file.write(data)
        
        print(f"Video saved as {save_path}")  # Notify where the file was saved
    except socket.timeout:
        print("Connection timed out. Server might not be responding.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()  # Close the connection after receiving the file

if __name__ == "_main_":
    while True:
        # Ask the user for the next file to request
        video_to_request = input("Enter the file name with extension (or type 'exit' to quit): ")  # Request the video by name
        
        # Exit condition
        if video_to_request.lower() == 'exit':
            print("Exiting the program.")
            break
        
        # Request the video and save it uniquely
        request_video(video_to_request)