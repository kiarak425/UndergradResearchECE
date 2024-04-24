INSTRUCTION_MANUAL = """\
    Mosaic is a command-line tool designed for various satellite tracking operations. It provides the ability to perform tasks such as checking server status, locating satellites, retrieving TLEs (Two-Line Element) data, obtaining long names of satellites, and predicting the next pass of a satellite. This code is paired with a Geometry Engine and a Back-End Database.

    
    Required Arguments:

        task: The task to be performed.
            - See if the server is alive
            - Find satellite
            - Get TLE
            - Get long name
            - Next pass
            
        command: The specific command for the task.
            - mosaic
            
        subcommand: Additional command details
            - ping
            - satloc
            - tle
            - longname
            
        -s <SERVER>: Specify the server.
        -n <NORAD-ID>: Specify the NORAD ID of the satellite.
        -t <UTC>: Specify the Coordinated Universal Time (UTC).
            - MM-DD-YYY HH:MM:SS
        -l <LOC>
            - latitude longitude 
            - ex: 40.446 -79.982
        
    Returns:
        <SERVER-STATUS>: Status of the server.
        AZ [deg]: Azimuth in degrees.
        EL [deg]: Elevation in degrees.
        <TLE>: Two-Line Element (TLE) data.
        <longname>: Long name of the satellite.
        <UTC>: Coordinated Universal Time.
        
    CLI Calls:
        mosaic ping       -s <SERVER>                                       : <SERVER-STATUS>
        mosaic satloc     -s <SERVER>    -n <NORAD-ID>	-t <UTC> -l <LOC>   : AZ [deg], EL [deg]
        mosaic tle        -s <SERVER>	  -n <NORAD-ID>                     : <TLE>
        mosaic longname   -s <SERVER>	  -n <NORAD-ID> : longname
        mosaic nextpass   -s <SERVER>    -n <NORAD-ID> -t <UTC> -l <LOC>    : AZ [deg], max EL [deg], <UTC> at max EL

    Please type: 'exit' to exit the program. 
"""



def getLongName(norad_id):
    # Load valid NORAD IDs and longnames from file
    with open('validIDs.txt', 'r') as file:
        for line in file:
            norad, longname = line.strip().split(' ', 1)
            if norad == norad_id:
                return longname

    return "Longname not found"

# Function to validate NORAD ID
def validNoradID(norad_id):
    # Load valid NORAD IDs from file
    with open('validIDs.txt', 'r') as file:
        valid_ids = [line.split()[0] for line in file]
    return norad_id in valid_ids


# Function to validate UTC time format (MM-DD-YYYY HH:MM:SS)
def validUTC(utcDate, utcTime):
    try:
        # Validate date format (MM-DD-YYYY)
        month, day, year = map(int, utcDate.split('/'))
        if month < 1 or month > 12 or day < 1 or day > 31 or len(str(year)) != 4:
            return False
        # Validate time format (HH:MM:SS)
        hours, minutes, seconds = map(int, utcTime.split(':'))
        if hours < 0 or hours > 23 or minutes < 0 or minutes > 59 or seconds < 0 or seconds > 59:
            return False
        return True
    except ValueError:
        return False

# Function to validate location coordinates (decimal latitude, decimal longitude)
def validLocation(lat, long):
    try:
        # Convert latitude and longitude to float values
        lat = float(lat)
        long = float(long)
        # Validate latitude range (-90 to 90 degrees) and longitude range (-180 to 180 degrees)
        if -90 <= lat <= 90 and -180 <= long <= 180:
            return True
        else:
            return False
    except ValueError:
        return False
    


def getLongName(norad_id):
    # Load valid NORAD IDs and longnames from file
    with open('validIDs.txt', 'r') as file:
        for line in file:
            norad, longname = line.strip().split(' ', 1)
            if norad == norad_id:
                return longname

    return "Longname not found"
