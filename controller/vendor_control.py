from db.connection import db, DB
from datetime import datetime
from flask import request

akunColl = DB.akunColl

class VendorModel:
    def __init__(self):
        self.collection = db.get_collection("VENDOR")
        
    def get_bank(self):
        try:
            banks = db.get_collection("BANK").find({"activeStatus": "Y"})
            return [{"_id": bank["_id"], "bankDesc": bank["bankDesc"]} for bank in banks]
        except Exception as e:
            return {"success": False, "error": str(e)}

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
            vendor_data = {
                "_id": request.form.get('_id'),
                "partnerType": request.form.get('partnerType'),
                "vendorName": request.form.get('vendorName'),
                "unitUsaha": request.form.get('unitUsaha'), 
                "address": request.form.get('address'),
                "country": request.form.get('country'),
                "province": request.form.get('province'),
                "noTelp": request.form.get('noTelp'),
                "emailCompany": request.form.get('emailCompany'),
                "website": request.form.get('website'),
                "noNPWP": request.form.get('noNPWP'),
                "activeStatus": request.form.get('activeStatus'),
                "supportingEquipment": [],
                "accountBank": [],
                "pic": []
            } 
            i = 0
            while request.form.get(f"supportingEquipment[{i}][toolType]"):
                vendor_data["supportingEquipment"].append({
                    "toolType": request.form.get(f"supportingEquipment[{i}][toolType]"),
                    "count": request.form.get(f"supportingEquipment[{i}][count]"),
                    "merk": request.form.get(f"supportingEquipment[{i}][merk]"),
                    "condition": request.form.get(f"supportingEquipment[{i}][condition]")
                })
                i += 1

            i = 0
            while request.form.get(f"accountBank[{i}][bankCode]"):
                vendor_data["accountBank"].append({
                    "bankCode": request.form.get(f"accountBank[{i}][bankCode]"),
                    "bankName": request.form.get(f"accountBank[{i}][bankName]"),
                    "accountNumber": request.form.get(f"accountBank[{i}][accountNumber]"),
                    "accountName": request.form.get(f"accountBank[{i}][accountName]")
                })
                i += 1
            
            i = 0
            while request.form.get(f"pic[{i}][username]"):
                vendor_data["pic"].append({
                    "username": request.form.get(f"pic[{i}][username]"),
                    "name": request.form.get(f"pic[{i}][name]"),
                    "email": request.form.get(f"pic[{i}][email]"),
                    "noTelp": request.form.get(f"pic[{i}][noTelp]")
                })
                i += 1
                
            required_fields = ['_id', 'partnerType', 'vendorName', 'emailCompany']
            for field in required_fields:
                if not vendor_data.get(field):
                    return {"success": False, "message": f"{field} is required"}

            if 'emailCompany' in vendor_data and '@' not in vendor_data['emailCompany']:
                return {"success": False, "message": "Invalid email format"}
            
            if self.collection.find_one({"_id": vendor_data["_id"]}):
                return {"success": False, "message": "Document with this _id already exists"}

            result = self.collection.insert_one(vendor_data)
            return {"success": True, "inserted_id": vendor_data["_id"]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update(self, vendor_id,update_data, username):
        try:
            update_data = {
            "partnerType": update_data.get('partnerType'),
            "vendorName": update_data.get('vendorName'),
            "unitUsaha": update_data.get('unitUsaha'),
            "address": update_data.get('address'),
            "country": update_data.get('country'),
            "province": update_data.get('province'),
            "noTelp": update_data.get('noTelp'),
            "emailCompany": update_data.get('emailCompany'),
            "website": update_data.get('website'),
            "noNPWP": update_data.get('noNPWP'),
            "activeStatus": update_data.get('activeStatus'), 
            "supportingEquipment": update_data.get("supportingEquipment", []),
            "pic": update_data.get("pic", []),
            "accountBank": update_data.get("accountBank", []),
            "change.updateUser": username,
            "change.updateDate": datetime.utcnow()
            }
            result = self.collection.update_one(
                {"_id": vendor_id},
                {"$set": update_data}
            )
            if result.matched_count == 0:
                return {"success": False}
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete(self, vendor_id):
        try:
            result = self.collection.delete_one({"_id": vendor_id})
            if result.deleted_count == 0:
                return {"success": False, "message": "Document not found"}
            return {"success": True, "message": "Document deleted successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    

        
