"""
Test admin login flow
"""
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import bcrypt
from datetime import datetime

load_dotenv()

def test_admin_login():
    # Connect to MongoDB
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    atlas_uri = os.getenv('MONGODB_ATLAS_URI')
    
    try:
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✅ Connected to local MongoDB")
    except:
        if atlas_uri:
            client = MongoClient(atlas_uri, serverSelectionTimeoutMS=10000)
            client.server_info()
            print("✅ Connected to MongoDB Atlas")
        else:
            print("❌ Could not connect to MongoDB")
            return
    
    db = client.snipx
    admins = db.admins
    
    # Test credentials
    email = "admin@snipx.com"
    password = "admin123"
    
    print(f"\n🔍 Testing login for: {email}")
    print(f"🔑 Password: {password}")
    
    # Step 1: Find admin
    admin_data = admins.find_one({'email': email})
    
    if not admin_data:
        print("❌ Admin not found")
        return
    
    print("✅ Admin found in database")
    
    # Step 2: Check is_active
    is_active = admin_data.get('is_active', True)
    print(f"🔓 Is Active: {is_active}")
    
    if not is_active:
        print("❌ Admin is not active")
        return
    
    # Step 3: Check password
    print("\n🧪 Testing password verification...")
    print(f"Password hash type: {type(admin_data['password_hash'])}")
    print(f"Password type: {type(password)}")
    print(f"Password encoded type: {type(password.encode('utf-8'))}")
    
    try:
        password_match = bcrypt.checkpw(password.encode('utf-8'), admin_data['password_hash'])
        print(f"Password check result: {password_match}")
        
        if not password_match:
            print("❌ Password does not match")
            return
        
        print("✅ Password matches!")
        
        # Step 4: Update last login (like in authenticate_admin)
        admins.update_one(
            {'_id': admin_data['_id']},
            {'$set': {'last_login': datetime.now()}}
        )
        print("✅ Last login updated")
        
        # Step 5: Return admin data
        print("\n✅ Login successful!")
        print(f"Admin ID: {admin_data['_id']}")
        print(f"Admin Name: {admin_data.get('name')}")
        print(f"Admin Role: {admin_data.get('role')}")
        
    except Exception as e:
        print(f"❌ Error during password check: {e}")
        import traceback
        traceback.print_exc()
    
    client.close()

if __name__ == '__main__':
    test_admin_login()
