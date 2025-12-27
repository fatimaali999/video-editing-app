from pymongo import MongoClient
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
db = client.snipx

admin = db.admins.find_one({'email': 'admin@snipx.com'})

if admin:
    print(f"Admin email: {admin['email']}")
    print(f"Password hash type: {type(admin['password_hash'])}")
    print(f"Is bytes: {isinstance(admin['password_hash'], bytes)}")
    print(f"Password check result: {bcrypt.checkpw(b'admin123', admin['password_hash'])}")
    print(f"Is active: {admin.get('is_active', True)}")
else:
    print("Admin not found")

client.close()
