from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.library
collection = db.inventory

@app.route("/inventory", methods=["GET"])
def get_inventory():
    inventory = list(db.inventory.find({}, {"_id": 0}))
    return jsonify(inventory)

@app.route("/inventory", methods=["POST"])
def add_inventory():
    item = request.json
    db.inventory.insert_one(item)
    return jsonify({"msg": "Inventory item added"}), 201

@app.route("/inventory/<isbn>", methods=["PATCH"])
def update_stock(isbn):
    data = request.json
    db.inventory.update_one({"isbn": isbn}, {"$set": data})
    return jsonify({"msg": "Stock updated"})

@app.route("/inventory/<isbn>", methods=["PUT"])
def replace_inventory(isbn):
    data = request.json
    result = db.inventory.replace_one({"isbn": isbn}, data, upsert=True)
    return jsonify({"msg": "Inventory record replaced", "matched": result.matched_count})

@app.route("/inventory/<isbn>", methods=["DELETE"])
def delete_inventory(isbn):
    result = db.inventory.delete_one({"isbn": isbn})
    return jsonify({"msg": "Inventory item deleted", "deleted": result.deleted_count})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
