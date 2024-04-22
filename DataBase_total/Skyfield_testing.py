from skyfield.api import load, wgs84, EarthSatellite, N, W,utc
from skyfield.iokit import parse_tle_file
from datetime import datetime as dt


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

def dopplerEffect(number,time,position,fInput):
    altaz = positionAtTime(number,time, position)
    if(altaz[0]>0):


        x = velocityAtTime(number,time,position)

        c = 3*10**8

        fRecieved = (c/(c+x))*fInput

        return fRecieved
    else:
        return "Error: Satellite not in the sky at this time"

# generate a specific time in UTC
ts = load.timescale()
testtime = dt.fromisoformat('2011-11-04 00:05:23.283')
testtime= testtime.replace(tzinfo=utc)      # to fix an existing datetime   
intermediate = testtime.replace(year = 2024, day = 22, month = 4, minute= 40, hour = 12, second= 0, microsecond=0)
thisMorning = ts.from_datetime(intermediate)

# generate a specific location
blacksburg = wgs84.latlon(37.2296 * N, 80.4139 * W)

x = positionAtTime("25544",thisMorning, blacksburg)

print(x)


