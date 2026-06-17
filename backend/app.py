import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Allows the frontend to make requests to this API

# Fetch MongoDB URI from environment variable (default to local fallback)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydatabase")
client = MongoClient(MONGO_URI)
db = client.get_default_database()
collection = db["tasks"]

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = list(collection.find({}, {"_id": 0}))
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    if data and "title" in data:
        collection.insert_one({"title": data["title"]})
        return jsonify({"message": "Task added successfully!"}), 201
    return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    # Listen on all interfaces for container readiness
    app.run(host='0.0.0.0', port=5000)
