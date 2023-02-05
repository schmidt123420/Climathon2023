from flask import Flask, render_template, redirect, url_for, request
from flask_mail import Mail, Message
import flask_login
import json
import purple_air_control as purple
from calculations import processUserData
from emailcontrol import email_control

app = Flask("Climathon 2023 Thing") #create app object
app.secret_key = 'secrety secret'

#Instantiate a login manager object and link to app
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.html"

#Dictionary to model stored users
users = {
    'schmidt.1234@osu.edu':{'password':'bob123', 'name':'Bob Jones', 'age':'elder', 'asthma':True, 'heart/lung':True, 'pregnant':False, 'zip code':43202, 'outdoor activity':1},
    'sarah@gmail.com':{'password':'sarah123', 'name':'Sarah Boat', 'age':'adult', 'asthma':False, 'heart/lung':False, 'pregnant':True, 'zip code':43210, 'outdoor activity':3}
    }

#Define User object
class User(flask_login.UserMixin):
    pass

#Define user_loader callback
@login_manager.user_loader
def user_loader(email):
    if email not in users.keys():
        return
    else:
        user = User()
        user.id = email
        return user

#Define request_loader callback
@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users.keys():
        return
    else:
        user = User()
        user.id = email
        return user


#configuration for email address to send email from
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'climathon2023@gmail.com'
app.config['MAIL_PASSWORD'] = 'xacevjjzpiqprdkn'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def home():
    return render_template("login.html")

@app.route('/welcome')
def welcome():
    #Retrieve current user info in currUser.json
    filename = "currUser.json"
    with open(filename, 'r') as f:
        email = json.load(f)
    email_control(mail)
    return render_template('welcome.html', email=email['email'], users=users)

@app.route('/info')
def info():
    #render a template
    email_control(mail)
    return render_template('info.html')

@app.route('/data')
def data():
    #render a template
    email_control(mail)
    return render_template('data.html')

#Route for the user login page
@app.route('/form_login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", feedback="")
    email = request.form['email']
    password = request.form['password']

    #Store current user info in currUser.json
    currUser = {'email':email} #data to be stored
    filename = "currUser.json"
    with open(filename, 'w') as f:
        json.dump(currUser, f)

    if email in users.keys() and password == users[email]['password']:
        processUserData(email)
        email_control(mail)
        print("PROCESSING USER DATA!!!")
        user = User()
        user.id = email
        print(f"EMAIL: {email}")
        currEmail = email #bad practice
        print(f"CURR EMAIL: {currEmail}")
        print(f"USERS: {users}")
        flask_login.login_user(user)
        # return redirect(url_for('welcome'))
        return render_template("welcome.html", email=currEmail, users=users)
    # return 'Incorrect Email/Password'
    elif email not in users.keys():
        return render_template("login.html", feedback="Invalid Email")
    elif users[email]["password"] != password:
        return render_template("login.html", feedback="Invalid Email/Password")
    else:
        return "Something has gone wrong!"



@app.route('/protected')
@flask_login.login_required
def protected():
    return f"Logged in as: {flask_login.current_user.id}"

#Route for logging user out
@app.route('/logout')
def logout():
    # session.pop('is_logged_in', None)
    # return redirect()
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


if __name__ == '__main__':
    app.run(debug = True)
