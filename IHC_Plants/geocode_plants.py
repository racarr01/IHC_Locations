import geopy.geocoders
from geopy.geocoders import TomTom as Tom
from geopy.exc import GeocoderTimedOut
import csv
keys_file = open("/home/racarr/projects/IHC_Geocode/tomtom.txt")
lines = keys_file.readlines()
user_agent = lines[0].rstrip()
last_loc = ''
tomtom_api_key = lines[1].rstrip()
keys_file.close()

geopy.geocoders.options.default_timeout = 30
geolocator = Tom(user_agent=user_agent,api_key=tomtom_api_key)
def do_geocode(address,n):
    if (n < 5):
        try:
            return geolocator.geocode(address)
        except GeocoderTimedOut:
            n = n + 1
            return do_geocode(address,n)

with open("/home/racarr/projects/IHC_Geocode/IH_Plants/plants.csv","r") as infile,\
open ("/home/racarr/projects/IHC_Geocode/IH_Plants/plants_geo.csv","a") as outfile,\
open ("/home/racarr/projects/IHC_Geocode/IH_Plants/plants_err.txt", "w") as errfile:
    reader = csv.reader(infile, delimiter=",")
    for i, line in enumerate(reader):
         if (i > 0):
             line = [n.replace('"', '') for n in line]
             #print (line[1])
             loc = '{}, {}, {}'.format(line[0],line[1],line[2])
             print (loc) 
             if (loc == last_loc):
                 outfile.write ('\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"\n'.format(line[0],\
                 line[1],line[2],line[3],line[4],location.latitude,location.longitude))
             else:
                 location = do_geocode(loc,1)
                 if (location):
                     #outfile.write ('{},{},{}\n'.format(str(line)[1:-1],location.latitude,location.longitude))
                     outfile.write ('\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"\n'.format(line[0],\
                     line[1],line[2],line[3],line[4],location.latitude,location.longitude))
                     last_loc = loc
                 else:
                     errfile.write ('Error {}\n'.format(line))

        

