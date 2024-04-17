import socket
import threading

# Server configuration
HOST = '192.168.0.102' # accessible address of r720
PORT = 3310  # Port to connect to

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Function to send messages to the server
def send_message():
    while True:
        try:
            print()
            message = input("")
            client.send(message.encode('utf-8'))
            if message.lower() == 'exit':
                client.close()
                break
        except Exception as e:
            print("An error occurred:", str(e))
            break

# Function to receive messages from the server
def receive_message():
    while True:
        try:
            data = client.recv(1024).decode('utf-8')
            if not data:
                print("Disconnected from server.")
                break
            print(data)
            print ()
            if data.lower() == 'exit':
                client.close()
                break
        except Exception as e:
            print("An error occurred:", str(e))
            break

# Create two threads for sending and receiving messages
send_thread = threading.Thread(target=send_message)
receive_thread = threading.Thread(target=receive_message)

# Start the threads
send_thread.start()
receive_thread.start()

# Join the threads
send_thread.join()
receive_thread.join()

# Close the client socket
client.close()