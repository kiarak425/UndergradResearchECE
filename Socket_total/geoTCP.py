import socket

def send_request(request_type, request_data, host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        # Combine request type and data into a single string
        request_str = ','.join([request_type] + request_data)
        s.sendall(request_str.encode('utf-8'))
        received_data = s.recv(1024).decode('utf-8')
        return received_data

# Example usage
if __name__ == "__main__":
    norad_id = "43478"  # Replace this with the actual NORAD ID
    lat = "40.7128"     # Latitude of the location (e.g., New York City)
    long = "-74.0060"   # Longitude of the location (e.g., New York City)
    utc_datetime = "now"  # Current UTC datetime
    
    result = send_request('azimuth', [norad_id, lat, long, utc_datetime])
    tle = send_request('tle', [norad_id])
    name = send_request('name', [norad_id])
    #nxt = send_request('next_pass', [norad_id, lat, long, utc_datetime])

    print(result + "\n")
    print(tle + "\n")
    print(name + "\n")
    #print(nxt + "\n")