import pyrebase

from flask import *
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
app = Flask(__name__, template_folder="html")
app.secret_key = "trainersrus"
app.permanent_session_lifetime = timedelta(minutes=60)
config = {
    "apiKey": "AIzaSyCRQLgByC3jG5YbDViv1i_9KnckWEgePC0",
    "authDomain": "trainers-r-us.firebaseapp.com",
    "projectId": "trainers-r-us",
    "databaseURL": "https://trainers-r-us-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "trainers-r-us.appspot.com",
    "messagingSenderId": "128175027453",
    "appId": "1:128175027453:web:4b91f00815ac01c4747a94",
    "measurementId": "G-6JY1N1W5ZY"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
database = firebase.database()

@app.route('/')
def homePage():
    return render_template("HomePage.html")

# need to fix the part where the email is not valid or
# he did not use a proper email
@app.route('/memberLogin', methods=["POST", "GET"])
def memberLogin():
    unsuccessful = "Please check your credentials"
    successful = "Login successful"
    if request.method == "POST":
        email = request.form["name"]
        password = request.form["pass"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print(successful)
            return redirect(url_for("memberHome"))
        except:
            flash(unsuccessful)
            print(unsuccessful)
            return redirect(url_for("memberLogin"))
    return render_template("MemberLogin.html")


@app.route('/memberHome', methods=["POST", "GET"])
def memberHome():
    return render_template("MemberHome.html")

@app.route('/createNewMember', methods = ["POST", "GET"])
def createNewMember(): 
    if request.method == "POST":
        try:
            # getting the email and pw
            email = str(request.form["email"])
            pw = str(request.form["userpassword"])
            if len(pw) < 6:
                flash("Password too short please try a new one")
                return render_template("CreateNewMember.html")
            else:
                user = auth.create_user_with_email_and_password(email, pw)
                print("Successfully created an account")
                flash("Please go to your email to verify your account")
                auth.send_email_verification(user["idToken"])
        except:
            flash("Please enter valid details")             
        return redirect(url_for("memberDetails"))
    else:
        return render_template("CreateNewMember.html")

@app.route('/memberDetails', methods=["POST", "GET"])
def memberDetails():
    if request.method == "POST":
        try:
            name = request.form["membername"]
            age = request.form["age"]
            location = request.form["location"]
            # still need to settle the lvl of trg and type of trg part
            data = {"Name": name, "Age": age, "Location": location}
            database.child("Users").child(name).set(data)
            print("data has been created")
        except:
            print("smth is wrong")
        flash("Please key in your details")
        return redirect(url_for("memberLogin"))
    else:
        return render_template("MemberDetails.html")

if __name__ == "__main__":
    app.run()

# email = input("Please enter your email\n")

# password = input("Please enter your password\n")

# user = auth.create_user_with_email_and_password(email, password)

# user = auth.sign_in_with_email_and_password(email, password)

# auth.send_password_reset_email(email)

# auth.send_email_verification(user["idToken"])

# print(auth.get_account_info(user["idToken"]))