# MOSAIC

## Database

This part of the project is meant to get the most accurate and most recent data from SpaceTrack.org 

This is an edited copy of example code on SpaceTrack.org to work with the SWIFT-UDP project

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

## Geometry Engine

The Geometry Engine is meant to parse through the TLE file in the Database Engine Repository. Furthermore, this iterates throughout the TLE files to get the most recent data and be able to create a list of satellite information.

## Socket

This socket is a command-line tool designed for various satellite tracking operations. It provides the ability to perform tasks such as checking server status, locating satellites, retrieving TLEs (Two-Line Element) data, obtaining long names of satellites, and predicting the next pass of a satellite. This code is paired with a Geometry Engine and a Back-End Database.

# "How to"s
## Generating Skyfield Time and Position 
There are a couple of ways to generate a Skyfield time and position but this is a method I've found is the easiest to edit on the fly to dedicate more of my time to actually working one the MOSAIC project. Using the code I put below I recommend generating a general time using pythons date and time function shown here as testtime where I set that testtime to a random time of no significance. Then to make sure this time can later be converted into the skyfields time format it is necesary to set the timezone to UTC. Finally where I set intermediate I recommend changing the values in year, day, month, minute and hour to values of more significance. I don't recommend touching seconds and microseconds as the .at() function from skyfield doesn't differentiate between seconds or lower but I left those values in just incase an interested party wanted to see the whole picture. Finally create a variable with a significant name value and use the ts.from_datetime() skyfield function to turn your intermediate datetime into a skyfield time. To get position is much easier. As I have it written I recommend only changing the latitude and longitude of the wgs84.latlon() function. Here I show how one would make blacksburg in skyfield position format. 

```
# generate a specific time in UTC
ts = load.timescale()
testtime = dt.fromisoformat('2011-11-04 00:05:23.283')
testtime= testtime.replace(tzinfo=utc)      # to fix an existing datetime   
intermediate = testtime.replace(year = 2024, day = 16, month = 4, minute= 0, hour = 5, second= 0, microsecond=0)
thisMorning = ts.from_datetime(intermediate)

# generate a specific location
blacksburg = wgs84.latlon(37.2296 * N, 80.4139 * W)
```

## Verifying skyfield is working 
The entirety of this project is based around the correct functioning of the skyfield library and the accuracy of the TLEs gained from [space-track](https://www.space-track.org/documentation). To verify the system is working there are a number of sites that do real time tracking of celestial objects. We can use these sites to check the accuracy of our program by setting the time to as close to the current time and seeing if the site and program agrees. This section details completing this check for a satellite and the sun. 

### Verifying the position of a satellite
To verifiy the position of a satellite I recommend using [NY20](https://www.n2yo.com/). This site does real time tracking of satellites including LEO satellites such as the starlink and iridium satellites. This section will outline how to check the position of the international space station, ISS, but it is just as easy to use any other satellite with this method. To use any satellite use the 'find satellite' section in the top right of the mainpage. Put in the NORAD ID  of the satellite you wish to track and click the 'track it' button.

1. Opening up N2Y0 from the homepage will have the ISS already tracked. You should see a section for azimuth and elevation. Make note of the aziumth and elevation as well as the UTC time, this is what we will be referencing to check that skyfield is working.

![N2YO output](https://github.com/kiarak425/UndergradResearchECE/blob/main/assets/N2YO%20tracking%20the%20space%20station.png)

2. Open up a file with the function dependencies for the positionAtTime() function. If you are unsure of how to do this use skyfield_testing.py file under database_total. This script is designed to have all functions and imports such that it is easy to test that skyfield is working.
3. Using your favorite debugger of which I recommend VScode's python debugger which is already set up in that directory pause at the output of the positionAtTime() function. Now write the below code. Replace the testtime.replace time with the UTC time you found from N2YO. Here the UTC time is 12:40 on April 22nd. I recommend rounding to the nearst 5 minutes but skyfield has been accurate to the nearest 1 minute in previous tests. Make note of the variable defined on the last line. Here I am using 'thisMorning'.
```
# generate a specific time in UTC
ts = load.timescale()
testtime = dt.fromisoformat('2011-11-04 00:05:23.283')
testtime= testtime.replace(tzinfo=utc)      # to fix an existing datetime   
intermediate = testtime.replace(year = 2024, day = 22, month = 4, minute= 40, hour = 12, second= 0, microsecond=0)
thisMorning = ts.from_datetime(intermediate)
```
4. Next you're going to want to set your location seen from N2YO. I recommend copying the below code. Here I am using blacksburg which is at 37.2296 N and 80.4139 W. Make note of the varaible defined. Here I am using the variable 'blacksburg'
```
# generate a specific location
blacksburg = wgs84.latlon(37.2296 * N, 80.4139 * W)
```
5. Finally call the positionAtTime() function. Before we were setting all the variables we needed to make sure the positionAtTime() function had everything it needed to accurate get the Azimuth and Elevation of a satellite. I put the code for the function call below. In this case I've set the output to a random variable x. If you don't have a debugger I'd recommend editing the positionAtTime() function to output degrees then print the output of the positionAtTime() function to the command line. 
```
x = positionAtTime("25544",thisMorning, blacksburg)
```
6. With the dubugger check the alt and az variables defined in the positionAtTime() function. These values should be accurate within a degree. Note: expect some inaccuracy due to the fact that a TLE is a guess as to where a satellite will be and is increasingly inaccurate from times different from it's epoch. I show the output of my function call below.

![skyfield output](https://github.com/kiarak425/UndergradResearchECE/blob/main/assets/skyfieldTrackingSpaceStation.png)

### Verifying the position of the sun
There are 2 different ways to get the position of the sun in real time. The first is to go outside and physically measure the azimuth and elevation of that "big glowing thing in the sky" with a compass and protractor. The second best way is with [suncalc](https://www.suncalc.org/#/37.2258,-80.4101,12/2024.04.22/08:01/1/3). Here I've linked the sun calc position of blacksburg on April 22nd.
1. To start I'd recommend finding your location on suncalc. From there take note of the time you wish to verify with skyfield. In this case I chose 8am. Suncalc doesn't give UTC dates but in the same place as finding the time it tells you the difference from UTC the location you input is. In my case Blacksburg is UTC-4 so I would add 4 to the time in skyfield to get accurate position data of the sun. Make note of the time in UTC you wish to compare. Below I put a picture of the output of suncalc.

![Suncalc](https://github.com/kiarak425/UndergradResearchECE/blob/main/assets/Suncalc%20az%20alt.png)

2. Next use the code below to get the time for the use of the .at() function. Make sure to use the UTC time. Here I have input April 22nd 8 am in Blacksburg. Make note of the variable set to the skyfield time variable in my case this variable is thisMorning.
```
# generate a specific time in UTC
ts = load.timescale()
testtime = dt.fromisoformat('2011-11-04 00:05:23.283')
testtime= testtime.replace(tzinfo=utc)      # to fix an existing datetime   
intermediate = testtime.replace(year = 2024, day = 22, month = 4, minute= 0, hour = 12, second= 0, microsecond=0)
thisMorning = ts.from_datetime(intermediate)
```
3. Next use the code below to load the planets database in skyfield. Here I have set the position of the sun to the 'sun' variable. Notice I have another line defining the position of 'earth'. This will be necessary for the next step when defining where Blacksburg is relative to the sun. 
```
planets = load('de421.bsp')  # ephemeris DE421
sun = planets['sun']
earth = planets['Earth']
```
4. Next use the code below to get the position for the relative altitude and azimuth. Here I am using the latitude and longitude of Blacksburg. Make note of the variable set to the skyfield posiiton in my case this variable is geoblacksburg. Notice the use of the 'earth' variable. 
```
goeblacksburg = earth+ wgs84.latlon(37.2296 * N, 80.4139 * W)
```
5. Finally use the below code to get the position of the sun in altitude and azimuth. I recommend writing a print statement after and pausing there to better see all the varaible terms of the alt and az variables. I have shown a photo of the output which is usually within a degree of accuracy from the real position of the sun.
```
x = goeblacksburg.at(thisMorning).observe(sun)
alt, az, d = x.apparent().altaz()
```

![sunfromskyfield](https://github.com/kiarak425/UndergradResearchECE/blob/main/assets/skyfieldsunfinding.png)
 


# Side Projects 
The purpose of the side projects section is to work on possible features of the MOSAIC program for radio astronomy. These projects typically borrow heavily from the geometry engine but lack server communication. Typically these features will be implemented as functions to later be added the geometry engine as a whole or used by other interested parties in their own scripts. 

## Distance from the sun
### Purpose
The purpose of this section of the program is to build a graph that will outline the angular distance between a satellite and the sun. The code EclipseStudy.py as standalone will generate a graph with angular distance from the sun and a satellite over the course of a specified day and month. To pick a different satellite put 1 TLE of the databaseGeneratorV1.py format into the text file associated with this repo. To pick a different day one has 2 options. The first is to change the value of the month and day variables at the beginning of ElipseStudy.py, if one chooses this option remember to find the generateDistance() function call and verify it is taking in the day and month values in that order. The second is find the generateDistance() function and change the day and month at the function call. 

### How this works
The way angular distance is calculated in this scenario is using the [angular distance forumla](https://en.wikipedia.org/wiki/Angular_distance). Using the at() function on skyfield we get the azimuth and elevation of the object in question. In the terms of the angular distance formula we get the alpha and delta in that order. I used the most accurate formula since I didn't see a reason to not be as accurate as possible and in some cases it would be possible for such assumptions to not be valid. We have already confirmed that the azimuth and elevation of an object in the sky is accurate when tracked by skyfield. For more on that topic see the section [verifying skyfield is working](##Verifying-skyfield-is-working).

## Using this Program/Function
To make this study more useful to the MOSAIC team as a whole the working part of this study has been made into a function which can easily be copied and pasted into the geometry engine or any other interested parties program. The name of this function is generateDistance(). The inputs of this function are day, month and satelliteID in that order. day and month are integers, satelliteID is a string with the NORAD ID of the satellite in question. To make sure this works copy lines 11-47 as written. The reason for this is that satelliteParser() depends on a value generated by a function call of satelliteParser() as does generateDistance(). The code will not work if the text file that satelliteParser() expects to read from isn't in the same folder as script calling the function. In EclipseStudy.py the text file is sltrack_iridium_perm_small.txt. The function returns a 1 by 1440 array with the angular distances of the satellite in question over the course of a day starting at 12am and ending at 11:59pm with each point represening a minute from the last position. This function does _not_ graph the output but if one wishes to graph the output that is done at the end of the ElcipseStudy.py program. 

| Input Name | Format | Description |
| --- | --- | --- |
| day | number (int works best) | Day of interest |
| month | number (int works best) | Month of interest |
| Satellite ID | string | NORAD ID of the satellite of interest |

### Library Dependencies
If one wishes just to copy the function generateDistance() one needs the python libraries outlined below. One is able to copy these dependcies as written in this readme for ease of use. 
```
  from skyfield.api import load, wgs84, EarthSatellite, N, W,utc
  from skyfield.iokit import parse_tle_file
  from datetime import datetime as dt
  import numpy as np
  from matplotlib import pyplot as plt
```
### Function Dependencies
If one wishes just to copy the function generateDistance() one needs the functions from other parts of the MOSAIC organization outlined below. These functions also appear in the EclipseStudy.py program. Please see the section on using this program/function for more details on how to copy these functions into your code. 

  - satelliteParser()  -  note: this means that the code works with TLEs generated by the databaseGeneratorV1.py script
  - satelliteFinderID() 
  - positionAtTime() - note: this function was built for the operation of this program and is based off of latandlongfunction() in the geometry engine
```
def satelliteParser():
    #files and opens the file
    with open('sltrack_iridium_perm_small.txt', 'r') as file:
        #reads all lines into a list
        lines = file.readlines()  
        satelliteList = []


        #skips the first line which is the data
        #the range function allows to increment by 3 lines 
        #and start at line 1 instead of 0 and 
        #go to the end of the file
        for i in range(1, len(lines)):
            singleSatellite = []
            #takes each of the lines and gives them a 
            #corresponding variable
            temp = lines[i].split(",")
            name = temp[0].strip()
            tle1 = temp[1].strip()
            tle2 = temp[2].strip()
            NORADid = tle1[2:7]
            #loads the timescale using the 
            #official Earth Rotation data
            singleSatellite.append(name)
            singleSatellite.append(NORADid)
            singleSatellite.append(tle1)
            singleSatellite.append(tle2)

            satelliteList.append(singleSatellite)

    return satelliteList

# this code is vital to the proper functioning of the function always run this between
# satelliteParser() and satelliteFinderID 
templist = satelliteParser()
temp = templist[0]
SatelliteID = temp[1]



def satelliteFinderID(ID):
    for element in templist:
        if(element[1] == ID):
            return element
        

def positionAtTime(number,time,position):
    tempsatellite = satelliteFinderID(number)
    #Gets the satellite data loaded from a tle
    satellite = EarthSatellite(tempsatellite[2], tempsatellite[3], tempsatellite[0])

    difference = satellite - position
    #Gets the satellite's position
    satFromDiff = difference.at(time)

    alt, az, distance = satFromDiff.altaz()
    # print('Altitude:', alt.degrees)
    # print('Azimuth:', az.degrees)
    # print('Distance: {:.1f} km'.format(distance.km))
    return [alt.radians, az.radians]
```
### Function as written
For ease of use I have copied the generateDistance() function below for quick analysis by interested parties.

```
def generateDistance(day, month, SatelliteID):
    testtime = dt.fromisoformat('2011-11-04 00:05:23.283')
    testtime= testtime.replace(tzinfo=utc)      # to fix an existing datetime   
    out = [0]*1440
    for x in range(0,24):
        for y in range(0,60):
            realTime = testtime.replace(year = 2024, day = day, month = month, minute= y, hour = x, second= 0, microsecond=0)

            t = ts.from_datetime(realTime)

            # gets the distance vector for a satellite
            postemp = positionAtTime(SatelliteID,t,blacksburg)
            pos1 = [np.sin(np.pi/2-postemp[0])*np.cos(postemp[1]),np.sin(np.pi/2-postemp[0])*np.sin(postemp[1]),np.cos(np.pi/2-postemp[0])]        

            goeblacksburg = earth+ wgs84.latlon(37.2296 * N, 80.4139 * W)
            astrometric = goeblacksburg.at(t).observe(sun)
            alt, az, d = astrometric.apparent().altaz()
            pos2 = [np.sin(np.pi/2-alt.radians)*np.cos(az.radians),np.sin(np.pi/2-alt.radians)*np.sin(az.radians),np.cos(np.pi/2-alt.radians)]
    

            deltaA = (postemp[1]-az.radians)*np.cos(postemp[0])
            deltaB = postemp[1]-alt.radians
            out[x*60+y] = (180/np.pi)*(np.arccos(np.sin(alt.radians)*np.sin(postemp[1])+np.cos(alt.radians)*np.cos(postemp[1])*np.cos(az.radians-postemp[0])))
    return out
```
## Doppler Effect Calculator
### Purpose
The purpose of this section of the program is to build a function able to calculate the doppler shifted frequency of a satellite given that satelliltes frequency. The program dopplerEffect.py as standalone will print to the termincal the doppler shifted frequency of the object of interest given a frequency. This is done by using a new function designed specifically for the purpose of getting the velocity of satellites relative to an oberserver. This function appears in function dependencies of this function. 

### Using this as a function/program
To make this study more useful to the MOSAIC team as a whole the working part of this study has been made into a function which can easily be copied and pasted into the geometry engine or any other interested parties program. The name of this function is dopplerEffect(). The inputs of this function are number, time, position and fInput in that order. To make sure this works copy the code appearing in function dependencies of this section. The code will not work if the text file that satelliteParser() expects to read from isn't in the same folder as script calling the function. In dopperEffect.py the text file is sltrack_iridium_perm_small.txt. Later in this section there is a description of how to generate a skyfield time format as well as a skyfield position format. Using the function as a standalone program there are a few things one must keep in mind. First is to generate a TLE of the database generator format and copy that TLE into the same .txt file your satelliteParser() function expects. Next review the section on generating a skyfield time and position format. Finally change the last input of the dopplerEffect() call to the function of the object you are trying to observe. The output of the dopplerEffect() function isn't consistent for a reason. If the satellite is in the sky the dopplerEffect() function will output the doppler shifted frequency of the satellite as observed from the ground. The function will output a string detailing an error if the satellite isn't in the sky. I recommend printing the output of this function as is but if one needs an error value such as -1 the last line of the dopplerEffect() function can be easily edited to ouptut -1.

| Input Name | Format | Description |
| --- | --- | --- |
| number | string | NORAD ID of the Satellite of interest |
| time | skyfield time format | UTC time of interest |
| position | skyfield position format | Position of oberserver |
| fInput | number (double works best) | frequency of object of interest |

### Library dependencies 
If one wishes just to copy the function generateDistance() one needs the python libraries outlined below. One is able to copy these dependcies as written in this readme for ease of use. 
```
  from skyfield.api import load, wgs84, EarthSatellite, N, W,utc
  from skyfield.iokit import parse_tle_file
  from datetime import datetime as dt
```
### Function Dependencies
If one wishes just to copy the function dopplerEffect() one needs the functions from other parts of the MOSAIC organization outlined below. These functions also appear in the dopplerEffect.py program. Please see the section on using this program/function for more details on how to copy these functions into your code. 

  - satelliteParser()  -  note: this means that the code works with TLEs generated by the databaseGeneratorV1.py script
  - satelliteFinderID() 
  - velocityAtTime()
  - positionAtTime() - note: this function was built for the operation of this program and is based off of latandlongfunction() in the geometry engine


```
def satelliteParser():
    #files and opens the file
    with open('sltrack_iridium_perm_small.txt', 'r') as file:
        #reads all lines into a list
        lines = file.readlines()  
        satelliteList = []


        #skips the first line which is the data
        #the range function allows to increment by 3 lines 
        #and start at line 1 instead of 0 and 
        #go to the end of the file
        for i in range(1, len(lines)):
            singleSatellite = []
            #takes each of the lines and gives them a 
            #corresponding variable
            temp = lines[i].split(",")
            name = temp[0].strip()
            tle1 = temp[1].strip()
            tle2 = temp[2].strip()
            NORADid = tle1[2:7]
            #loads the timescale using the 
            #official Earth Rotation data
            singleSatellite.append(name)
            singleSatellite.append(NORADid)
            singleSatellite.append(tle1)
            singleSatellite.append(tle2)

            satelliteList.append(singleSatellite)

    return satelliteList

# this code is vital to the proper functioning of the function always run this between
# satelliteParser() and satelliteFinderID 
templist = satelliteParser()
temp = templist[0]
SatelliteID = temp[1]



def satelliteFinderID(ID):
    for element in templist:
        if(element[1] == ID):
            return element
        

def velocityAtTime(number,time,position):
    tempsatellite = satelliteFinderID(number)
    #Gets the satellite data loaded from a tle
    satellite = EarthSatellite(tempsatellite[2], tempsatellite[3], tempsatellite[0])

    difference = satellite - position
    #Gets the satellite's position
    satFromDiff = difference.at(time)

    rates = satFromDiff.frame_latlon_and_rates(position)
    vel = rates[5]
    return vel.m_per_s

def positionAtTime(number,time,position):
    tempsatellite = satelliteFinderID(number)
    #Gets the satellite data loaded from a tle
    satellite = EarthSatellite(tempsatellite[2], tempsatellite[3], tempsatellite[0])

    difference = satellite - position
    #Gets the satellite's position
    satFromDiff = difference.at(time)

    alt, az, distance = satFromDiff.altaz()
    # print('Altitude:', alt.degrees)
    # print('Azimuth:', az.degrees)
    # print('Distance: {:.1f} km'.format(distance.km))
    return [alt.radians, az.radians]
```

### Function as Written
For ease of use I have copied the generateDistance() function below for quick analysis by interested parties.

```
def dopplerEffect(number,time,position,fInput):
    altaz = positionAtTime(number,time, position)
    if(altaz[0]>0):


        x = velocityAtTime(number,time,position)

        c = 3*10**8

        fRecieved = (c/(c+x))*fInput

        return fRecieved
    else:
        return "Error: Satellite not in the sky at this time"
```




