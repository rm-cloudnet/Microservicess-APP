import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId  # Added to target specific records

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydatabase")
client = MongoClient(MONGO_URI)
db = client.get_default_database()
collection = db["tasks"]

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = []
    for doc in collection.find({}):
        tasks.append({
            "id": str(doc["_id"]),  # Convert ObjectId to string for JS to read
            "title": doc["title"],
            "completed": doc.get("completed", False)  # Safely fetch state
        })
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    if data and "title" in data:
        # Save task with a default 'completed' tracking flag
        collection.insert_one({
            "title": data["title"],
            "completed": False
        })
        return jsonify({"message": "Task added successfully!"}), 201
    return jsonify({"error": "Invalid data"}), 400

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def toggle_task(task_id):
    data = request.json
    if data and "completed" in data:
        # Update the specific document by its unique ID
        collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"completed": data["completed"]}}
        )
        return jsonify({"message": "Status updated!"}), 200
    return jsonify({"error": "Invalid payload"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
