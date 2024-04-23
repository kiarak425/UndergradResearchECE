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
# Define host and port
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Bind the socket to the address and port
    s.bind((HOST, PORT))
    # Listen for incoming connections
    s.listen()

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        # Accept incoming connection
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                # Receive data from the client
                data = conn.recv(1024)
                if not data:
                    break  # If no data received, break the loop

                # Decode the received data
                request = data.decode()

                # Parse the request and call the appropriate function
                parts = request.split(',')
                command = parts[0]

                if command == "azimuth_elevation":
                    norad_id = int(parts[1])
                    lat = float(parts[2])
                    long = float(parts[3])
                    utc_datetime = parts[4]
                    result = GeometryEngine.get_azimuth_elevation(norad_id, lat, long, utc_datetime)
                elif command == "tle":
                    norad_id = int(parts[1])
                    result = GeometryEngine.get_tle(norad_id)
                elif command == "name":
                    norad_id = int(parts[1])
                    result = GeometryEngine.get_name(norad_id)
                elif command == "next_pass":
                    norad_id = int(parts[1])
                    utc_date = parts[2]
                    utc_time = parts[3]
                    lat = float(parts[4])
                    long = float(parts[5])
                    result = GeometryEngine.get_next_pass(norad_id, utc_date, utc_time, lat, long)
                else:
                    result = "Invalid command"

                # Send the result back to the client
                conn.sendall(result.encode())