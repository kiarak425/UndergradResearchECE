import socket
import threading
import serverSupport
import time
import geoTCP

# Server configuration
HOST = '0.0.0.0'
PORT = 3310                  # Port to listen on
START_TIME = time.time() # for server uptime


# Function to handle client connections
def handle_client(client_socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    client_socket.send(serverSupport.INSTRUCTION_MANUAL.encode('utf-8'))

    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8').strip()
            if not data:
                break

            # Parse client input
            args = data.split()
            
            if args[0] == 'mosaic':
                #if args[1] == 'exit':
                                    
                if args[1] == 'ping':
                    if args[2] == "-s" and len(args) == 4 and (args[3] == f"{HOST}:{PORT}" or args[3] == "hostname"):
                        uptime_seconds = int(time.time() - START_TIME)
                        uptime_hours = uptime_seconds // 3600
                        uptime_minutes = (uptime_seconds % 3600) // 60
                        uptime_seconds %= 60
                        uptime_str = f"{uptime_hours} hours, {uptime_minutes} minutes, {uptime_seconds} seconds"

                        # Output: Server uptime
                        response = f"Server: {HOST}:{PORT} \nServer uptime: {uptime_str}"                        
                    else:
                        response = "Invalid arguments"
                        
                elif args[1] == 'satloc':
                    if args[2] == '-s' and args[4] == '-n':# and args[6] == '-t' and args[9] == '-l':
                        norad_id = args[5]
                        if (arg[7] == "now"):
                            utc_datetime = "now"
                            lat = args[9]
                            long = args[10]
                        else:
                            utc_datetime = args[7] + " " + args[8]
                            lat = args[10]
                            long = args[11]
                        
                            response = str(geoTCP.send_request_to_server(norad_id, lat, long, utc_datetime))
                            print(response)

                    #     if serverSupport.validNoradID(norad_id) and serverSupport.validLocation(lat, long) and serverSupport.validUTC(utcDate, utcTime):
                    #         # Output: AZ [deg] EL [deg]
                    #             #response from a text file
                    #         #response = f"AZ deg, EL deg"
                    #     else:
                    #         response = "Invalid NORAD ID, UTC, or Location"
                    # else:
                    #     response = "Invalid arguments for satloc"
                    
                elif args[1] == 'tle':
                    if len(args) == 6 and args[2] == '-s' and args[4] == '-n':
                        # Output: <TLE>
                            # output the tle from a file according to noradID                        
                        response = "<TLE>"
                        
                elif args[1] == 'longname':
                    if len(args) == 6 and args[2] == '-s' and args[4] == '-n':
                        # Output: <longname>
                        norad_id = args[5]
                        response = serverSupport.getLongName(norad_id)
                    else:
                        response = "Invalid arguments"
                        
                    
                elif args[1] == 'nextpass' and len(args) >= 11:
                    # Output: AZ [deg] max EL [deg] <UTC> at max EL                    
                    if len(args) == 12 and args[2] == '-s' and args[4] == '-n' and args[6] == '-t' and args[9] == '-l':
                        norad_id = args[5]
                        utcDate = args[7]
                        utcTime = args[8]
                        lat = args[10]
                        long = args[11]

                        if serverSupport.validNoradID(norad_id) and serverSupport.validLocation(lat, long) and serverSupport.validUTC(utcDate, utcTime):
                            # Output: AZ [deg] EL [deg] <UTC> at max EL
                                #response from a text file
                            response = f"AZ deg, EL deg, UTC Max EL"
                        else:
                            response = "Invalid NORAD ID, UTC, or Location"
                    else:
                        response = "Invalid arguments for nextpass"
                        
                else:
                    response = "Input error"     
            else:
                response = "Input error"
                
            with open('userInput.txt', 'w') as file:
                for arg in args:
                    file.write(arg + ' ')

            # Send response to the client
            client_socket.send(response.encode('utf-8'))
        except:
            print(f"[DISCONNECTED] Client {address} disconnected.")
            break

    client_socket.close()

# Main function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        # Accept incoming connections
        client_socket, address = server.accept()
        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    start_server()