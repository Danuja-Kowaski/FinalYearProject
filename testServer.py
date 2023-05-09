from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import hashlib


#Mongo connection
client = MongoClient('mongodb://localhost:27017/')
db = client['users_db']
users_collection = db['users']

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)


@app.route('/register', methods=['POST'])
def register(username, password):
    data = request.get_json()
    #  Check if user already exists
    if users_collection.find_one({"username": username}):
        return False
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users_collection.insert_one({"username": username, "email": email, "password": hashed_password})
    #     return True
    return jsonify({'message': 'User created successfully'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = next((user for user in users if user['username'] == username), None)
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=user['id'])
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({'message': 'This is a protected route'})


if __name__ == '__main__':
    app.run(debug=True)
