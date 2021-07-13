from os import path
import pyrebase
from flask import *
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from wtforms import SelectField

app = Flask(__name__, template_folder="html")
app.secret_key = "trainersrus"
app.permanent_session_lifetime = timedelta(minutes=60)
config = {
    "apiKey": "AIzaSyCRQLgByC3jG5YbDViv1i_9KnckWEgePC0",
    "authDomain": "trainers-r-us.firebaseapp.com",
    "projectId": "trainers-r-us",
    "databaseURL": "https://trainers-r-us-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "trainers-r-us.appspot.com",
    "serviceAccount": "trainers-r-us/serviceAccountKey.json",
    "messagingSenderId": "128175027453",
    "appId": "1:128175027453:web:4b91f00815ac01c4747a94",
    "measurementId": "G-6JY1N1W5ZY"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()
storage = firebase.storage()
all_files = storage.list_files()
# storage.child("images/foo.jpg").download("myface.jpg")

# need to fix the part where the email is not valid or
# he did not use a proper email

# Main Home Page


@app.route('/')
def homePage():
    return render_template("HomePage.html")

# Login Pages


@app.route('/memberLogin', methods=["POST", "GET"])
def memberLogin():
    unsuccessful = "Incorrect email or password"
    successful = "Login successful"
    if request.method == "POST":
        session.permanent = True
        username = request.form["name"]
        password = request.form["pass"]
        usernameTwo = username.replace(".", "_DOT_")
        if database.child("Users").child(usernameTwo).get().val() == None:
            flash("You do not have an account with us")
            print("You do not have an account with us")
            return redirect(url_for("memberLogin"))
        try:
            user = auth.sign_in_with_email_and_password(username, password)
            print(successful)
            session["username"] = usernameTwo
            session["userToken"] = user
            return redirect(url_for("memberHome"))
        except:
            flash(unsuccessful)
            print(unsuccessful)
            return redirect(url_for("memberLogin"))
    return render_template("MemberLogin.html")


@app.route('/trainerLogin', methods=["POST", "GET"])
def trainerLogin():
    unsuccessful = "Incorrect email or password"
    successful = "Login successful"
    if request.method == "POST":
        session.permanent = True
        email = request.form["name"]
        password = request.form["pass"]
        usernameTwo = email.replace(".", "_DOT_")
        if database.child("Trainers").child(usernameTwo).get().val() == None:
            flash("You do not have an account with us")
            print("You do not have an account with us")
            return redirect(url_for("trainerLogin"))
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print(successful)
            session["username"] = usernameTwo
            session["userToken"] = user
            return redirect(url_for("trainerHome"))
        except:
            flash(unsuccessful)
            print(unsuccessful)
            return redirect(url_for("trainerLogin"))
    return render_template("trainerLogin.html")

# Member and Trainer Home Page


@app.route('/memberHome', methods=["POST", "GET"])
def memberHome():
    return render_template("MemberHome.html")


@app.route('/trainerHome', methods=["POST", "GET"])
def trainerHome():
    return render_template("trainerHome.html")


# Creating New Users Page
@app.route('/createNewMember', methods=["POST", "GET"])
def createNewMember():
    if request.method == "POST":
        try:
            # getting the email and pw
            email = str(request.form["email"])
            print(email)
            pw = str(request.form["userpassword"])
            print(pw)
            name = str(request.form["membername"])
            print(name)
            number = str(request.form["number"])
            print(number)
            gender = str(request.form["gender"])
            print(gender)
            trglvl = str(request.form["trglvl"])
            print(trglvl)
            trgtype = str(request.form["trgtype"])
            print(trgtype)
            pic = request.files["picture"]
            print(pic)
            print('test')            
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
                print("Successfully uploaded personal details")
                path_on_cloud = "member_images/" + str(emailTwo) + ".jpg"
                storage.child(path_on_cloud).put(pic)
                print("data has been created")
        except:
            print("went to except")
            flash("Please enter valid details")
            return render_template("CreateNewMember.html")
        return redirect(url_for("memberLogin"))
    else:
        return render_template("CreateNewMember.html")


@app.route('/createNewTrainer', methods=["POST", "GET"])
def createNewTrainer():
    if request.method == "POST":
        try:
            email = str(request.form["email"])
            print(email)
            pw = str(request.form["trainerpw"])
            print(pw)
            name = request.form["trainername"]
            print(name)
            number = request.form["contact"]
            print(number)
            gender = request.form["gender"]
            print(gender)
            description = request.form["description"]
            print(description)
            location = request.form["location"]
            print(location)
            experience = request.form["experience"]
            print(experience)
            trgtype = request.form["trgtype"]
            print(trgtype)
            # need to allow the users to click multiple values
            pricerange = request.form["pricerange"]
            print(pricerange)
            pic = request.files["picture"]
            print(pic)

            if len(pw) < 6:
                flash("Password too short please try a new one")
                return render_template("CreateNewTrainer.html")
            else:
                user = auth.create_user_with_email_and_password(email, pw)
                print("Successfully created an account")
                flash("Please go to your email to verify your account")
                auth.send_email_verification(user["idToken"])
                emailTwo = email.replace(".", "_DOT_")
                data = {"Email": emailTwo, "Name": name, "Number": number, "Location": location,
                        "Gender": gender, "Description": description, "Experience": experience, "Training Type": trgtype, "Price Range": pricerange}
                # rmb to try to create a range slider for the price range
                database.child("Trainers").child(emailTwo).set(data)
                path_on_cloud = "trainer_images/" + str(emailTwo) + ".jpg"
                storage.child(path_on_cloud).put(pic)
                print("data has been created")
        except:
            print("went to except")
            flash("Please enter valid details")
            return render_template("CreateNewTrainer.html")
        return redirect(url_for("trainerLogin"))
    else:
        return render_template("CreateNewTrainer.html")

# Details Pages


@app.route('/memberDetails', methods=["POST","GET"])
def memberDetails():
    if "username" and "userToken" in session:
        username = str(session["username"])
        user = session["userToken"]
        dict = database.child("Users").child(username).get()
        lst = []
        usernameTwo = username.replace("_DOT_", ".")
        for value in dict.val().values():
            if value == username:
                lst.append(usernameTwo)
            else:
                lst.append(value)
        print(lst)
        all_files = storage.list_files()
        for file in all_files:
            usernameTwo = "member_images/" + username + ".jpg"
            # only allow jpg files
            print(usernameTwo)
            if usernameTwo == file.name:
                print("there is a file with the same name")
                print(file.name)
                url = storage.child(file.name).get_url(user["idToken"])
                # need to deal w the case where the person has no profile image i think
                break
        oldEmail = request.form.get("oldEmail")
        print(oldEmail)
        newEmail = request.form.get("newEmail")
        print(newEmail)
        oldName = request.form.get("oldName")
        print(oldName)
        newName = request.form.get("newName")
        print(newName)
        oldNumber = request.form.get("oldNumber")
        print(oldNumber)
        newNumber = request.form.get("newNumber")
        print(newNumber)
        oldGender = request.form.get("oldGender")
        print(oldGender)
        newGender = request.form.get("newGender")
        print(newGender)
        oldTrgLvl = request.form.get("oldTrgLvl")
        print(oldTrgLvl)
        newTrgLvl = request.form.get("newTrgLvl")
        print(newTrgLvl)
        oldTrgType = request.form.get("oldTrgType")
        print(oldTrgType)
        newTrgType = request.form.get("newTrgType")
        print(newTrgType)
        dict = database.child("Users").child(username).get().val()
        valLst = []
        keyLst = []
        for key, value in dict.items():
            valLst.append(value)
            keyLst.append(key)
        print(keyLst)
        for key, value in dict.items():
            if oldEmail == value:
                database.child("Users").child(username).update({key: newEmail})
            elif oldName == value:
                database.child("Users").child(username).update({key: newName})
            elif oldNumber == value:
                database.child("Users").child(username).update({key: newNumber})
            elif oldGender == value:
                if newGender:
                    database.child("Users").child(username).update({key: newGender})
            elif oldTrgLvl == value:
                if newTrgLvl:
                    database.child("Users").child(username).update({key: newTrgLvl})
            elif oldTrgType == value:
                if newTrgType:                
                    database.child("Users").child(username).update({key: newTrgType})
    return render_template("MemberDetails.html", details=lst, profileImage = url, valDetails=valLst, keyDetails=keyLst)


@app.route('/trainerDetails', methods=["POST", "GET"])
def trainerDetails():
    if "username" and "userToken" in session:
        username = str(session["username"])
        user = session["userToken"]
        dict = database.child("Trainers").child(username).get()
        lst = []
        usernameTwo = username.replace("_DOT_", ".")
        for value in dict.val().values():
            if value == username:
                lst.append(usernameTwo)
            else:
                lst.append(value)
        print(lst)
        all_files = storage.list_files()
        for file in all_files:
            usernameTwo = "trainer_images/" + username + ".jpg"
            # only allow jpg files
            print(usernameTwo)
            if usernameTwo == file.name:
                print("there is a file with the same name")
                print(file.name)
                url = storage.child(file.name).get_url(user["idToken"])
                # need to deal w the case where the person has no profile image i think
                break

        oldEmail = request.form.get("oldEmail")
        print(oldEmail)
        newEmail = request.form.get("newEmail")
        print(newEmail)
        oldName = request.form.get("oldName")
        print(oldName)
        newName = request.form.get("newName")
        print(newName)
        oldNumber = request.form.get("oldNumber")
        print(oldNumber)
        newNumber = request.form.get("newNumber")
        print(newNumber)
        oldDescrip = request.form.get("oldDescrip")
        print(oldDescrip)
        newDescrip = request.form.get("newDescrip")
        print(newDescrip)
        oldExp = request.form.get("oldExp")
        print(oldExp)
        newExp = request.form.get("newExp")
        print(newExp)
        oldLocation = request.form.get("oldLocation")
        print(oldLocation)
        newLocation = request.form.get("newLocation")
        print(newLocation)
        oldGender = request.form.get("oldGender")
        print(oldGender)
        newGender = request.form.get("newGender")
        print(newGender)
        oldPriceRange = request.form.get("oldPriceRange")
        print(oldPriceRange)
        newPriceRange = request.form.get("newPriceRange")
        print(newPriceRange)
        oldTrgType = request.form.get("oldTrgType")
        print(oldTrgType)
        newTrgType = request.form.get("newTrgType")
        print(newTrgType)
        dict = database.child("Trainers").child(username).get().val()
        valLst = []
        keyLst = []
        for key, value in dict.items():
            valLst.append(value)
            keyLst.append(key)
        print(keyLst)
        for key, value in dict.items():
            if oldEmail == value:
                database.child("Trainers").child(username).update({key: newEmail})
            elif oldName == value:
                database.child("Trainers").child(username).update({key: newName})
            elif oldNumber == value:
                database.child("Trainers").child(username).update({key: newNumber})
            elif oldDescrip == value:
                database.child("Trainers").child(username).update({key: newDescrip})
            elif oldLocation == value:
                database.child("Trainers").child(username).update({key: newLocation})
            elif oldExp == value:
                if newExp:
                    database.child("Trainers").child(username).update({key: newExp})
            elif oldGender == value:
                if newGender:
                    database.child("Trainers").child(username).update({key: newGender})
            elif oldPriceRange == value:
                if newPriceRange:
                    database.child("Trainers").child(username).update({key: newPriceRange})
            elif oldTrgType == value:
                if newTrgType:                
                    database.child("Trainers").child(username).update({key: newTrgType})
    return render_template("TrainerDetails.html", details=lst, profileImage = url, valDetails=valLst, keyDetails=keyLst)

# Update Pages


# @app.route("/memberDetailUpdate", methods=["POST", "GET"])
# def memberDetailUpdate():
#     if "username" in session:
#         username = str(session["username"])
#         new = request.form.get("new")
#         print(new)
#         print(type(new))
#         old = request.form.get("old")
#         print(old)
#         print(type(old))
#         dict = database.child("Users").child(username).get().val()
#         valLst = []
#         keyLst = []
#         for key, value in dict.items():
#             valLst.append(value)
#             keyLst.append(key)
#         print(keyLst)
#         for key, value in dict.items():
#             if old == value:
#                 database.child("Users").child(username).update({key: new})
#                 flash("Please refresh page to see changes")
#                 break
#     return render_template("MemberDetailUpdate.html", valDetails=valLst, keyDetails=keyLst)


@app.route("/trainerDetailUpdate", methods=["POST", "GET"])
def trainerDetailUpdate():
    if "username" in session:
        username = str(session["username"])
        new = request.form.get("new")
        print(new)
        print(type(new))
        old = request.form.get("old")
        print(old)
        print(type(old))
        dict = database.child("Trainers").child(username).get().val()
        valLst = []
        keyLst = []
        for key, value in dict.items():
            valLst.append(value)
            keyLst.append(key)
        for key, value in dict.items():
            if old == value:
                database.child("Trainers").child(username).update({key: new})
                flash("Please refresh page to see changes")
                break
    return render_template("TrainerDetailUpdate.html", valDetails=valLst, keyDetails=keyLst)


@app.route("/logout")
def logout():
    if "username" in session:    
        flash(f"You have been logged out")
    session.pop("username", None)
    return redirect(url_for("homePage"))


# to take data out of database
# add in parsing or data pulling and settle what headers to display
# consider adding more but should be generic

@app.route('/filterTrainers', methods=['POST', 'GET'])
def filterTrainers():
    data = ()
    # to read all trainers
    trainers = database.child("Trainers").get()

    # to check if trainers are present in database
    if trainers.each():
        for i in trainers.each():
            headings = ()
            for head in i.val():
                headings += (head,)

        for i in trainers.each():
            personaldata = ()
            for a in i.val():
                personaldata += (i.val()[a],)
            data += (personaldata,)

        # to check if trainers are being filtered
        if request.method == 'POST':
            gender = request.form.getlist("gender")
            location = request.form.getlist("location")
            price = request.form.getlist("price")
            trgtype = request.form.getlist("trgtype")

            data1 = ()
            # to read data
            for i in trainers.each():
                personaldata = ()
                if gender == [] or i.val()['Gender'] in gender:
                    if location == [] or i.val()['Location'] in location:
                        # if (i.val()['Price'] == [] or i.val()['Gender'] in trgtype):
                        if trgtype == [] or i.val()['Training Type'] in trgtype:
                            for a in i.val():
                                personaldata += (i.val()[a],)
                if personaldata:
                    data1 += (personaldata,)
            if data1:
                return render_template("FilterTrainers.html", headings=headings, data=data1)
            else:
                flash("No such trainer exists. Please try again!")
                return render_template("FilterTrainers.html")
        return render_template("FilterTrainers.html", headings=headings, data=data)
    else:
        flash("No trainers in the database!")
        return render_template("FilterTrainers.html")

if __name__ == "__main__":
    app.run()

# email = input("Please enter your email\n")

# password = input("Please enter your password\n")

# user = auth.create_user_with_email_and_password(email, password)

# user = auth.sign_in_with_email_and_password(email, password)

# auth.send_password_reset_email(email)

# auth.send_email_verification(user["idToken"])

# print(auth.get_account_info(user["idToken"]))
