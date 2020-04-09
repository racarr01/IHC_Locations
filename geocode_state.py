import geopy.geocoders
from geopy.geocoders import TomTom as Tom
from geopy.exc import GeocoderTimedOut
import csv
import os
import sys
from dotenv import load_dotenv
load_dotenv()
#keys_file = open("/home/racarr/projects/IHC_Geocode/tomtom.txt")
#lines = keys_file.readlines()
#user_agent = lines[0].rstrip()
#tomtom_api_key = lines[1].rstrip()
#keys_file.close()
TT_AGENT = os.getenv("user_agent")
TOMTOM_API_KEY = os.getenv("api_key")
geopy.geocoders.options.default_timeout = 30
geolocator = Tom(user_agent=TT_AGENT,api_key=TOMTOM_API_KEY)
fldr = sys.argv[1]
basedir = "/home/racarr/projects/IHC_Locations/"

def do_geocode(address,n):
    if (n < 5):
        try:
            return geolocator.geocode(address)
        except GeocoderTimedOut:
            n = n + 1
            return do_geocode(address,n)
Files = []
Files.append(basedir + fldr + "/" + fldr + ".csv")
Files.append(basedir + fldr + "/" + fldr + "_geo.csv")
Files.append(basedir + fldr + "/" + fldr + "_err.txt")

if (fldr == "test"):
    print(Files[0])
    print(Files[1])
    print(Files[2])


    exit()


with open("/home/racarr/projects/IHC_Geocode/in.csv","r") as infile,\
open ("/home/racarr/projects/IHC_Geocode/in_geo.csv","a") as outfile,\
open ("/home/racarr/projects/IHC_Geocode/in_err.txt", "w") as errfile:
    reader = csv.reader(infile, delimiter=",")
    for i, line in enumerate(reader):
         if (i > 0):
             line = [n.replace('"', '') for n in line]
             #print (line[1])
             loc = '{}, {}, {} USA'.format(line[1],line[2],line[3])
             print (loc)
             location = do_geocode(loc,1)
             if (location):
                 #outfile.write ('{},{},{}\n'.format(str(line)[1:-1],location.latitude,location.longitude))
                 outfile.write ('\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",{},{}\n'.format(line[0],\
                 line[1],line[2],line[3],line[4],location.latitude,location.longitude))
             else:
                 errfile.write ('Error {}\n'.format(line))

        

