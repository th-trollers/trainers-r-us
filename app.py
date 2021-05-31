import pyrebase

from flask import *
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
app = Flask(__name__, template_folder="html")
app.secret_key= "trainersrus"
app.permanent_session_lifetime = timedelta(minutes = 60)
config = {
    "apiKey": "AIzaSyCRQLgByC3jG5YbDViv1i_9KnckWEgePC0",
    "authDomain": "trainers-r-us.firebaseapp.com",
    "projectId": "trainers-r-us",
    "databaseURL" : "",
    "storageBucket": "trainers-r-us.appspot.com",
    "messagingSenderId": "128175027453",
    "appId": "1:128175027453:web:4b91f00815ac01c4747a94",
    "measurementId": "G-6JY1N1W5ZY"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

@app.route('/', methods = ["POST", "GET"])
def loginPage():
    unsuccessful = "Please check your credentials"
    successful = "Login successful"
    if request.method == "POST":
        email = request.form["name"]
        password = request.form["pass"]
        try:
            auth.sign_in_with_email_and_password(email, password)
            return render_template("HomePage.html")
        except:
            flash(unsuccessful)
            return render_template("LoginPage.html")
    return render_template("LoginPage.html")

@app.route('/', methods = ["POST", "GET"])
def homePage():
    return render_template("HomePage.html")

if __name__ == "__main__":
    app.run()

# email = input("Please enter your email\n")

# password = input("Please enter your password\n")

# user = auth.create_user_with_email_and_password(email, password)

# user = auth.sign_in_with_email_and_password(email, password)

# auth.send_password_reset_email(email)

# auth.send_email_verification(user["idToken"])

# print(auth.get_account_info(user["idToken"]))


