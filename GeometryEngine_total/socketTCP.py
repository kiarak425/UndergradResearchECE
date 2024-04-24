import socket
import geoServer

# Define the host and port for the server
HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Create a TCP/IP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to the address and port
    s.bind((HOST, PORT))
    # Continuously listen for incoming connections
    while True:
        # Listen for incoming connections
        s.listen()
        print("Waiting for a connection...")
        # Accept connections
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # Decode the received data
                received_data = data.decode('utf-8').strip()
                # Split the received data into individual values
                request_params = received_data.split(',')
                
                if len(request_params) < 2:
                    conn.send("Error: Invalid request format.".encode('utf-8'))
                    continue
                
                request_type = request_params[0]
                request_data = request_params[1:]

                # Handle different request types
                if request_type == 'azimuth':
                    norad_id, lat, long, utc_datetime = request_data
                    output = geoServer.get_azimuth_elevation(norad_id, float(lat), float(long), utc_datetime)
                elif request_type == 'tle':
                    norad_id = request_data[0]
                    output = geoServer.get_tle(norad_id)
                elif request_type == 'name':
                    norad_id = request_data[0]
                    output = geoServer.get_name(norad_id)
                elif request_type == 'next_pass':
                    norad_id, utc_date, utc_time, lat, long = request_data
                    output = geoServer.get_next_pass(norad_id, utc_date, utc_time, lat, long)
                else:
                    output = "Error: Invalid request type."

                conn.send(output.encode('utf-8'))
