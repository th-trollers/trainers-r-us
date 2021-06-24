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
        session.permanent = True
        username = request.form["name"]
        password = request.form["pass"]
        try:
            user = auth.sign_in_with_email_and_password(username, password)
            print(successful)
            usernameTwo = username.replace(".", "_DOT_")
            session["username"] = usernameTwo
            return redirect(url_for("memberHome"))
        except:
            flash(unsuccessful)
            print(unsuccessful)
            return redirect(url_for("memberLogin"))
    return render_template("MemberLogin.html")


@app.route('/memberHome', methods=["POST", "GET"])
def memberHome():
    if "username" in session:
        username = str(session["username"])
        flash("Welcome " + database.child("Users").child(username).get().val()["Name"])
    return render_template("MemberHome.html")

@app.route('/createNewMember', methods = ["POST", "GET"])
def createNewMember(): 
    if request.method == "POST":
        try:
            # getting the email and pw
            email = str(request.form["email"])
            pw = str(request.form["userpassword"])
            name = str(request.form["membername"])
            number = str(request.form["number"])
            gender = str(request.form["gender"])
            trglvl = str(request.form["trglvl"])
            trgtype = str(request.form["trgtype"])
            print('test')
            print(email)
            print(pw)
            print(name)
            print(number)
            print(gender)
            print(trglvl)
            print(trgtype)
            if len(pw) < 6:
                flash("Password too short please try a new one")
                return render_template("CreateNewMember.html")
            else:
                user = auth.create_user_with_email_and_password(email, pw)
                print("Successfully created an account")
                flash("Please go to your email to verify your account")
                auth.send_email_verification(user["idToken"])
                emailTwo = email.replace(".", "_DOT_")
                data = {"Email": emailTwo, "Name": name, "Number": number, "Gender": gender, "Training Level": trglvl, "Training Type": trgtype}
                database.child("Users").child(emailTwo).set(data)
                print("data has been created")
        except:
            print("went to except")
            flash("Please enter valid details")   
            return render_template("CreateNewMember.html")  
        return redirect(url_for("memberLogin"))
    else:
        return render_template("CreateNewMember.html")

@app.route('/memberDetails', methods=["GET"])
def memberDetails():
    if "username" in session:
        username = str(session["username"])
        dict = database.child("Users").child(username).get()
        lst = []
        for value in dict.val().values():
            lst.append(value)
        print(lst)
    return render_template("MemberDetails.html", details = lst)

@app.route("/memberDetailUpdate", methods = ["POST", "GET"])
def memberDetailUpdate():
    if "username" in session:
        username = str(session["username"])
        new = request.form.get("new")
        print(new)
        print(type(new))
        old = request.form.get("old")
        print(old)
        print(type(old))
        dict = database.child("Users").child(username).get().val()
        lst = []
        for value in dict.values():
            lst.append(value)
        for key,value in dict.items():
            if old == value:
                database.child("Users").child(username).update({key : new})
                flash("Please refresh page to see changes")
                break
    return render_template("MemberDetailUpdate.html", details = lst)


@app.route("/logout")
def logout():
    flash(f"You have been logged out")
    session.pop("email", None)
    session.pop("name", None)
    return redirect(url_for("homePage"))

if __name__ == "__main__":
    app.run()

# email = input("Please enter your email\n")

# password = input("Please enter your password\n")

# user = auth.create_user_with_email_and_password(email, password)

# user = auth.sign_in_with_email_and_password(email, password)

# auth.send_password_reset_email(email)

# auth.send_email_verification(user["idToken"])

# print(auth.get_account_info(user["idToken"]))