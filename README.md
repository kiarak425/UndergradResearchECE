# UndergradResearchECE-Database

This part of the project is meant to get the most accurate and most recent data from SpaceTrack.org 

This is an edited copy of example code on SpaceTrack.org to work with the SWIFT-UDP project

there is a couple of important elements such as the configuration file with Jackson's SpaceTrack.org login information but any login information should work as long as the configuration file is updated. **NOTE**: if you want to edit this code for your own purposes I'd ask that you use your own login information to Space-Track.org. 

<<<<<<< Updated upstream
One thing to note is the name of the python script as DatabaseGeneratorV1 even though we are using Github to keep the database up to date, having it named V1 is useful in case Jackson's credentials gets flagged with an API violation. The same code would work but that specific script would not. This information was found after trying to debug the first iteration of the program a day after Jackson recieved an API violation. The main goal is to never get API violations but if they do happen while debugging (what caused the first API violation) there is an easy solution in changing the name of the script to DatabaseGeneratorV2 and so on. 

There is a text file that the python script writes to. The file is temporary and is wiped after every loop of the main program. The file always starts with the date and time the file was generated.
You might notice it has some change notifications this is because if I run the code Github notices a change in the file and exports it along with the changed code.
=======
The current login is

username: ajackson03@vt.edu

Password: Swift-UDP1234567

There is a text file that the python script writes to. The file is temporary and is wiped after every loop of the main program. The file always starts with the date and time the file was generated. The lines of the TLE are all on one line (despite the name) and each line is separated with a comma. I have attached a sample TLE below for reference. There are a few notable elements useful for parsing. First every TLE in this file will start with a 0 then the first line of the TLE. Next each line of the TLE after the first starts with a comma then a 1 or 2 depending on which line of the TLE it is. Next notice that the NORAD ID, bolded, always ends with it's classification as a letter. This satellite is unclassified and therefore has a U after it's NORAD ID. The element just after the NORAD ID is the international identifier and also ends with a letter.

0 IRIDIUM 109,1 **41919U** 17003C   24055.16914585  .00000180  00000-0  57273-4 0  9997,2 41919  86.3912  81.2083 0002093  86.2157 273.9278 14.34216678372248

The sltrack_iridium.txt file is temporary. What I mean by this is that every time the program wants to change the file it rewrites the entire file from scratch. If the user wants an example file to test a parsing script with I'd recommend using sltrack_iridium_perm.txt which isn't seen by the program and contains an output from Febuary 26th. This will only ever be changed by human hands as necessary and is a what the final script will output. I also made a sltrack_iridium_perm_small.txt which is the same as sltrack_iridium_perm.txt but with only the first 5 elements for easier debugging. 

Editing the configuration file
I have written some example code below that will help you edit the configuration file. You will need to use configparser for this version but I'm sure there's more ways to do this. To set the speed of operation one needs to edit the configuration "speed" option to a value between 1 and 12. This will change the amount of times the program queries the site before pausing 60 seconds for limit reasons. The maximum speed is 12. If any value of speed is chosen greater than 12 the code will set the speed to the modulus of 12 and still run. I recommend changing the config file demandPull section to '0' whenever normal mode is requested, there is no reason to change demandRequest if one wants to run the program on normal mode. If one wants to request a specific satellite set the demandPull section to '1'. Then change the demandRequest section to the NORAD id of the satellite you want the TLE for. 

NOTE: for now the code just prints the TLE to the command line

**Start code for changing the configuration file**

  import configparser

  SLTrack = configparser.ConfigParser()

  SLTrack.set("configuration", "speed", "(value from 1-12)")

  SLTrack.set("configuration", "demandPull", "1 to do a demand pull or 0 for normal operation)")

  SLTrack.set("configuration", "demandRequest", "(NORAD id of satellite you want)")

**End code for changing the configuration file**
>>>>>>> Stashed changes

There are a couple TODOs ranked in order of most important

<<<<<<< Updated upstream
(completed 2/17) Find a new query that only gets the most recent OMM data from space track. Currently the code is getting all historical data which was fine for the source code which only tracked starlink satellites with less historical data but not so much for iridum. 
=======
!!! have way to respond to server for on demand pull with TLE. Currently the program just prints the TLE to the command line. 
>>>>>>> Stashed changes

!! have way to respond to server if the configuration file is messed up. Ex. speed more than 12 should tell the user that that speed won't work.

