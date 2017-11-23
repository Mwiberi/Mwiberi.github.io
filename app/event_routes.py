#!flask/bin/python
from flask import Flask, jsonify 
from flask import abort
from flask import request
from flask import make_response


app = Flask(__name__)

events = [
    {
        'eventName': 'Coke studio Africa',
        'eventID': 1,
        'location': 'Nairobi', 
        'date': '12-13-2017'

    }
]
#Function to create new events
@app.route('/brightEvents/api/v1/events', methods=['POST'])
def create_events():
    if not request.json or not 'eventName' in request.json:
        abort(400)
        event = {
        'eventID': events[-1]['id'] + 1,
        'eventName': request.json['eventName'],
        'location': request.json['location'],
        'date': request.json['date']
    }
    events.append(event)
    return jsonify({'event': event}), 201
    
# Function to the get event based on the ID
@app.route('/brightEvents/api/v1/events/<int:eventID>', methods=['GET'])
def get_event(eventID):
    event = [event for event in events if event['eventID'] == eventID]
    if len(event) == 0:
        abort(404)
    return render_template('userEvents.html', result=jsonify({'event': event[0]})) 

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
    if not request.json:
        abort(400)
    if 'eventName' in request.json and type(request.json['eventName']) != unicode:
        abort(400)
    if 'location' in request.json and type(request.json['location']) is not unicode:
        abort(400)
    
    event[0]['eventName'] = request.json.get('eventName', event[0]['eventName'])
    event[0]['location'] = request.json.get('location', event[0]['location'])
    event[0]['date'] = request.json.get('date', event[0]['date'])
    return jsonify({'event': event[0]})


#Function to delete an event based on the ID
@app.route('/brightEvents/api/v1/events/<int:eventID>', methods=['DELETE'])
def delete_event(eventID):
    event = [event for event in events if event['eventID'] == eventID]
    if len(event) == 0:
        abort(404)
    event.remove(event[0])
    return jsonify({'result': True})

    # The main method
if __name__ == '__main__':
    app.run(debug=True)