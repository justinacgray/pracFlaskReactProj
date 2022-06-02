from email.policy import default
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from  flask_cors import CORS



app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:yahor@localhost:5432/baby-tracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False) #can't be empty field, MUST have a value
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) this would be passed in constructor method
    
    def __repr__(self):
        # https://stackoverflow.com/questions/1984162/purpose-of-repr-method
        print("THIS IS WHAT THE __repr__ METHOD DOES!!!")
        return f"Event: {self.description}"
    
    def __init__(self, description):
        self.description = description

# this takes into our event and it'll format to that we have a json and we take that json and pass to front end so our frontend will have access to it without making an additional network request - 20 ins in explains this a code /event route too https://www.youtube.com/watch?v=RcQwcyyCOmM&t=1395s 
def format_event(event):
    return {
        "description": event.description,
        "id" : event.id,
        "created_at" : event.created_at
    }

@app.route('/')
def greet():
    return "<h1>shalom<h1>"

# can combine methods in an array like this methods=['POST', 'GET'] for one and methods=['DELETE', 'GET']

# create an event
@app.route("/events", methods=['POST'])
def create_event():
    # this could be request.form if I'm not mistaken 
    description = request.json['description']
    event = Event(description)
    db.session.add(event)
    # if data is not being saved to DB check to the commit- forgot the () on it
    db.session.commit()
    # this line is so that our front-end has access to this data
    return format_event(event)

# get all events
@app.route("/events", methods=['GET'])
def get_events():
    events = Event.query.order_by(Event.id.asc()).all()
    event_list= []
    for event in events:
        event_list.append(format_event(event))
    return {'events': event_list}

# get 1 event
@app.route('/events/<id>', methods=['GET'])
def get_event(id):
    # filtering by id so we can either use .one() ir .first()
    event = Event.query.filter_by(id=id).one()
    formatted_event = format_event(event)
    return {'event': formatted_event}

# delete 1 event
@app.route('/events/<id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.filter_by(id=id).one()
    db.session.delete(event)
    db.session.commit()
    return f'Event(id: {id}) deleted'

# update event 
@app.route('/events/<id>', methods=['PUT'])
def update_event(id):
    event = Event.query.filter_by(id=id)
    description= request.json['description']
    event.update(dict(description=description, created_at=datetime.utcnow()))
    db.session.commit()
    return {'event' : format_event(event.one())}
    
if __name__ == '__main__':
    app.run()