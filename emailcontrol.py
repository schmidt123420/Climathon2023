from time import time
import requests
import json
from flask_mail import Mail, Message
# from app import send_emails

def email_control(mail):
    # #Retrieve start time in time.json
    # filename = "time.json"
    # with open(filename, 'r') as f:
    #     data = json.load(f)
    #     #if first time, set start time to now
    #     print(f"DATA: {data}")
    #     if data["start"] == -1:
    #         data["start"] = time()
    #         start = time()
    #     else: #if not first time, retrieve start time
    #         start = data["start"] + time()
    
    # timeElapsed = int(start - time()) #turn into int
    # print(f"TIME ELAPSED IN EMAIL CONTROL: {timeElapsed}")
    # if timeElapsed > 10_000_000_000:
    #     #reset time elapsed to 0
    #     data["start"] = 0
    #     #Update email_list.json based on AQI and asthma/age/etc
    #     updateEmailList()

    #     #Email everyone on the email list

    # #Update time.json (if not needed it just rewrites what was there before)
    # with open(filename, 'w') as f:
    #     data = json.dump(data, f)
    updateEmailList()
    send_emails(mail)


#Update email_list.json based on thresholds for each user in users.json
def updateEmailList():
    #Open email_list.json
    email_file = "email_list.json"
    with open(email_file, 'r') as efile:
        email_users = json.load(efile)
        #Retrieve users from users.json
        filename = "users.json"
        with open(filename, 'r') as ufile:
            data = json.load(ufile)
        
        print("BEFORE FOR LOOP IN UPDATE EMAIL LIST")
        for user in data:
            info = data[user]
            print(f"USER: {info}")
            if info["threshold"] == 0 and user in email_users["users"]:
                email_users["users"].remove(user)
            elif info["threshold"] == 1 and user not in email_users["users"]:
                email_users["users"].append(user)
    
    #update email list
    with open(email_file, 'w') as efile:
        json.dump(email_users, efile)


def send_emails(mail):
    efile = "email_list.json"
    userfile = "users.json"
    with open(efile, 'r') as f1:
        email_data = json.load(f1)
    with open(userfile, 'r') as f:
        userinfo = json.load(f)
        while len(email_data["users"]) > 0:
            user = email_data["users"].pop()
            print(f"USEEEEER: {user}")
            msg = f"Hello {user}, this is a warning that the AQI is {userinfo[user]['AQI']} which is above your threshold"
            message = Message(msg, sender = 'climathon2023@gmail.com', recipients = [user])
            message.body = msg

            mail.send(message)
            #send message to arduino
            sensor_index = userinfo[user]['closest sensor']
            aqi_value = userinfo[user]['AQI']
            color = "green"
            user_thresh = userinfo[user]['threshold']
            response = requests.get("https://script.google.com/macros/s/AKfycbxoUijwJgmVLw9hRk0gmyLqhoY6-WeT5-dgSkSsnAwlWG8355ONiU5XLgG-BxmW1exA/exec?request=set&sensor_index=" + str(sensor_index) + "&aqi=" + str(aqi_value) + "&color=" + color + "&user_thresh=" + str(user_thresh))
    
    with open(efile, 'w') as f2:
        # empty = {"users" : []}
        json.dump(email_data, f2)

    # updateinfo(email_data)

# def updateinfo(email_data):
#     with open("email_list.json", 'w') as f:
#         json.dump(email_data, f)