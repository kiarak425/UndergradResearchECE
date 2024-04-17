# MOSAIC Server - Client Socket
## Overview:
Mosaic is a command-line tool designed for various satellite tracking operations. It provides the ability to perform tasks such as checking server status, locating satellites, retrieving TLEs (Two-Line Element) data, obtaining long names of satellites, and predicting the next pass of a satellite. This code is paired with a Geometry Engine and a Back-End Database.



> To operate Mosaic, ensure that the `server.py` file is activated first. This server runs on port 3310, on the IP specified in `client.py`. Alter the IP Address in `client.py` to the address for which the `server.py` is hosted. Once the server is running, clients can be started using the `client.py` file. Multiple clients can run simultaneously, allowing for efficient satellite tracking and information retrieval.


## Required Arguments
- `task`: The task to be performed.
  - `see if server is alive`
  - `find satellite`
  - `get TLE`
  - `get long name`
  - `next pass`
- `command`: The specific command for the task.
   - `mosaic`
- `subcommand`: Additional command details.
  - `ping`
  - `satloc`
  - `tle`
  - `longname`
  - `nextpass`
- `-s <SERVER>`: Specify the server. Using "hostname" works as well.
- `-n <NORAD-ID>`: Specify the NORAD ID of the satellite.
- `-t <UTC>`: Specify the Coordinated Universal Time (UTC).
  - `MM-DD-YYYY HH:MM:SS`
- `-l <LOC>`: Specify the location.
  - `latitude longitude`
    - example: `40.446 -79.982`

## Returns
- `<SERVER-STATUS>`: Status of the server.
- `AZ [deg]`: Azimuth in degrees.
- `EL [deg]`: Elevation in degrees.
- `<TLE>`: Two-Line Element (TLE) data.
- `<longname>`: Long name of the satellite.
- `<UTC>`: Coordinated Universal Time.

## Command Line Call
- `mosaic ping       -s <SERVER> `                                           : `<SERVER-STATUS>`
- `mosaic satloc     -s <SERVER>    -n <NORAD-ID>	-t <UTC>	-l <LOC>`        : `AZ [deg], EL [deg]`
- `mosaic tle        -s <SERVER>	  -n <NORAD-ID>`                           : `<TLE>`
- `mosaic longname   -s <SERVER>	  -n <NORAD-ID>`                           : `longname`
- `mosaic nextpass   -s <SERVER>    -n <NORAD-ID> -t <UTC> -l <LOC>`         : `AZ [deg], max EL [deg], <UTC> at max EL`

## Typing 'exit' will shutdown and disconnect the client.
