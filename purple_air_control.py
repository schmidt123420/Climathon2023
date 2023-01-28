# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#Passed in zipcode, not sensor index
#Sensor index will create itself through a zip->sensor_index function

import requests
import pgeocode
import uszipcode
from numpy import sin
from numpy import cos
from numpy import pi
from numpy import arctan2
from numpy import sqrt
#from uszipcode import zipcode

class Sensor:
    def __init__(self, Zipcode):
        self.Zipcode = Zipcode
        sensorIndex = findClosestSensor(Zipcode)
        latitude = 0
        longitude = 0
        altitude = 0
        humidity = 0
        temperature = 0
        pressure = 0
        voc = 0
        ozone1 = 0
        pm1 = 0
        pm25 = 0
        pm10 = 0

    def getData(self):
        urlString = "https://api.purpleair.com/v1/sensors?"
        fieldsString = "fields=latitude%2Clongitude%2Caltitude%2Chumidity%2Ctemperature%2Cpressure%2Cvoc%2Cozone1%2Cpm1.0%2Cpm2.5%2Cpm10.0"
        sensorIndexString = "&show_only=" + str(self.sensorIndex)
        apiString = "&api_key=AEDF734E-9E94-11ED-B6F4-42010A800007"
        callString = urlString + fieldsString + sensorIndexString + apiString
        response = requests.get(callString)
        responseDict = response.json()
        responseData = responseDict['data'][0]
        self.sensorIndex = responseData[0]
        self.latitude = responseData[1]
        self.longitude = responseData[2]
        self.altitude = responseData[3]
        self.humidity = responseData[4]
        self.temperature = responseData[5]
        self.pressure = responseData[6]
        self.voc = responseData[7]
        self.ozone1 = responseData[8]
        self.pm1 = responseData[9]
        self.pm25 = responseData[10]
        self.pm10 = responseData[11]



#Pass in lat and long, returns zipcode as string
"""
def getDistanceAway(zip1, zip2):
    geo = pgeocode.GeoDistance("us")
    dist = geo.query_postal_code(zip1, zip2)
    return dist
"""

"""
def coor2Zip(lat, long):
    result = uszipcode.SearchEngine().by_coordinates(lat, long)
    return result[0].zipcode
"""

"""
def zip2Sensor(zipcode):
    geo = pgeocode.GeoDistance("us")
    sensorZip = coor2Zip(40.001938, -83.013911)
    dist = getDistanceAway(zipcode, sensorZip)
    print(dist) #Returns distance in kilometers
"""

def distanceBetween(zipcode, latitude, longitude):
    #R = 6371
    #theta1 = (uszipcode.SearchEngine().by_zipcode(zipcode).lat)*(pi/180)
    #phi1 = (uszipcode.SearchEngine().by_zipcode(zipcode).lng)*(pi/180)
    #theta2 = latitude*(pi/180)
    #phi2 = longitude*(pi/180)

    phi1 = latitude*pi/180
    phi2 = (uszipcode.SearchEngine().by_zipcode(zipcode).lat)*(pi/180)
    deltaPhi = phi2-phi1
    deltaLambda = (longitude - uszipcode.SearchEngine().by_zipcode(zipcode).lng)*(pi/180)

    a = sin(deltaPhi/2)*sin(deltaPhi/2) + cos(phi1)*cos(phi2)*sin(deltaLambda/2)*sin(deltaLambda/2)
    c = 2*arctan2(sqrt(a), sqrt(1-a))
    distance = c

    return distance


    #x1 = R*cos(theta1)*cos(phi1)
    #y1 = R*cos(theta1)*sin(phi1)
    #z1 = R*sin(theta1)

    #x2 = R * cos(theta2) * cos(phi2)
    #y2 = R * cos(theta2) * sin(phi2)
    #z2 = R * sin(theta2)

    #distance = sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

    #theta = .5*(theta1+theta2)
    #phi = .5*(phi1+phi2)
    #distance = R*sqrt((theta2-theta1)**2 + (cos(theta))**2 * (phi2-phi1)**2)
    #print(distance)


#Takes all sensors and matches their index with a zipcode
def findClosestSensor(zipcode):
    response = requests.get("https://api.purpleair.com/v1/sensors?fields=latitude%2Clongitude&api_key=AEDF734E-9E94-11ED-B6F4-42010A800007")
    responseDict = response.json()
    responseData = responseDict['data']
    responseData_Set = {tuple(y) for y in responseData}
    closest = 11840
    minDist = 999999999999999999999999999
    for x in responseData_Set:
        if isinstance(x[1], float) == False:
            continue
        if isinstance(x[2], float) == False:
            continue
        if distanceBetween(zipcode, x[1], x[2]) < minDist:
            minDist = distanceBetween(zipcode, x[1], x[2])
            closest = x[0]


    return closest




#distanceBetween(43210, 40.001938, -83.013911)
#distanceBetween(43210, 39.963003, -121.629864)
print(findClosestSensor(84078))

