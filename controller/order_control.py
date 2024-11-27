from db.connection import db, DB
from datetime import datetime
from flask import request

orderColl = DB.orderColl

class OrderModel:
    def __init__(self):
        self.collection = db.get_collection("ORDER")
        
    def find_one(self, query):
        try:
            return self.collection.find_one(query)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_all(self):
        try:
            return list(self.collection.find({}))
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create(self, username):
        try:
            order_data = {
                "_id": request.form.get('_id'),
                "count": request.form.get('count'),
                "orderName": request.form.get('orderName'),
                "setup": {
                    "createDate": datetime.utcnow(),
                    "createUser": username,
                    "updateUser": username,
                    "updateDate": datetime.utcnow()
                }
            }
            if not order_data["_id"].strip():
                return {"success": False, "message": "_id is required"}
            if order_data["orderName"] is None:
                return {"success": False, "message": "orderName is required"}
            if not order_data["count"]:
                return {"success": False, "message": "count is required"}

            if self.collection.find_one({"_id": order_data["_id"]}):
                return {"success": False, "message": "Document with this _id already exists"}

            resultt = self.collection.insert_one(order_data)
            return {"success": True, "inserted_id": order_data["_id"]}
        except Exception as e:
            return {"success": False, "error": str(e)}
