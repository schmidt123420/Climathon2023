import json
import purple_air_control as purple
def processUserData(email):
    """Calculates Air Quality Index value for user 
    whose email address is #email"""
    
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
        data[email]["closest sensor"] = s.sensorIndex
        data[email]["AQI"] = calculateAQI(s)
    
    #Write changes back to JSON file
    with open(filename, 'w') as f:
        data = json.dump(data, f)



def calculateAQI(s):
    return 200