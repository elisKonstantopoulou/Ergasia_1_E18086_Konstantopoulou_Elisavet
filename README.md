# Ergasia_1_E18086_Konstantopoulou_Elisavet
Στην 1η Υποχρεωτική Εργασία στο μάθημα Πληροφοριακά Συστήματα κληθήκαμε να υλοποιήσουμε εννέα endpoints με τα οποία εκτελούμε ενέργειες πάνω σε μια βάση **MongoDB**. Να σημειωθεί ότι η εργασία υλοποιήθηκε σε περιβάλλον **Ubuntu 20.04** και η επεξεργασία του Python script στον **Visual Studio Code** editor. Μετά από μια σύντομη επεξήγηση του κώδικα θα ακολουθεί ένα screenshot της terminal εντολής για την υλοποίηση του εκάστιτε endpoint και τα αποτελέσματα. 

# Αρχικά Στάδια
Παρακάτω εμφανίζονται οι εντολές του terminal που εκτελέστηκαν για την **δημιουργία του 'mongodb' Docker container** και του **virtual environment**.
```bash
sudo apt-get update 
sudo systemctl enable docker --now 
sudo usermod -aG docker $elisavetk
sudo docker pull mongo
sudo docker run -d -p 27017:27017 --name mongodb mongo
sudo docker ps -a
sudo docker start mongodb
sudo docker exec -it mongodb mongo
sudo docker cp students.json mongodb:/students.json
sudo docker exec -it mongodb mongoimport --db=InfoSys --collection=Students --file=students.json
sudo docker start mongodb
sudo apt install python3-pip
pip install flask
pip install virtualenv
virtualenv v
source /home/elisavet/v/bin/activate activate
pip install pymongo
python3 app.py
```
<img src="/terminal_screenshots/00.png" width=60%>

# Python Script 
## ENDPOINT 1
```python
if users.find({"username":data["username"]}).count() == 0 :
        user = {"username": data["username"], "password": data["password"]}
        users.insert_one(user)
        return Response(data["username"]+" was added to the MongoDB", status=200, mimetype='application/json')
    else:
        return Response("User already exists.", status=400)
```
Στο παραπάνω κομμάτι κώδικα ελέγχουμε εαν ο συνδυασμός του *username* και *password* που δεχτήκαμε υπάρχει στην βάση. Εαν όχι, τότε δημιουργούμε έναν καινούριο user με τα αντίστοιχα credentials και τον εισάγουμε στους 'users'.

<img src="/terminal_screenshots/01.png" width=150%>

Πριν τραβηχτεί το screenshot αυτό ο χρήστης **_elli_** υπήρχε ήδη, επομένως εμφανίζεται το μήνυμα *User already exists*. Παρακάτω δημιουργούμε καινούριο χρήστη με το όνομα **_ellik_** και βλέπουμε ότι προστέθηκε επιτυχώς στους **'users'**.

## ENDPOINT 2
```python
if users.find_one({"$and":[{"username":data["username"]}, {"password":data["password"]}]}):
        user_uuid = create_session(data["username"])
        res = {"uuid": user_uuid, "username": data["username"]}
        return Response("Authentication successful." + json.dumps(res), mimetype='application/json', status=200)
    else:
        return Response("Wrong username or password.", status=400, mimetype='application/json')
```
Με την μέθοδο **find_one()** αναζητούμε το ζεύγος *username*-*password* που εισήγαγε ο χρήστης και στην περίπτωση που υπάρχει αντιστοίχηση επιστρέφεται το ανίστοιχο μήνμα, καθως και το **user id _(uuid)_** το οποίο θα χρησιμοποιεί ο χρήστης για να εκτελεί τα επόμενα endpoints. Η **find_one()** θα χρησιοποιηθεί και σε επόμενα ερωτήματα, παίρνοντας ως ορίσματα τα πεδία που χρειάζονται κάθε φορά.

<img src="/terminal_screenshots/02.png" width=150%>

Εάν από εδώ και στο εξής ο χρήστης δεν χρησιμοποιεί το αναγραφόμενο **_uuid_** για να αυθεντικοποιηθεί θα εμφανιστεί το μήνυμα *User not authenticated*, όπως φαίνεται στο παρακάτω screenshot όταν έγινε προσπάθεια εμφάνισης μαθητή με λάθος **_uuid_**.

<img src="/terminal_screenshots/user_not_authenticated.png" width=150%>

## ENDPOINT 3
```python
uuid = request.headers.get('authorization')
flag = is_session_valid(uuid)

if flag:
   ...
```
Η παραπάνω εντολές θα χρησιμοποιηθούν σε όλα τα υπόλοιπα endpoints διότι αυτές αυθεντικοποιούν τον χρήστη. 
```python
student = students.find_one({"email":data["email"]})
```
Χρησιμοποιείται πάλι η μέθοδος **find_one()** με όρισμα αυτή τη φορά το *email* που έδωσε ο χρήστης.

<img src="/terminal_screenshots/03.png" width=150%>

## ENDPOINT 4
```python
temp = students.find({"yearOfBirth":{'$eq':1991}})
student_list = []
for student in temp:
   student['_id'] = None
   student_list.append(student)
   if student_list != None:
      return Response(json.dumps(student_list), status=200, mimetype='application/json')
   else:
       return  Response("There aren't any 30-year-old students")
```
Το έτος γέννησης πρέπει να είναι το 2021-30=1991 και για αυτό χρησιμοποιείται το **_'$eq':1991_** για την εισαγωγή μαθητών στην λίστα *student_list*. Όσοι ικανοποίησαν το παραπάνω κριτήριο θα εισαχθούν στην *student_list*.

<img src="/terminal_screenshots/04.png" width=150%>

## ENDPOINT 5
Στο συγκεκριμένο endpoint το μόνο που αλλάζει είναι ότι το **_'$eq':1991_** γίνεται **_'$lte':1991_** που σημαίνει **_less than or equal_**.

<img src="/terminal_screenshots/05.png" width=150%>

*Σημείωση: τα ονόματα που εμφανίζει είναι περισσότερα από αυτά που φαίνονται στο screenshot, απλώς για λόγους συντομίας συμπεριλήφθηκε μόνο ένα κομμάτι τους.*

## ENDPOINT 6
```python
student = students.find_one({"$and":[{"address":{"$ne":None}}, {"email":data["email"]}]})
```
Το παραπάνω κομμάτι αξίζει να αναφερθεί καθώς τα κριτήρια μέσα στην μέθοδο είναι ελαφρώς διαφορετικά καθώς έγινε η χρήση του **_"$and"_** για χάρη της σύζευξης και του **_"$ne"_** για να βεβαιωθούμε ότι επιστρέφονται μαθητής που έχει δηλώσει διεύθυνση (**_address not equal to None_**).

<img src="/terminal_screenshots/06.png" width=150%>

Σε περίπτωση που εισάγουμε *email* μαθητή που δεν έχει κατοικία:

<img src="/terminal_screenshots/06_no_address.png" width=150%>

## ENDPOINT 7
```python
if student != None:
   student_name = {"name":data["name"]}
   msg = {"Student " + student_name + " was successfully deleted"}
   students.delete_one(student)
   return Response(msg, status=200, mimetype='application/json')
else:
    return Response("Student doesn't exist.")
```
Με την ίδια **_find_one()_** εντολή όπως και στο ENDPOINT 3 αναζητούμε έναν μαθητή με βάση το *email* του και χρησιμοποιούμε την μέθοδο **_delete_one()_** τον διαγράφουμε. Γίνεται και χρήση ενός **_msg_** όπως ζητήθηκε στην εκφώνηση.

<img src="/terminal_screenshots/07.png" width=150%>

## ENDPOINT 8
```python
student = students.update_one({"email":data["email"]}, 
{"$set":
   {
      "courses":student["courses"]
   }
})
return Response("Courses added.", status=200, mimetype='application/json')
```
Με την χρήση της μεθόδου **_update_one()_** προσθέτουμε, κατά μια έννοια, courses σύμφωνα με τον τρόπο που αναγράφεται στην εκφώνηση.

<img src="/terminal_screenshots/08.png" width=150%>

## ENDPOINT 9
```python
for course in courses.values():
   for item in course:
      for grade in item:
         if item.get(grade)>=5:      
            student[grade]=item.get(grade)
            return Response("The student has passed the following courses: " + json.dumps(student), status=200, mimetype='application/json')
```
Το αξιοσημείωτο στο ENDPOINT 9  είναι τα *nested for loops*, καθώς η συνθήκη για να εκτελεστεί ο παραπάνω κώδικας είναι αρχικά η αυθεντικοποίηση του χρήστη και μετά η αντίστοιχη εντολή **_find_one()_** του ENDPOINT 6, απλά με τα ορίσματα *{"email":data["email"]}* και *{"courses":{"$ne":None}}*. 

Ο στόχος ήταν να **απομονώσουμε** το κάθε μάθημα με τις προσπελάσεις αυτές και να πάρουμε μόνο τον βαθμό για να τον συγκρίνουμε με το 5. Εάν ο βαθμός είναι μεγαλύτερος ή ίσος του 5, τότε το μάθημα είναι περασμένο και όλο το αντίστοιχο course (όνομα μαθήματος & βαθμός) περνάει στον πίινακα student. 
Τέλος εμφανίζουμε τον πίνακα student.

<img src="/terminal_screenshots/09.png" width=150%>
