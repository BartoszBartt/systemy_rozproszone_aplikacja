from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.mongo_client import MongoClient


app = Flask(__name__)

client = MongoClient("mongodb+srv://spambartosz123:c0WDL8nciXDSAo1w@cluster0.ffekdag.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client['systemy_rozproszone2']
collection = db["users"]

@app.route('/register', methods=['POST'])
def register():
    # Get JSON data from request
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username and password:
        # Check if user already exists
        if collection.find_one({'username': username}):
            return jsonify({'message': 'User already exists.'}), 409
        
        # Hash password and save user
        hash_pass = generate_password_hash(password)
        collection.insert_one({'username': username, 'password': hash_pass})
        return jsonify({'message': 'User registered successfully.'}), 201
    else:
        return jsonify({'message': 'Missing username or password.'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password.'}), 400
    
    user = collection.find_one({'username': username})
    
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Logged in successfully.'}), 200
    else:
        return jsonify({'message': 'Invalid username or password.'}), 401

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
