#!flask/bin/python
from flask import Flask, jsonify 
from flask import Flask, flash, redirect, render_template, request, session, abort, make_response, Markup 
from flask_httpauth import HTTPBasicAuth
from users import User
import re

#create an object of HTTPBasicAuth
auth=HTTPBasicAuth()




app = Flask(__name__)
app.secret_key = "superdooper1"
users = [
    {
        'userID': 1,
        'fname': 'sue',
        'lname': 'smith',
        'uname': 'sue', 
        'email': 'sue@outlook.com',
        'pwd': 'sue',
        'cpwd' :'sue'

    },
    {
        'userID': 2,
        'fname': 'sam',
        'lname': 'smith',
        'uname': 'sam', 
        'email': 'sam@outlook.com',
        'pwd': 'sam'
    }
]


events = [
    {
        'eventName': 'Coke studio Africa',
        'eventID': 1,
        'location': 'Nairobi', 
        'date': '12-13-2017'

    },
    {
        'eventName': 'Don Moen concert',
        'eventID': 2,
        'location': 'Citam', 
        'date': '11-12-2017'

    }
]
guests=[{
    'uname':'John',
    'email':'smiles@gmail.com',
    'userID':77,
    'eventID':1

}

]
#/////////////////////////USER SIDE////////////////////////////

#Function to create a new user
@app.route('/brightEvents/api/v1/auth/register', methods=['GET', 'POST'])
def create_users():
    if request.method == 'POST':
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        uname=request.form.get('uname')
        email=request.form.get('email')
        pwd=request.form.get('pwd')
        cpwd=request.form.get('cpwd')
        #checking if there's any empty fields
        if not fname or not lname or not uname or not email or not pwd :
            flash("All form fields must be filled ")
            return render_template('user_registration.html')
        #elif not re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email):
                #flash("Enter a valid email address") 
        elif len(pwd) <= 7 or len(cpwd) <= 7 :
                flash("Password length too small. Enter at least 8 characters")
                return render_template('user_registration.html')
        elif pwd!=cpwd:
            flash("Passwords don't match!")
            return render_template('user_registration.html')

        

       # user=User(fname, lname, uname, email, pwd)

        user = {
            'userID': users[-1]['userID'] + 1,
            'fname': fname,
            'lname': lname,
            'uname': uname,
            'email': email,
            'pwd': pwd,
            
    }
        users.append(user)
        flash('Thanks for signing up please login')
        return render_template('user_login.html')
        #return jsonify(users), 201
    return render_template('user_registration.html')
   
        


#Function to get the user login details and user login form if they are correct
@app.route('/brightEvents/api/v1/auth/login', methods=['GET','POST'])
#@auth.login_required
@auth.get_password
def getLoginDetails():
    if request.method == 'POST':
        user = [user for user in users if user['uname'] == request.form['uname'] and user['pwd'] == request.form['pwd']]
        if len(user) >= 1:
            session['logged_in'] = True
            return home()
        else:
            flash('Wrong username or password')
        return render_template('user_login.html')
    return render_template('user_login.html')


#Function to access the home page
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('events.html', result=events)
    else:
        return render_template('index.html')  
             
   

# make a better eror 401 response
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized!Incorrect username or password'}), 401)



   
#The logout Function
@app.route('/brightEvents/api/v1/auth/logout')
def user_logout():
    session['logged_in'] = False
    return home()


#The Reset Password Function
@app.route('/brightEvents/api/v1/reset-password', methods=['GET', 'POST'])
def reset_password():
    if



    #////////////////////EVENTS SIDE/////////////////////////////////
    
#Functions to create new events
@app.route('/brightEvents/api/v1/events', methods=['GET','POST'])
def create_events():
    if request.method == 'POST':
        eventName = request.form['eventName']
        location= request.form['location']
        date = request.form['date']
        if not eventName or not location or not date:
            message = Markup("All fields must be filled")
            flash(message)
            return render_template('index.html'), 400
        
        
        event={
            'eventID': events[-1]['eventID'] + 1,
            'eventName':eventName ,
            'location':location ,
            'date': date
        }
        events.append(event)
        flash('Event added successfully')
        return render_template('userEvents.html', result=events)
        #return jsonify(events), 201 -----would apply if the api was not connected to the templates
    return get_allEvents()




#Function to get all the events
@app.route('/brightEvents/api/v1/events',methods=['GET'])
def get_allEvents():
    return render_template('userEvents.html', result= events) 
    #return jsonify(events), 201 --. would apply if the api was not connected to the templates

    

# Function to the get event based on the ID
@app.route('/brightEvents/api/v1/events/<int:eventID>', methods=['GET'])
def get_event(eventID):
    event = [event for event in events if event['eventID'] == eventID]
    if len(event) == 0:
        abort(404)
    results=[]
    results.append(event)
    #return jsonify(results)
    return render_template('userEvents.html', result=results)

#creating a much better error 404 response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}), 404)

#Function to update an event
@app.route('/brightEvents/api/v1/events/<int:eventID>', methods=['PUT'])
def update_event(eventID):
    event = [event for event in events if event['eventID'] == eventID]
    if len(event) == 0:
        abort(404)
    #if type(request.form['eventName']) is not str:
        #abort(400)
    #if type(request.form['location']) is not str:
        #abort(400)
    
    event[0]['eventName'] = request.form.get('eventName', event[0]['eventName'])
    event[0]['location'] = request.form.get('location', event[0]['location'])
    event[0]['date'] = request.form.get('date', event[0]['date'])
    #return jsonify({'event': event[0]})
    return jsonify(events)



#creating a much better error 400 response
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'Error': 'Details entered are incorrect'}), 400)

#Function to delete an event based on the ID
@app.route('/brightEvents/api/v1/events/<int:eventID>', methods=['DELETE'])
def delete_event(eventID):
    event = [event for event in events if event['eventID'] == eventID]
    if len(event) == 0:
        #abort(404)
        return jsonify({'message': 'Event specified does not exist'}), 404
    event.remove(event[0])
    #return jsonify({'result': True})
    return jsonify(events)


#Function to rsvp to an event
@app.route('/brightEvents/api/v1/events/<int:eventID>/rsvp', methods=['GET','POST'])
def rsvp(eventID):
    if request.method == 'POST':
        if session['logged_in'] == True:
            uname=session['uname']
            user = [user for user in users if user['uname'] == uname]
            if len(user) == 0:
                abort(404)
            for i in user:
                eventID=event['eventID']
                uname=user['uname']
                email=user['email']
                userID=user['userID']
            guest={
                'eventID':eventID,
                'uname' :uname,
                'email' :email,
                'userID':userID
            }
            guests.append(guest)
            return 'You have sent your rsvp'
            return render_template('events.html', result=events)
        else:
            eventID=event['eventID']
            uname=request.form['uname']
            email=request.form['email']
            
            guest={
                'eventID':eventID,
                'uname' :uname,
                'email' :email,
                'userID':users[-1]['userID'] + 1
            }
            guests.append(guest)
            return 'You have sent your rsvp'
            return jsonify(guests)
            #return render_template('events.html', result=events)
    ###GET##
    else:
        return render_template('rsvp.html')
    

   
    # The main method
if __name__ == '__main__':
    app.run(debug=True)
    