import GeometryEngine

#Function which takes in the server input and returns the Azimuth and Elevation
def get_azimuth_elevation(norad_id, lat, long, utc_datetime):

    azimuth = GeometryEngine.azimuth(norad_id, lat, long, utc_datetime)
    return azimuth

#Function which takes the norad id and returns the TLE
def get_tle(norad_id):
    tleInformation = GeometryEngine.satelliteFinderID(norad_id)
    return f"Line 1: {tleInformation[2]}, Line 2: {tleInformation[3]}"

#Function which takes the norad id and returns the satellite name
def get_name(norad_id):
    tleInformation = GeometryEngine.satelliteFinderID(norad_id)
    return f"Satellite Name: {tleInformation[0]}"

#Next pass of satellite
def get_next_pass(norad_id, utc_date, utc_time, lat, long):
    next_pass_info = GeometryEngine.nextPass(norad_id, utc_date, utc_time, lat, long)
    return f"Next Pass: {next_pass_info}"


