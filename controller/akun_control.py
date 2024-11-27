from db.connection import db, DB

akunColl = DB.akunColl

class AkunModel:
    def __init__(self):
        self.collection = db.get_collection("AKUN")

    def get_all(self):
        try:
            return list(self.collection.find({}, {"_id": 0, "username": 1, "roleid": 1}))
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_role(self, username, roleid):
        try:
            update_data = {
                "roleid": roleid,
            }
            result = self.collection.update_one(
                {"username": username},
                {"$set": update_data}
            )
            if result.matched_count == 0:
                return {"success": False, "message": "Account not found"}
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
        
    def delete(self, username):
        try:
            result = self.collection.delete_one({"username": username})
            if result.deleted_count == 0:
                return {"success": False, "message": "User not found"}
            return {"success": True, "message": "User deleted successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        
        

