import GeometryEngine

#Function which takes in the server input and returns the Azimuth and Elevation
def get_azimuth_elevation(norad_id, lat, long, utc_datetime):

    azimuth = GeometryEngine.azimuth(norad_id, lat, long, utc_datetime)
    return azimuth

#Function which takes the norad id and returns the TLE
def get_tle(norad_id):
    tleInformation = GeometryEngine.satelliteFinderID(norad_id)
    return f"Line 1: {tleInformation[2]}, Line 2: {tleInformation[3]}"

#Function which takes the norad id and returns the satellite name
def get_name(norad_id):
    tleInformation = GeometryEngine.satelliteFinderID(norad_id)
    return f"Satellite Name: {tleInformation[0]}"

#Next pass of satellite
def get_next_pass(norad_id, utc_date, utc_time, lat, long):
    next_pass_info = GeometryEngine.nextPass(norad_id, utc_date, utc_time, lat, long)
    return f"Next Pass: {next_pass_info}"



import socket

# Server configuration
HOST = '127.0.0.1'  # Server IP address
PORT = 3315  # Port to listen on
TLE_FILE = 'tle_data.txt'  # File containing TLE data

# Function to handle client requests
def handle_client(client_socket):
    # Receive NORAD ID from client
    norad_id = client_socket.recv(1024).decode('utf-8').strip()
    
    # Search for NORAD ID in TLE file
    with open(TLE_FILE, 'r') as file:
        tle = get_tle(norad_id)
        client_socket.send(tle.encode('utf-8'))
           
# Main function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)  # Listen for only one connection at a time
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        # Accept incoming connections
        client_socket, address = server.accept()
        print(f"[NEW CONNECTION] Connected to {address[0]}:{address[1]}")
        
        # Handle client request in a separate thread
        handle_client(client_socket)
        client_socket.close()

if __name__ == "__main__":
    start_server()