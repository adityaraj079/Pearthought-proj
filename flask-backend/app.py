from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(email=data['email'], notification_preference=data['preference'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/preferences', methods=['GET'])
def get_preferences():
    users = User.query.all()
    return jsonify([{"email": user.email, "preference": user.notification_preference} for user in users]), 200

@app.route('/sns/bounce', methods=['POST'])
def handle_bounce():
    notification = json.loads(request.data)
    message = json.loads(notification['Message'])

    for recipient in message['bounce']['bouncedRecipients']:
        email = recipient['emailAddress']
        user = User.query.filter_by(email=email).first()
        if user:
            user.status = 'bounced'
            db.session.commit()

    return '', 200

@app.route('/sns/complaint', methods=['POST'])
def handle_complaint():
    notification = json.loads(request.data)
    message = json.loads(notification['Message'])

    for recipient in message['complaint']['complainedRecipients']:
        email = recipient['emailAddress']
        user = User.query.filter_by(email=email).first()
        if user:
            user.status = 'complained'
            db.session.commit()

    return '', 200

@app.route('/unsubscribe/<email>', methods=['GET'])
def unsubscribe(email):
    user = User.query.filter_by(email=email).first()
    if user:
        user.status = 'unsubscribed'
        db.session.commit()
        return jsonify({"message": "You have been unsubscribed"}), 200
    return jsonify({"message": "Email not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
