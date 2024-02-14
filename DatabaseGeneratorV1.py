##
## SLTrack.py
## (c) 2019 Andrew Stokes  All Rights Reserved
##
##
## Simple Python app to extract Starlink satellite history data from www.space-track.org into a spreadsheet
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
import xlsxwriter
import time
from datetime import datetime

class MyError(Exception):
    def __init___(self,args):
        Exception.__init__(self,"my exception was raised with arguments {0}".format(args))
        self.args = args

# See https://www.space-track.org/documentation for details on REST queries
# the "Find Starlinks" query searches all satellites with NORAD_CAT_ID > 40000, with OBJECT_NAME matching STARLINK*, 1 line per sat
# the "OMM Starlink" query gets all Orbital Mean-Elements Messages (OMM) for a specific NORAD_CAT_ID in JSON format

uriBase                = "https://www.space-track.org"
requestLogin           = "/ajaxauth/login"
requestCmdAction       = "/basicspacedata/query" 
requestFindStarlinks   = "/class/gp/GP_ID/%3E/OBJECT_TYPE/payload/orderby/GP_ID%20desc/format/json/OBJECT_NAME/iridium~~/"
requestOMMStarlink1    = "/class/omm/NORAD_CAT_ID/"
requestOMMStarlink2    = "/orderby/EPOCH%20asc/format/limit/1/json"

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
# Provide a config file in the same directory as this file, called SLTrack.ini, with this format (without the # signs)
# [configuration]
# username = "ajackson03@vt.edu"
# password = "IdowhatIwant1!!!"
# output = "STLtrack.xlsx"
#
# ... where XXX and YYY are your www.space-track.org credentials (https://www.space-track.org/auth/createAccount for free account)
# ... and ZZZ is your Excel Output file - e.g. starlink-track.xlsx (note: make it an .xlsx file)

# Use configparser package to pull in the ini file (pip install configparser)
config = configparser.ConfigParser()
config.read("./SLTrack.ini")
configUsr = config.get("configuration","username")
configPwd = config.get("configuration","password")
configOut = config.get("configuration","output")
siteCred = {'identity': configUsr, 'password': configPwd}


 
while True:
    # use requests package to drive the RESTful session with space-track.org
        # get a time variable
    now = datetime.now()
    nowStr = now.strftime("%m/%d/%Y %H:%M:%S")

    # (Jackson) open text file
    f = open("sltrack_iridium.txt", "w")
    f.write(nowStr + "\n")

    with requests.Session() as session:
        # run the session in a with block to force session to close if we exit

        # need to log in first. note that we get a 200 to say the web site got the data, not that we are logged in
        resp = session.post(uriBase + requestLogin, data = siteCred)
        if resp.status_code != 200:
            raise MyError(resp, "POST fail on login")

        # this query picks up all Starlink satellites from the catalog. Note - a 401 failure shows you have bad credentials 
        resp = session.get(uriBase + requestCmdAction + requestFindStarlinks)
        if resp.status_code != 200:
            print(resp)
            raise MyError(resp, "GET fail on request for Starlink satellites")

        # use the json package to break the json formatted response text into a Python structure (a list of dictionaries)
        retData = json.loads(resp.text)
        satCount = len(retData)
        satIds = []
        for e in retData:
            # each e describes the latest elements for one Starlink satellite. We just need the NORAD_CAT_ID 
            catId = e['NORAD_CAT_ID']
            satIds.append(catId)

        # using our new list of Starlink satellite NORAD_CAT_IDs, we can now get the OMM message
        maxs = 1
        for s in satIds:
            resp = session.get(uriBase + requestCmdAction + requestOMMStarlink1 + s + requestOMMStarlink2)
            if resp.status_code != 200:
                    # If you are getting error 500's here, its probably the rate throttle on the site (20/min and 200/hr)
                    # wait a while and retry
                    print(resp)
                    raise MyError(resp, "GET fail on request for Starlink satellite " + s)

                # the data here can be quite large, as it's all the elements for every entry for one Starlink satellite
            retData = json.loads(resp.text)
            # each element is one reading of the orbital elements for one Starlink
            e = retData[-1]
            print("Scanning satellite " + e['OBJECT_NAME'] + " at epoch " + e['EPOCH'])

            f.write(e['TLE_LINE0'] + "\n")
            f.write(e['TLE_LINE1'] + "\n")
            f.write(e['TLE_LINE2'] + "\n") 
            
            maxs = maxs + 1
            if maxs > 18:
                    break
                    print("Snoozing for 60 secs for rate limit reasons (max 20/min and 200/hr)...")
                    time.sleep(60)
                    maxs = 1
        session.close()
    
    f.close
    break
    print("Completed session") 
    print("pausing " + prompt)
    time.sleep(timeToWaitSeconds)
