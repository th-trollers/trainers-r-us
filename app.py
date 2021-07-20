from os import path
import pyrebase
from flask import *
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from flask_socketio import SocketIO, join_room, leave_room
from requests.api import get

app = Flask(__name__, template_folder="html")
app.secret_key = "trainersrus"
socketio = SocketIO(app)
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
            session["check"] = "User"
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
            session["check"] = "Trainer"
            return redirect(url_for("trainerHome"))
        except:
            flash(unsuccessful)
            print(unsuccessful)
            return redirect(url_for("trainerLogin"))
    return render_template("TrainerLogin.html")

# Member and Trainer Home Page


@app.route('/memberHome', methods=["POST", "GET"])
def memberHome():
    return render_template("MemberHome.html")


@app.route('/trainerHome', methods=["POST", "GET"])
def trainerHome():
    if "username" in session:
        print("username in session")
        username = str(session["username"])
        flash("Welcome trainer " +
              database.child("Trainers").child(username).get().val()["Name"])
    return render_template("TrainerHome.html")


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
                data = {"Email": emailTwo, "Name": name, "Number": number,
                        "Gender": gender, "Training Level": trglvl, "Training Type": trgtype}
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


# @app.route("/trainerDetailUpdate", methods=["POST", "GET"])
# def trainerDetailUpdate():
#     if "username" in session:
#         username = str(session["username"])
#         new = request.form.get("new")
#         print(new)
#         print(type(new))
#         old = request.form.get("old")
#         print(old)
#         print(type(old))
#         dict = database.child("Trainers").child(username).get().val()
#         valLst = []
#         keyLst = []
#         for key, value in dict.items():
#             valLst.append(value)
#             keyLst.append(key)
#         for key, value in dict.items():
#             if old == value:
#                 database.child("Trainers").child(username).update({key: new})
#                 flash("Please refresh page to see changes")
#                 break
#     return render_template("TrainerDetailUpdate.html", valDetails=valLst, keyDetails=keyLst)


@app.route("/logout")
def logout():
    flash(f"You have been logged out")
    session.pop("username", None)
    session.pop("userToken", None)
    session.pop("check", None)
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
            print(gender)
            location = request.form.getlist("location")
            print(location)
            price = request.form.getlist("pricerange")
            print(price)
            trgtype = request.form.getlist("trgtype")
            print(trgtype)

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
                print(headings)
                print(data1)
                return render_template("FilterTrainers.html", headings=headings, data=data1)
            else:
                flash("No such trainer exists. Please try again!")
                return render_template("FilterTrainers.html")
        print(headings)
        print(data)
        return render_template("FilterTrainers.html", headings=headings, data=data)
    else:
        flash("No trainers in the database!")
        return render_template("FilterTrainers.html")


# booking module --------------------------------------------------------------------------

@app.route("/bookings")
def bookings():
    return render_template("Bookings.html")


# chat functions--------------------------------------------------------------------------------

# get trainer info from his username (returns tuple of info)
def get_trainer(email):
    print("getting trainer")
    print(email)
    trainer = ()
    trainers = database.child("Trainers").get()
    if trainers.each():
        for i in trainers.each():
            if email == i.val()["Email"]:
                for a in i.val():
                    trainer += (i.val()[a],)
        if trainer:
            return trainer
        else:
            return None
    else:
        return None


# to check whether chat between trainer and user exists and return messages
# if it does exist return messages
def check_chats(user, trainer):
    print("checking chats")
    chats = database.child("Chats").get()
    messages = ()
    store = ()
    newstore = ()
    boolean = False
    if chats.each():
        for i in chats.each():

            if session["check"] == "User":
                if user == i.val()["Username"]:
                    if trainer == i.val()["Trainer"]:
                        boolean = True
                        keys = list(i.val().keys())
                        if "Messages" in keys:
                            for a in i.val()["Messages"]:
                                msg = ()
                                msg += (i.val()
                                        ["Messages"].get(a).get("Content"),)
                                msg += (i.val()
                                        ["Messages"].get(a).get("Sender"),)
                                msg += (i.val()
                                        ["Messages"].get(a).get("Date"),)
                                if len(a) < 10:
                                    messages += (msg,)
                                elif len(a) == 10:
                                    store += (msg,)
                                else:
                                    newstore += (msg,)
                            if store:
                                for x in store:
                                    messages += (x,)
                            if newstore:
                                for y in newstore:
                                    messages += (y,)
                            return messages
                        else:
                            return "No messages"

            if session["check"] == "Trainer":
                if user == i.val()["Trainer"]:
                    if trainer == i.val()["Username"]:
                        boolean = True
                        keys = list(i.val().keys())
                        if "Messages" in keys:
                            for a in i.val()["Messages"]:
                                msg = ()
                                msg += (i.val()
                                        ["Messages"].get(a).get("Content"),)
                                msg += (i.val()
                                        ["Messages"].get(a).get("Sender"),)
                                msg += (i.val()
                                        ["Messages"].get(a).get("Date"),)
                                if len(a) < 10:
                                    messages += (msg,)
                                elif len(a) == 10:
                                    store += (msg,)
                                else:
                                    newstore += (msg,)
                            if store:
                                for x in store:
                                    messages += (x,)
                            if newstore:
                                for y in newstore:
                                    messages += (y,)
                            return messages
                        else:
                            return "No messages"
        if boolean == False:
            return None
    else:
        return None


# to check room number of room
def check_roomnum(user, trainer):
    print("checking room num")
    chats = database.child("Chats").get()
    if chats.each():
        if session["check"] == "User":
            for i in chats.each():
                if user == i.val()["Username"]:
                    if trainer == i.val()["Trainer"]:
                        return i.val()["Room Number"]
        else:
            for i in chats.each():
                if user == i.val()["Trainer"]:
                    if trainer == i.val()["Username"]:
                        return i.val()["Room Number"]
    else:
        return None


# given user's email return his name for display
def get_user_name(email):
    users = database.child("Users").get()
    if users.each():
        for i in users.each():
            if email == i.val()["Email"]:
                return i.val()["Name"]
    else:
        return None


# get all chats for user/trainer (returns tuple of emails with whom user has existing chat history)
def get_chat(username):
    print("getting chat")
    print(username)
    chats = database.child("Chats").get()
    if chats.each():
        chat = ()
        for i in chats.each():
            if username == i.val()["Username"]:
                print("useracc found")
                keys = list(i.val().keys())
                if "Messages" in keys:
                    chat += (i.val()["Trainer"],)
            elif username == i.val()["Trainer"]:
                print("trainer acc found")
                keys = list(i.val().keys())
                if "Messages" in keys:
                    chat += (i.val()["Username"],)
        if chat:
            print(chat)
            return chat
        else:
            return None
    else:
        return None


# to save message into database permanently
def save_msg(room, message, sender, date):
    chats = database.child("Chats").get()
    print("trying to save msg")
    if chats.each():
        for i in chats.each():
            if room == i.val()["Room Number"]:
                print("found room")
                print(room)
                msgs = database.child("Chats").child(
                    room).child("Messages").get()
                index = 0
                if msgs.each():
                    for i in msgs.each():
                        index += 1
                counter = index + 1
                msgname = "Message " + str(counter)
                msg = {"Content": message, "Sender": sender, "Date": date}
                database.child("Chats").child(room).child(
                    "Messages").child(msgname).set(msg)


# to view individual trainer info
@app.route('/trainers/<trainer_email>/')
def viewtrainerprofile(trainer_email):
    trainer = get_trainer(trainer_email)
    if trainer:
        return render_template('ViewTrainer.html', trainer=trainer)
    else:
        return "Trainer not found", 404


@app.route('/viewChat')
def viewChat():
    if "username" in session:
        email = request.args.get("email")
        if session["check"] == "User":
            print("user logged in")
            trainer = get_trainer(email)
            trainername = trainer[5]
            username = str(session["username"])
            name = get_user_name(username)
            test = check_chats(username, email)

            roomnum = check_roomnum(username, email)
            if test:
                if test == "No messages":
                    return render_template('ViewChat.html', username=name, room=roomnum, trainer=trainername)
                else:
                    return render_template("ViewChat.html", username=name, room=roomnum, messages=test, trainer=trainername)
            else:
                # if not open new chat room
                chats = database.child("Chats").get()
                index = 0
                for i in chats.each():
                    index += 1
                counter = index + 1
                roomname = "Room " + str(counter)
                data = {"Username": username,
                        "Trainer": email, "Room Number": roomname}
                database.child("Chats").child(roomname).set(data)
                return render_template('ViewChat.html', username=name, room=roomname, trainer=trainername)
        else:
            # trainer logged in
            print("trainer logged in")
            trainer = str(session["username"])
            username = get_user_name(email)
            test = check_chats(trainer, email)
            roomnum = check_roomnum(trainer, email)
            trainertuple = get_trainer(trainer)
            trainername = trainertuple[5]
            if test:
                if test == "No messages":
                    return render_template('TrainerViewChat.html', username=trainername, room=roomnum, trainer=username)
                else:
                    return render_template("TrainerViewChat.html", username=trainername, room=roomnum, messages=test, trainer=username)
            else:
                # if not open new chat room
                print("no existing room")
                chats = database.child("Chats").get()
                index = 0
                for i in chats.each():
                    index += 1
                counter = index + 1
                roomname = "Room " + str(counter)
                data = {"Username": email, "Trainer": trainer,
                        "Room Number": roomname}
                database.child("Chats").child(roomname).set(data)
                return render_template('TrainerViewChat.html', username=trainername, room=roomname, trainer=username)
    else:
        return render_template("HomePage.html")


@app.route('/allChats')
def allChats():
    if "username" in session:
        username = str(session["username"])
        print("trying to find all chats")
        chat_hist = get_chat(username)
        names = ()
        if session["check"] == "User":
            print("logged in as user")
            for chat in chat_hist:
                names += (get_trainer(chat)[5],)
        else:
            print("logged in as trainer")
            for chat in chat_hist:
                names += (get_user_name(chat),)
        combined = ()
        index = 0
        for i in chat_hist:
            combined += (((chat_hist[index]), (names[index])),)
            index += 1
        return render_template("AllChats.html", chats=combined)
    else:
        return render_template("HomePage.html")


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    save_msg(data['room'], data['message'],
             data['username'], data['created_at'])
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(
        data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(
        data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


if __name__ == "__main__":
    # app.run()
    socketio.run(app, debug=True)

# email = input("Please enter your email\n")

# password = input("Please enter your password\n")

# user = auth.create_user_with_email_and_password(email, password)

# user = auth.sign_in_with_email_and_password(email, password)

# auth.send_password_reset_email(email)

# auth.send_email_verification(user["idToken"])

# print(auth.get_account_info(user["idToken"]))
