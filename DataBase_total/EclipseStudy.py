from skyfield.api import load, wgs84, EarthSatellite, N, W,utc
from skyfield.iokit import parse_tle_file
from datetime import datetime as dt
import numpy as np
from matplotlib import pyplot as plt
import configparser


config = configparser.ConfigParser()
config.read("./EclipseStudy.ini")
month = int(config.get("configuration","startDateMonth"))
day = int(config.get("configuration","startDateDay"))
oneDayTrack = bool(config.get("configuration","oneDay"))
daysElapsed = int(config.get("configuration","daysToTrack"))
latidude = bool(config.get("configuration","oneDay"))
longitude = int(config.get("configuration","daysToTrack"))


def satelliteParser():
    #files and opens the file
    with open('EclipseStudy.txt', 'r') as file:
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

def latandlongFunction(number):
    #Gets the current realtime timescale
    ts = load.timescale()
    t = ts.now()
    tempsatellite = satelliteFinderID(number)

    #Gets the satellite data loaded from a tle
    satellite = EarthSatellite(tempsatellite[2], tempsatellite[3], tempsatellite[0])

    #Gets the satellite's position
    geocentric = satellite.at(t)

    return [geocentric.position.au[0],geocentric.position.au[1],geocentric.position.au[2]]


def generateDistance(day, month, SatelliteID):
    testtime = dt.fromisoformat('2011-11-04 00:05:23.283')
    testtime= testtime.replace(tzinfo=utc)      # to fix an existing datetime   
    out = [0]*1440*daysElapsed
    for days in range(0,daysElapsed):
        for hours in range(0,24):
            for minutes in range(0,60):
                realTime = testtime.replace(year = 2024, day = day+days, month = month, minute= minutes, hour = hours, second= 0, microsecond=0)

                t = ts.from_datetime(realTime)

                # gets the distance vector for a satellite
                postemp = positionAtTime(SatelliteID,t,location)
                # pos1 = [np.sin(np.pi/2-postemp[0])*np.cos(postemp[1]),np.sin(np.pi/2-postemp[0])*np.sin(postemp[1]),np.cos(np.pi/2-postemp[0])]        

                locationGEO = earth+ wgs84.latlon(latidude * N, longitude * W)
                astrometric = locationGEO.at(t).observe(sun)
                alt, az, d = astrometric.apparent().altaz()
                # pos2 = [np.sin(np.pi/2-alt.radians)*np.cos(az.radians),np.sin(np.pi/2-alt.radians)*np.sin(az.radians),np.cos(np.pi/2-alt.radians)]
        

                # deltaA = (postemp[1]-az.radians)*np.cos(postemp[0])
                # deltaB = postemp[1]-alt.radians
                out[hours*60+minutes+1440*days] = (180/np.pi)*(np.arccos(np.sin(alt.radians)*np.sin(postemp[1])+np.cos(alt.radians)*np.cos(postemp[1])*np.cos(az.radians-postemp[0])))
    return out

ts = load.timescale()
planets = load('de421.bsp')  # ephemeris DE421
sun = planets['sun']
earth = planets['Earth']
location = wgs84.latlon(latidude * N, longitude * W)

out = generateDistance(day,month,SatelliteID)

# print(out)
figure, axes = plt.subplots()
monthstr = str(month)
daystr = str(day)
satelliteName = temp[0]

satelliteName= satelliteName.replace("0", " ")
satelliteName= satelliteName.strip()
plt.title("distance " +satelliteName+ " from sun on " + monthstr + '/' + daystr)
plt.xlabel("minutes in a day")
plt.ylabel("angular separation (deg)")
x = np.arange(1440*daysElapsed)
plt.plot(x,out,'.',color = 'blue')
plt.ylim(0,180)
plt.show()