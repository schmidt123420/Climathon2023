from flask import Flask, render_template, redirect, url_for, request
from flask_mail import Mail, Message
import flask_login

app = Flask("Climathon 2023 Thing") #create app object
app.secret_key = 'secrety secret'

#Instantiate a login manager object and link to app
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.html"

#Dictionary to model stored users
users = {
    'bob@gmail.com':{'password':'bob123', 'age':'elder', 'asthma':True, 'heart/lung':True, 'pregnant':False, 'zip code':43202, 'outdoor activity':1},
    'sarah@gmail.com':{'password':'sarah123', 'age':'adult', 'asthma':False, 'heart/lung':False, 'pregnant':True, 'zip code':43210, 'outdoor activity':3}
    }

#bad practice but it's 3:34am and I'm tired so global variable here we go
currEmail = ""

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
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'climathon2023@gmail.com'
# app.config['MAIL_PASSWORD'] = 'xacevjjzpiqprdkn'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

@app.route("/")
def home():
    # message = Message('Hello darkness my old friend', sender = 'climathon2023@gmail.com', recipients = ['schmidt.1234@osu.edu'])
    # message.body = "Testing 1 2 3 Does this work?"
    # mail.send(message)
    # return "Sent ze message"
    return render_template("login.html")

@app.route('/welcome')
def welcome():
    #render a template
    email = currEmail
    print(f"\n\ncurrEmail: {currEmail}")
    return render_template('welcome.html', email=email)

@app.route('/info')
def info():
    #render a template
    return render_template('info.html')

@app.route('/data')
def data():
    #render a template
    return render_template('data.html')

#Route for the user login page
@app.route('/form_login', methods=['GET', 'POST'])
def login():
    # error = None
    # if request.method == 'POST':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid credentials, try again'
    #     else:
    #         #successfully logged in
    #         session['is_logged_in'] = True
    #         return redirect(url_for('home'))
    # return render_template('login.html', error=error)

    #testing something
    # email = request.form['email']
    # password = request.form['password']
    # if email not in users.keys():
    #     return render_template("login.html", feedback="Invalid Email/")
    # elif users[email]["password"] != password:
    #     return render_template("login.html", feedback="Invalid Password/")
    # else:
    #     return render_template("welcome.html")



    if request.method == 'GET':
        return render_template("login.html", feedback="")
            #  return '''
            #    <form action='login' method='POST'>
            #     <input type='text' name='email' id='email' placeholder='email'/>
            #     <input type='password' name='password' id='password' placeholder='password'/>
            #     <input type='submit' name='submit'/>
            #    </form>
            #    '''
    email = request.form['email']
    password = request.form['password']
    if email in users.keys() and password == users[email]['password']:
        user = User()
        user.id = email
        print(f"EMAIL: {email}")
        currEmail = email #bad practice
        print(f"CURR EMAIL: {currEmail}")
        flask_login.login_user(user)
        return redirect(url_for('welcome'))
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