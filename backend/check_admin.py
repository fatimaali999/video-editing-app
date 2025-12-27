"""
Script to check admin user details
"""
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()

def check_admin():
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
    
    # Find admin
    email = "admin@snipx.com"
    password = "admin123"
    
    admin = db.admins.find_one({'email': email})
    
    if admin:
        print(f"\n✅ Admin found:")
        print(f"📧 Email: {admin['email']}")
        print(f"👤 Name: {admin.get('name', 'N/A')}")
        print(f"🔑 Role: {admin.get('role', 'N/A')}")
        print(f"🔓 Is Active: {admin.get('is_active', 'N/A')}")
        print(f"🔐 Password Hash Type: {type(admin['password_hash'])}")
        print(f"🔐 Password Hash Length: {len(admin['password_hash']) if admin['password_hash'] else 'N/A'}")
        
        # Test password verification
        try:
            password_hash = admin['password_hash']
            if isinstance(password_hash, str):
                password_hash = password_hash.encode('utf-8')
            
            is_valid = bcrypt.checkpw(password.encode('utf-8'), password_hash)
            print(f"\n🧪 Password Verification Test: {'✅ PASSED' if is_valid else '❌ FAILED'}")
            
            if not is_valid:
                print("\n⚠️ Password does not match! This is the issue.")
                print("Let's recreate the hash...")
                
                # Create correct hash
                new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                print(f"New hash type: {type(new_hash)}")
                
                # Update in database
                db.admins.update_one(
                    {'email': email},
                    {'$set': {'password_hash': new_hash}}
                )
                print("✅ Password hash updated!")
                
                # Verify again
                admin = db.admins.find_one({'email': email})
                is_valid_now = bcrypt.checkpw(password.encode('utf-8'), admin['password_hash'])
                print(f"🧪 Re-verification: {'✅ PASSED' if is_valid_now else '❌ STILL FAILED'}")
            
        except Exception as e:
            print(f"\n❌ Error during password verification: {e}")
            print(f"Error type: {type(e).__name__}")
    else:
        print(f"❌ Admin not found with email: {email}")
    
    client.close()

if __name__ == '__main__':
    check_admin()
