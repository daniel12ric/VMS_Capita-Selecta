from db.connection import db, DB
from datetime import datetime
from flask import request

akunColl = DB.akunColl

class BankModel:
    def __init__(self):
        self.collection = db.get_collection("BANK")

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
            bank_data = {
                "_id": request.form.get('_id'),
                "activeStatus": request.form.get('activeStatus'),
                "bankDesc": request.form.get('bankDesc'),
                "setup": {
                    "createDate": datetime.utcnow(),
                    "createUser": username,
                    "updateUser": username,
                    "updateDate": datetime.utcnow()
                }
            }
            if not bank_data["_id"].strip():
                return {"success": False, "message": "_id is required"}
            if bank_data["activeStatus"] is None:
                return {"success": False, "message": "activeStatus is required"}
            if not bank_data["bankDesc"].strip():
                return {"success": False, "message": "bankDesc is required"}

            if self.collection.find_one({"_id": bank_data["_id"]}):
                return {"success": False, "message": "Document with this _id already exists"}

            result = self.collection.insert_one(bank_data)
            return {"success": True, "inserted_id": bank_data["_id"]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update(self, bank_id,update_data, username):
        try:
            update_data = {
                "activeStatus": update_data.get('activeStatus'),
                "bankDesc": update_data.get('bankDesc'),
                "setup.updateUser": username,
                "setup.updateDate": datetime.utcnow()
            }

            result = self.collection.update_one(
                {"_id": bank_id},
                {"$set": update_data}
            )
            if result.matched_count == 0:
                return {"success": False}
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, bank_id):
        try:
            result = self.collection.delete_one({"_id": bank_id})
            if result.deleted_count == 0:
                return {"success": False, "message": "Document not found"}
            return {"success": True, "message": "Document deleted successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        
