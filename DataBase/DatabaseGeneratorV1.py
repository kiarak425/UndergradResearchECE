##
## SLTrack.py
## (c) 2019 Andrew Stokes  All Rights Reserved
## Edited by Jackson Andrew to better work with SWIFT-UDP research project
##
## Simple Python app to extract Iridium satellite latest data from www.space-track.org into a text file
## (Note action for you in the code below, to set up a config file with your access and output details)
## 
##
##  Copyright Notice:
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  For full licencing terms, please refer to the GNU General Public License
##  (gpl-3_0.txt) distributed with this release, or see
##  http://www.gnu.org/licenses/.
##

import requests
import json
import configparser
import time
from datetime import datetime

class MyError(Exception):
    def __init___(self,args):
        Exception.__init__(self,"my exception was raised with arguments {0}".format(args))
        self.args = args

# See https://www.space-track.org/documentation for details on REST queries
# the "Find Iridium" query searches all satellites with OBJECT_NAME matching "iridium", 1 line per sat
# the "OMM Iridium" query gets the latest Orbital Mean-Elements Messages (OMM) for a specific NORAD_CAT_ID in JSON format
# (Jackson) leaving above comment in in case readers curious how queries were made 
        # note above comment was edited to match new queries
# (Jackson) current query was edited from a suggested query by Space Track admim 
        # The reason for editing it is because the query output an HTML which wasn't useful to us     

uriBase                = "https://www.space-track.org"
requestLogin           = "/ajaxauth/login"
requestCmdAction       = "/basicspacedata/query" 
<<<<<<< Updated upstream
requestFindIridiums   = "/class/gp/GP_ID/%3E/OBJECT_TYPE/payload/orderby/GP_ID%20desc/format/json/OBJECT_NAME/iridium~~/"
requestOMMIridium1    = "/class/omm/NORAD_CAT_ID/"
requestOMMIridium2    = "/orderby/EPOCH%20desc/limit/1/emptyresult/show"
=======
requestFindIridiums    = "/class/gp/GP_ID/%3E/OBJECT_TYPE/payload/orderby/GP_ID%20desc/format/json/OBJECT_NAME/iridium~~/"
requestFindStarlinks   = "/class/gp/GP_ID/%3E/OBJECT_TYPE/payload/orderby/GP_ID%20desc/format/json/OBJECT_NAME/starlink~~/"
requestOMMStarlink1    = "/class/omm/NORAD_CAT_ID/"
requestOMMStarlink2    = "/orderby/EPOCH%20desc/limit/1/emptyresult/show"
>>>>>>> Stashed changes

timeToWaitSeconds = 43200
prompt = str(timeToWaitSeconds)


# Parameters to derive apoapsis and periapsis from mean motion (see https://en.wikipedia.org/wiki/Mean_motion)

GM = 398600441800000.0
GM13 = GM ** (1.0/3.0)
MRAD = 6378.137
PI = 3.14159265358979
TPI86 = 2.0 * PI / 86400.0

# ACTION REQUIRED FOR YOU:
#=========================
# Provide a config file in the same directory as this file, called MOSAIC_database.ini, with this format (without the # signs)
# [configuration]

# (Jackson) this is done it is already in SWIFT-UDP server with below information
# there is a reduntant add on with the output but I'm leaving it in case I need to debug with the source code

# username = "ajackson03@vt.edu"
# password = "Swift-UDP1234567"
# output = "STLtrack.xlsx"
#
# ... where XXX and YYY are your www.space-track.org credentials (https://www.space-track.org/auth/createAccount for free account)
# ... and ZZZ is your Excel Output file - e.g. starlink-track.xlsx (note: make it an .xlsx file)

# Use configparser package to pull in the ini file (pip install configparser)
config = configparser.ConfigParser()
config.read("./MOSAIC_database.ini")
configUsr = config.get("configuration","username")
configPwd = config.get("configuration","password")
configOut = config.get("configuration","output")
siteCred = {'identity': configUsr, 'password': configPwd}
# update speed from config file
speedStr = config.get("configuration","speed")
# if (int(temp)>12):
#     ## (to do) tell user they are stupid the max speed is 12 satellites before breaking
# being mod 12 because I don't want to get an API violation from bad requests
speed = int(speedStr) % 12
# get operation mode
demandPull = config.get("configuration","demandPull")
# get on demand satellite
onDemandSatellite = config.get("configuration","demandRequest")


now = datetime.now()
nowStr = now.strftime("%m/%d/%Y %H:%M:%S")
log = open("databaseLog.txt",'a')
log.write("\n" + nowStr + " Started operation")
if (demandPull == '1'):
     log.write("\n Mode: Demand Pull")
     log.write("\n Satellite: " + onDemandSatellite)
else:
    log.write("\n Mode: Normal Operation")
    log.write("\n Speed: " + speedStr)
log.close
log = open("databaseLog.txt", 'r')
log.close


if (demandPull == '1'):
    with requests.Session() as session:
        # run the session in a with block to force session to close if we exit
        

        # need to log in first. note that we get a 200 to say the web site got the data, not that we are logged in
        resp = session.post(uriBase + requestLogin, data = siteCred)
        if resp.status_code != 200:
            raise MyError(resp, "POST fail on login")
        
        
        resp = session.get(uriBase + requestCmdAction + requestOMMStarlink1 + onDemandSatellite + requestOMMStarlink2)
        if resp.status_code != 200:
            # If you are getting error 500's here, its probably the rate throttle on the site (20/min and 200/hr)
            # wait a while and retry
            print(resp)
            raise MyError(resp, "GET fail on request for Iridum satellite " + onDemandSatellite)
        retData = json.loads(resp.text)
        e = retData[-1]
        # Writes TLE data to the text file
        print(e['TLE_LINE0'] + "," + e['TLE_LINE1'] + "," + e['TLE_LINE2'] + '\n')
        f = open("MOSAIC_on_demand.txt", "w")
        now = datetime.now()
        nowStr = now.strftime("%m/%d/%Y %H:%M:%S")
        f.write(nowStr + "\n")          
        f.write(e['TLE_LINE0'] + "," + e['TLE_LINE1'] + "," + e['TLE_LINE2'] + '\n') 
        f.close
        f=open("MOSAIC_on_demand.txt", "r")
        f.close
        log = open("databaseLog.txt",'a')
        log.write("\n" + nowStr + " Completed on demand Satellite Request for " + onDemandSatellite)
        log.close
        log = open("databaseLog.txt", 'r')
        log.close
        

 # (Jackson) This is an add on I made such that it runs continuously
while True:
    if (demandPull == '1'):
        break
    with requests.Session() as session:
        # run the session in a with block to force session to close if we exit

        # need to log in first. note that we get a 200 to say the web site got the data, not that we are logged in
        resp = session.post(uriBase + requestLogin, data = siteCred)
        if resp.status_code != 200:
            raise MyError(resp, "POST fail on login")

        # this query picks up all Iridium satellites from the catalog. Note - a 401 failure shows you have bad credentials 
        # (Jackson) needs to get the list of all iridium satellites to later loop through 
        resp = session.get(uriBase + requestCmdAction + requestFindIridiums)
        if resp.status_code != 200:
            print(resp)
            raise MyError(resp, "GET fail on request for Iridium satellites")

        # use the json package to break the json formatted response text into a Python structure (a list of dictionaries)
        # (Jackson) parses above command to get loop ready
        retData = json.loads(resp.text)
        satCount = len(retData)
        satIds = []
        Satellites = []

        # (Jackson) The start of the loop
        # Loop uses e as the pointer to each omm of that satellite gained from the original search
        # builds an array of NORAD_CA_IDs to be later used in getting specific data
        for e in retData:
            # each e describes the latest elements for one Starlink satellite. We just need the NORAD_CAT_ID 
            catId = e['NORAD_CAT_ID']
            satIds.append(catId)

        # using our new list of Starlink Iridium NORAD_CAT_IDs, we can now get the OMM message
        # (Jackson) This is another loop that uses the array of NORAD_CAT_IDs to get specific data
        maxs = 1
        for s in satIds:
            resp = session.get(uriBase + requestCmdAction + requestOMMIridium1 + s + requestOMMIridium2)
            if resp.status_code != 200:
                    # If you are getting error 500's here, its probably the rate throttle on the site (20/min and 200/hr)
                    # wait a while and retry
                    print(resp)
                    raise MyError(resp, "GET fail on request for Iridum satellite " + s)

            retData = json.loads(resp.text)
            e = retData[-1]
            # print("Scanning satellite " + e['OBJECT_NAME'] + " at epoch " + e['EPOCH'])
            # Writes TLE data to the text file
            if e['DECAYED'] != '1':
                Satellites.append(e['TLE_LINE0'] + "," + e['TLE_LINE1'] + "," + e['TLE_LINE2'] + '\n')
            
            maxs = maxs + 1
            # (Jackson) This is a change from the original program where I changed the if statement from 
            # comparing 18 to comparing 5 because of getting lots of API violations
            # I think that because Starlink satellites don't have as much history this wasn't a problem
            # with starlink satellites but Iridium has been around longer which causes issues
            if maxs > 10:
                    
                    
                    # print("Snoozing for 60 secs for rate limit reasons")
                    time.sleep(60)
                    maxs = 1
        now = datetime.now()
        nowStr = now.strftime("%m/%d/%Y %H:%M:%S")
        log = open("databaseLog.txt",'a')
        log.write("\n" + nowStr + " Completed collection of Iridium satellites")
        log.close
        log = open("databaseLog.txt", 'r')
        log.close
        # START STARLINK SATELLITE FINDING

        # this query picks up all Starlink satellites from the catalog. Note - a 401 failure shows you have bad credentials 
        # (Jackson) needs to get the list of all iridium satellites to later loop through 
        resp = session.get(uriBase + requestCmdAction + requestFindStarlinks)
        if resp.status_code != 200:
            print(resp)
            raise MyError(resp, "GET fail on request for Starlink satellites")

        # use the json package to break the json formatted response text into a Python structure (a list of dictionaries)
        # (Jackson) parses above command to get loop ready
        retData = json.loads(resp.text)
        satCount = len(retData)
        satIds = []

        # (Jackson) The start of the loop
        # Loop uses e as the pointer to each omm of that satellite gained from the original search
        # builds an array of NORAD_CA_IDs to be later used in getting specific data
        for e in retData:
            # each e describes the latest elements for one Starlink satellite. We just need the NORAD_CAT_ID 
            catId = e['NORAD_CAT_ID']
            satIds.append(catId)

        # using our new list of Iridium NORAD_CAT_IDs, we can now get the OMM message
        # (Jackson) This is another loop that uses the array of NORAD_CAT_IDs to get specific data
        maxs = 1
        for s in satIds:
            resp = session.get(uriBase + requestCmdAction + requestOMMStarlink1 + s + requestOMMStarlink2)
            if resp.status_code != 200:
                    # If you are getting error 500's here, its probably the rate throttle on the site (20/min and 200/hr)
                    # wait a while and retry
                    print(resp)
                    raise MyError(resp, "GET fail on request for Iridum satellite " + s)

            retData = json.loads(resp.text)
            e = retData[-1]
            # print("Scanning satellite " + e['OBJECT_NAME'] + " at epoch " + e['EPOCH'])
            # Writes TLE data to the text file
            if e['DECAYED'] != '1':
                Satellites.append(e['TLE_LINE0'] + "," + e['TLE_LINE1'] + "," + e['TLE_LINE2'] + '\n')
            
            maxs = maxs + 1
            # (Jackson) This is a change from the original program where I changed the if statement from 
            # comparing 18 to comparing 5 because of getting lots of API violations
            # I think that because Starlink satellites don't have as much history this wasn't a problem
            # with starlink satellites but Iridium has been around longer which causes issues
            if maxs > 10:
                    
                    # print("Snoozing for 60 secs for rate limit reasons")
                    time.sleep(60)
                    maxs = 1     



        session.close()
    # (TO DO) add a way for the geometry engine to pause data collection and save the text file
        # use requests package to drive the RESTful session with space-track.org
        # get a time variable

    now = datetime.now()
    nowStr = now.strftime("%m/%d/%Y %H:%M:%S")
    log = open("databaseLog.txt",'a')
    log.write("\n" + nowStr + " Completed collection of Starlink satellites")
    log.close
    log = open("databaseLog.txt", 'r')
    log.close


    # (Jackson) open text file and write current time to it for debugging purposes
    f = open("MOSAIC_tracked.txt", "w")

    f.write(nowStr + "\n")    

    # (Jackson) export the entirety of the Satellites array into the file the save it
    # (Jackson) edit out satellites that have decayed
    for x in Satellites:
        f.write(x)   
        
    f.close

    # (Jackson) Yea I don't know, Unless I check that the program saved the file it wouldn't save the file
    # not sure how to fix it but this solution works
    f = open("MOSAIC_tracked.txt", "r")
    f.close

    # (Jackson) Clear satellites variable and prepare for the next loop
    Satellites.clear
    print("Completed session") 
    print("Pausing " + prompt + " minutes")
    time.sleep(timeToWaitSeconds)
    