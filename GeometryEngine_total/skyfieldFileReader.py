from skyfield.api import load, EarthSatellite, wgs84

# Load TLE data from a text file
with open('sltrack_iridium.txt', 'r') as file:
    lines = file.readlines()

# Extract the TLE lines
line1 = lines[1].strip()
line2 = lines[2].strip()

# Load the timescale and satellite data
ts = load.timescale()
satellite = EarthSatellite(line1, line2, name="Satellite")

#return an (x,y,z) position relative to the Earth’s center 
#in the Geocentric Celestial Reference System
# You can instead use ts.now() for the current time
t = ts.now()

geocentric = satellite.at(t)
print(geocentric.position.km)

##LAT AND LONG
lat, lon = wgs84.latlon_of(geocentric)
print('Latitude:', lat)
print('Longitude:', lon)




# Optionally, write the results to a new text file
# with open('results.txt', 'w') as file:
#     # Write results to the file
#     file.write(...)