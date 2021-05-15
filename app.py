from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json
import uuid
import time
# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')
# Choose database
db = client['InfoSys']
# Choose collections
students = db['Students']
users = db['Users']
# Initiate Flask App
app = Flask(__name__)
users_sessions = {}
def create_session(username):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (username, time.time())
    return user_uuid  
def is_session_valid(user_uuid):
    return user_uuid in users_sessions





# ΕΡΩΤΗΜΑ 1: Δημιουργία χρήστη -----------------------------------------------------------------------------------------
@app.route('/createUser', methods=['POST'])
def create_user():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")


    if users.find({"username":data["username"]}).count() == 0 :
        user = {"username": data["username"], "password": data["password"]}
        users.insert_one(user)
        return Response(data["username"]+" was added to the MongoDB", status=200, mimetype='application/json')
    else:
        return Response("User already exists.", status=400)





# ΕΡΩΤΗΜΑ 2: Login στο σύστημα -----------------------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    # find the user we added to the 'users' collection - if username and password match --> user is authenticated 
    if users.find_one({"$and":[{"username":data["username"]}, {"password":data["password"]}]}):
        user_uuid = create_session(data["username"])
        res = {"uuid": user_uuid, "username": data["username"]}
        return Response("Authentication successful." + json.dumps(res), mimetype='application/json', status=200)
    else:
        return Response("Wrong username or password.", status=400, mimetype='application/json')





# ΕΡΩΤΗΜΑ 3: Επιστροφή φοιτητή βάσει email -----------------------------------------------------------------------------
@app.route('/getStudent', methods=['GET'])
def get_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    # if the flag is true --> authentication successful --> continue with code inside the if statement
    uuid = request.headers.get('authorization')
    flag = is_session_valid(uuid)
    
    if flag:
        # using the 'find' method to find a student depending on the email the user gives
        student = students.find_one({"email":data["email"]})
        if student != None:
            student['_id'] = None
            return Response("User authenticated and student found: " + json.dumps(student), status=200, mimetype='application/json')
        else:
            return Response("Student doesn't exist.")
    else:
        return Response("User not authenticated.", status=401, mimetype='application/json')





# ΕΡΩΤΗΜΑ 4: Επιστροφή όλων των φοιτητών που είναι 30 ετών ------------------------------------------------------------
@app.route('/getStudents/thirties', methods=['GET'])
def get_students_thirty():

    # if the flag is true --> authentication successful --> continue with code inside the if statement
    uuid = request.headers.get('authorization')
    flag = is_session_valid(uuid)

    if flag:
        # using the 'find_one' method we find students whose birth date is equal to 1991
        temp = students.find({"yearOfBirth":{'$eq':1991}})
        student_list = []
        for student in temp:
            student['_id'] = None
            student_list.append(student)
        if student_list != None:
            return Response(json.dumps(student_list), status=200, mimetype='application/json')
        else:
            return  Response("There aren't any 30-year-old students")
    else:
        return Response("User not authenticated.", status=401, mimetype='application/json')





# ΕΡΩΤΗΜΑ 5: Επιστροφή όλων των φοιτητών που είναι τουλάχιστον 30 ετών -------------------------------------------------
@app.route('/getStudents/oldies', methods=['GET'])
def get_oldies():

    # if the flag is true --> authentication successful --> continue with code inside the if statement
    uuid = request.headers.get('authorization')
    flag = is_session_valid(uuid)

    if flag:
        # using the 'find_one' method we find students whose birth date is less or equal to 1991
        temp = students.find({"yearOfBirth":{'$lte':1991}})
        student_list = []
        for student in temp:
            student['_id'] = None
            student_list.append(student) # inserting the student in the student_list
        if student_list != None:
            return Response(json.dumps(student_list), status=200, mimetype='application/json')
        else:
            return  Response("There aren't any 30-year-old students, or older")
    else:
        return Response("User not authenticated.", status=401, mimetype='application/json')





# ΕΡΩΤΗΜΑ 6: Επιστροφή φοιτητή που έχει δηλώσει κατοικία βάσει email --------------------------------------------------
@app.route('/getStudentAddress', methods=['GET'])
def get_student_address():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    # if the flag is true --> authentication successful --> continue with code inside the if statement
    uuid = request.headers.get('authorization')
    flag = is_session_valid(uuid)

    if flag:
        # finding a student based on email address and email, we need the $ne because we need for the address to not equal to None
        student = students.find_one({"$and":[{"address":{"$ne":None}}, {"email":data["email"]}]})
        if student != None:
            student = {"name":student["name"], "address":student["address"]}
            return Response("User authenticated and the student is: " + json.dumps(student), status=200, mimetype='application/json')
        else:
            return Response("Student doesn't exist.")
    else:
        return Response("User not authenticated.", status=401, mimetype='application/json')





# ΕΡΩΤΗΜΑ 7: Διαγραφή φοιτητή βάσει email ------------------------------------------------------------------------------
@app.route('/deleteStudent', methods=['DELETE'])
def delete_student():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    # if the flag is true --> authentication successful --> continue with code inside the if statement
    uuid = request.headers.get('authorization')
    flag = is_session_valid(uuid)

    if flag:
        # usig the 'find_one' method to find a student depending on their email 
        student = students.find_one({"email":data["email"]})
        if student != None:
            student_name = student["name"]
            msg = {"Student " + student_name + " was successfully deleted"}
            students.delete_one(student)
            return Response(msg, status=200, mimetype='application/json')
        else:
            return Response("Student doesn't exist.")
    else:
        return Response("User not authenticated.", status=401, mimetype='application/json')





# ΕΡΩΤΗΜΑ 8: Εισαγωγή μαθημάτων σε φοιτητή βάσει email -----------------------------------------------------------------
@app.route('/addCourses', methods=['PATCH'])
def add_courses():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data or not "courses" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    # if the flag is true --> authentication successful --> continue with code inside the if statement
    uuid = request.headers.get('authorization')
    flag = is_session_valid(uuid)

    if flag:
        student = students.find_one({"email":data["email"]})
        if student != None:
            student = students.update_one({"email":data["email"]}, 
            {"$set":
                {
                    "courses":data["courses"]
                }
            })
            return Response("Courses added.", status=200, mimetype='application/json')
        else:
            return Response("Student doesn't exist.")
    else:
        return Response("User not authenticated.", status=401, mimetype='application/json')


"""         
        {
            email: "an email",
            courses: [
                {'course 1': 10, 
                {'course 2': 3 }, 
                {'course 3': 8},
                ...
            ]
        } 
"""





# ΕΡΩΤΗΜΑ 9: Επιστροφή περασμένων μαθημάτων φοιτητή βάσει email ----------------------------------------------------------
@app.route('/getPassedCourses', methods=['GET'])
def get_courses():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "email" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")
    
    # if the flag is true --> authentication successful --> continue with code inside the if statement
    uuid = request.headers.get('authorization')
    flag = is_session_valid(uuid)
    if flag:
        # given a student's email and the fact that their courses aren't None
        student = students.find_one({"$and":[{"email":data["email"]}, {"courses":{"$ne":None}}]})
        if student != None:
            student['_id'] = None
            courses={"courses":student["courses"]}
            student={}
            # for loops to get the course grades
            for course in courses.values():
                for item in course:
                    for grade in item:
                        if item.get(grade)>=5:
                            student[grade]=item.get(grade)
            return Response("The student has passed the following courses: " + json.dumps(student), status=200, mimetype='application/json')
        else:
            return Response("Student doesn't exist or doesn't have any courses.")
    else:
        return Response("User not authenticated.", status=401, mimetype='application/json')

"""    
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό 
        του στο σύστημα.

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή.
        * Στη περίπτωση που ο φοιτητής έχει βαθμολογία σε κάποια μαθήματα, θα πρέπει να επιστρέφεται το όνομά του (name) 
          καθώς και τα μαθήματα που έχει πέρασει.
        * Στη περίπτωη που είτε ο φοιτητής δεν περάσει κάποιο μάθημα, είτε δεν υπάρχει φοιτητής με αυτό το email 
          στο σύστημα, 
          να επιστρέφεται μήνυμα λάθους.
        
        Αν υπάρχει όντως ο φοιτητής με βαθμολογίες σε κάποια μαθήματα, να περάσετε τα δεδομένα του σε 
        ένα dictionary που θα ονομάζεται student.
        Το dictionary student θα πρέπει να είναι της μορφής: student = {"course name 1": X1, "course name 2": X2, ...}, 
        όπου X1, X2, ... οι βαθμολογίες (integer) των μαθημάτων στα αντίστοιχα μαθήματα.
    

    # Η παρακάτω εντολή χρησιμοποιείται μόνο σε περίπτωση επιτυχούς αναζήτησης φοιτητή 
    # (υπάρχει ο φοιτητής και έχει βαθμολογίες στο όνομά του).
    return Response(json.dumps(student), status=200, mimetype='application/json')
"""
# Εκτέλεση flask service σε debug mode, στην port 5000. 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
