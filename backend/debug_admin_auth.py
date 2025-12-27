"""
Debug admin authentication issue
"""
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()

def debug_admin():
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    
    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
    db = client.snipx
    
    print("=" * 60)
    print("DEBUGGING ADMIN AUTHENTICATION")
    print("=" * 60)
    
    # Check admin record
    admin = db.admins.find_one({'email': 'admin@snipx.com'})
    
    if admin:
        print("\n✅ Admin found in database")
        print(f"Email: {admin['email']}")
        print(f"Name: {admin.get('name')}")
        print(f"Role: {admin.get('role')}")
        print(f"Is Active: {admin.get('is_active')}")
        print(f"Password Hash Type: {type(admin['password_hash'])}")
        print(f"Password Hash (first 20 chars): {str(admin['password_hash'][:20])}")
        
        # Test with different password encoding
        password = "admin123"
        
        print("\n🧪 Testing password verification...")
        try:
            # Standard check
            result1 = bcrypt.checkpw(password.encode('utf-8'), admin['password_hash'])
            print(f"Standard check: {result1}")
            
            # Check if password_hash is stored as string
            if isinstance(admin['password_hash'], str):
                print("⚠️  Password hash is stored as STRING (should be BYTES)")
                result2 = bcrypt.checkpw(password.encode('utf-8'), admin['password_hash'].encode('utf-8'))
                print(f"String-to-bytes check: {result2}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ Admin not found")
    
    # Compare with a regular user
    print("\n" + "=" * 60)
    print("COMPARING WITH REGULAR USER")
    print("=" * 60)
    
    user = db.users.find_one()
    if user:
        print(f"\n✅ Sample user found: {user.get('email')}")
        print(f"Password Hash Type: {type(user.get('password_hash'))}")
        print(f"Password Hash (first 20 chars): {str(user.get('password_hash', '')[:20])}")
    else:
        print("No users found")
    
    client.close()

if __name__ == '__main__':
    debug_admin()
