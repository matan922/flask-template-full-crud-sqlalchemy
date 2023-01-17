from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)

# Configure the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite3')
db = SQLAlchemy(app)
CORS(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    #This will help in debugging, this will be shown in the console
    def __repr__(self):
        return '<User %r>' % self.username
   
    #This function will be used to jsonify the object
    def serialize(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

@app.route('/', methods=['GET'])
def test_home_page():
    return "hello world"

# Create a new user
@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'new user created!'})

# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

# Get a single user
@app.route('/user/<id>', methods=['GET'])
def get_one_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize())

# Update a user
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    data = request.get_json()
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'user updated!'})

# Delete a user
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'message': 'user deleted!'})


# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
