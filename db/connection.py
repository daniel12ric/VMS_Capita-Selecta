from pymongo import MongoClient
import pymongo
from config import MONGO_DB,MONGO_URI


class Database:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[MONGO_DB]  
        except pymongo.errors.ConnectionFailure:
            print("koneksi gagal {e}")

    def get_collection(self, collection_name):
        return self.db[collection_name]

db = Database()

class DB:
    akunColl = db.get_collection("AKUN")
    bankColl = db.get_collection("BANK")
    branchColl = db.get_collection("BRANCH")
    vendorColl = db.get_collection("VENDOR")
    orderColl = db.get_collection("ORDER")



