from dotenv import load_dotenv
import redis, os

load_dotenv()
#key
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB = os.getenv('MONGO_DB')
secret_key= os.getenv('secret_key')
# r = redis.StrictRedis(host="10.85.49.147", port=6379, db=0, password="b56e784c-49a7-4adf-be06-7192ca6ea73e")
r = redis.Redis(host='localhost', port= 6379, db= 0)
salted = os.getenv('saltedd')

