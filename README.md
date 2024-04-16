# MOSAIC

## database

This part of the project is meant to get the most accurate and most recent data from SpaceTrack.org 

This is an edited copy of example code on SpaceTrack.org to work with the SWIFT-UDP project

there is a couple of important elements such as the configuration file with Jackson's SpaceTrack.org login information but any login information should work as long as the configuration file is updated. **NOTE**: if you want to edit this code for your own purposes I'd ask that you use your own login information to Space-Track.org. 

The current login is

username: ajackson03@vt.edu

Password: Swift-UDP1234567

There is a text file that the python script writes to. The file is temporary and is wiped after every loop of the main program. The file always starts with the date and time the file was generated. The lines of the TLE are all on one line (despite the name) and each line is separated with a comma. I have attached a sample TLE below for reference. There are a few notable elements useful for parsing. First every TLE in this file will start with a 0 then the first line of the TLE. Next each line of the TLE after the first starts with a comma then a 1 or 2 depending on which line of the TLE it is. Next notice that the NORAD ID, bolded, always ends with it's classification as a letter. This satellite is unclassified and therefore has a U after it's NORAD ID. The element just after the NORAD ID is the international identifier and also ends with a letter.

0 IRIDIUM 109,1 **41919U** 17003C   24055.16914585  .00000180  00000-0  57273-4 0  9997,2 41919  86.3912  81.2083 0002093  86.2157 273.9278 14.34216678372248

The MOSAIC_tracked.txt file is temporary. What I mean by this is that every time the program wants to change the file it rewrites the entire file from scratch. If the user wants an example file to test a parsing script with I'd recommend using MOSAIC_perm.txt which isn't seen by the program and contains an output from Febuary 26th. This will only ever be changed by human hands as necessary and is a what the final script will output. I also made a MOSAIC_small_perm.txt which is the same as MOSAIC_perm.txt but with only the first 5 elements for easier debugging. 

Editing the configuration file
I have written some example code below that will help you edit the configuration file. You will need to use configparser for this version but I'm sure there's more ways to do this. To set the speed of operation one needs to edit the configuration "speed" option to a value between 1 and 12. This will change the amount of times the program queries the site before pausing 60 seconds for limit reasons. The maximum speed is 12. If any value of speed is chosen greater than 12 the code will set the speed to the modulus of 12 and still run. I recommend changing the config file demandPull section to '0' whenever normal mode is requested, there is no reason to change demandRequest if one wants to run the program on normal mode. If one wants to request a specific satellite set the demandPull section to '1'. Then change the demandRequest section to the NORAD id of the satellite you want the TLE for. The TLE will appear on a text file which should be easily able to be read from the program or user trying to get the TLE.

If you need to remake the configuration file use the code below. If you need to edit the configuration file one should be able to edit it as they would a text file.
```
  import configparser

  MOSAIC_database = configparser.ConfigParser()

  MOSAIC_database.set("configuration", "speed", "(value from 1-12)")

  MOSAIC_database.set("configuration", "demandPull", "1 to do a demand pull or 0 for normal operation)")

  MOSAIC_database.set("configuration", "demandRequest", "(NORAD id of satellite you want)")
  ```


There are a couple TODOs ranked in order of most important

! have way to respond to server for on demand pull with TLE. Currently the program just prints the TLE to a text file. 

