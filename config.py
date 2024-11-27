import redis

#key
MONGO_URI = "mongodb+srv://danieldarrenr:HNp0CRMCUgoRUYGu@clusterkapita.rxlsn.mongodb.net/"
MONGO_DB = "TR"
secret_key= "Kapita"
r = redis.StrictRedis(host="10.85.49.147", port=6379, db=0, password="b56e784c-49a7-4adf-be06-7192ca6ea73e")
# r = redis.Redis(host='localhost', port= 6379, db= 0)
salted = "kapita"


