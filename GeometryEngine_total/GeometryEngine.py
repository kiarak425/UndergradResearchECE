#Skyfield Read File
# Description: This file parses through the tle file 
# and gets all of the satellite information
################################################
#Importing skyfield and supporting 
from skyfield.api import load, EarthSatellite, wgs84, Topos
from geopy.geocoders import Nominatim

#Function: satelliteParser
#Returns the information from the tles given in the 
# database file
def satelliteParser():
    #files and opens the file
    with open('sltrack_iridium.txt', 'r') as file:
        #reads all lines into a list
        lines = file.readlines()  
        satelliteList = []

        
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

templist = satelliteParser()

#This function finds the specific satellite by the 
#Norad Number
def satelliteFinderID(ID):
    for element in templist:
        if(element[1] == ID):
            return element
        

#This function gets the latitude and longitude of te satellite
def latandlongFunction(number):
    ts = load.timescale()
    tempsatellite = satelliteFinderID(number)
    #Gets the satellite data loaded from a tle
    satellite = EarthSatellite(tempsatellite[2], tempsatellite[3], tempsatellite[0])

    #Gets the current realtime timescale
    t = ts.now()
    #Gets the satellite's position
    geocentric = satellite.at(t)
    #finds the latitude and longitude of the satellite
    lat, lon = wgs84.latlon_of(geocentric)

    #prints all the data
    print('Name:', tempsatellite[0])
    print('Latitude:', lat)
    print('Longitude:', lon)


def azimuth(number, lat, long, time):
    #Loads the time scale
    t = timeFinder(time)
    #finds the longitude and latitude of the position
    position1 = wgs84.latlon(lat, long)
    #finds the satellite information
    tempsatellite = satelliteFinderID(number)
    #sets up the satellite data from the TLE
    satellite = EarthSatellite(tempsatellite[2], tempsatellite[3], tempsatellite[0])
    #Finds the difference of the location to the satellite
    difference = satellite - position1
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()
    #prints out the altitude 
    print('Altitude: ', alt.degrees)
    print('Azimuth: ', az.degrees)
    #print('Distance: {:.1f} km'.format(distance.km))

#Function which finds the latitude and longitude of a city
def positionFinder(city):
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude

#Function which finds the time which the enters
def timeFinder(time):
    finalTime = time.split()
    #if user enters now, then the function will print out the current time
    if finalTime[0] == "now":
        ts = load.timescale()
        return ts.now()
    else:
        #else the function will print out the time which the user enters
        ts = load.timescale()
        t = ts.utc(int(finalTime[0]), int(finalTime[1]), int(finalTime[2]), int(finalTime[3]))
        return t


#Function to find the next pass -> the next time it passes the specific location
def nextPass(number, time, lat, long):
    observer_position = wgs84.latlon(lat, long)
    tempsatellite = satelliteFinderID(number)
    #sets up the satellite data from the TLE
    satellite = EarthSatellite(tempsatellite[2], tempsatellite[3], tempsatellite[0])

    ts = load.timescale()
    start_time = ts.now()

    # Get the next pass of the satellite over the observer position
    t, events = satellite.find_events(observer_position, start_time, 300) 

    for ti, event in zip(t, events):
        name = ('rise above %s' if event == 0 else 'culminate') % observer_position
        print(ti.utc_strftime('%Y-%m-%d %H:%M:%S'), name)
