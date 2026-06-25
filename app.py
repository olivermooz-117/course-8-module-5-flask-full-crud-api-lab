from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Welcome route
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Event Management API"}), 200

# Task 1 - Defining the Problem
# Get all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# Task 1 - Defining the Problem
# Getting a single event by id
@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    target_event = None
    for event in events:
        if event.id == event_id:
            target_event = event
            break

    if target_event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    return jsonify(target_event.to_dict()), 200

# Task 1 - Defining the Problem
# Creating a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Missing required field: title"}), 400

    new_id = max((e.id for e in events), default=0) + 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

# Task 1 - Defining the Problem
# Updating the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Missing required field: title"}), 400

    target_event = None
    for event in events:
        if event.id == event_id:
            target_event = event
            break

    if target_event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    target_event.title = data["title"]
    return jsonify(target_event.to_dict()), 200

# Task 1 - Defining the Problem
# Removing an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events

    target_event = None
    for event in events:
        if event.id == event_id:
            target_event = event
            break

    if target_event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    events = [e for e in events if e.id != event_id]
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)