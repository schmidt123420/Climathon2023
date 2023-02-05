import json
import purple_air_control as purple
def processUserData(email):
    """Calculates Air Quality Index value for user 
    whose email address is email"""
    
    #Retrieve current user info in currUser.json
    filename = "users.json"
    with open(filename, 'r') as f:
        data = json.load(f)
    
    #If AQI hasn't been set then calculate it
    if data[email]['AQI'] == -1:
        print("CALCULATING NEW AQI")
        zip = data[email]["zipcode"]
        s = purple.Sensor(zip)
        s.getData()
        s.sensorIndex = s.findClosestSensor(zip)
        data[email]["closest sensor"] = s.sensorIndex
        # data[email]["AQI"] = calculateAQI(s, data[email])
        data[email]["AQI"] = s.pm25

        data[email]['threshold'] = calculateThreshold(s, data[email])
    
    #Write changes back to JSON file
    with open(filename, 'w') as f:
        data = json.dump(data, f)

def calculateThreshold(s, user_info):
    return s.sensorIndex
    

def calculateAQI(s, user_info):
    return s.pm1 + s.pm25 + s.pm10