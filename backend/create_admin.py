"""
Script to create a default admin user
"""
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()

def create_admin():
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
    
    # Admin credentials
    email = "admin@snipx.com"
    password = "admin123"
    name = "Admin User"
    
    # Check if admin already exists
    existing_admin = db.admins.find_one({'email': email})
    
    if existing_admin:
        print(f"⚠️ Admin already exists with email: {email}")
        # Update password anyway
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db.admins.update_one(
            {'email': email},
            {'$set': {'password_hash': password_hash}}
        )
        print(f"✅ Password updated for admin: {email}")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
    else:
        # Create new admin
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        admin_doc = {
            'email': email,
            'password_hash': password_hash,
            'name': name,
            'role': 'super_admin',
            'permissions': {
                'view_users': True,
                'edit_users': True,
                'delete_users': True,
                'view_videos': True,
                'delete_videos': True,
                'view_analytics': True,
                'manage_admins': True,
                'system_settings': True
            },
            'is_active': True,
            'last_login': None
        }
        
        result = db.admins.insert_one(admin_doc)
        print(f"✅ Admin created successfully!")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print(f"🆔 Admin ID: {result.inserted_id}")
    
    client.close()

if __name__ == '__main__':
    create_admin()
