"""
Simple admin login troubleshooting guide
"""

print("=" * 60)
print("ADMIN LOGIN TROUBLESHOOTING GUIDE")
print("=" * 60)

print("\n✅ Admin Account Details:")
print("   📧 Email: admin@snipx.com")
print("   🔑 Password: admin123")

print("\n📋 Steps to fix the login issue:")
print("\n1️⃣  VERIFY BACKEND IS RUNNING:")
print("   • Open a terminal")
print("   • Navigate to backend folder:")
print("     cd c:\\Users\\Acer\\Downloads\\fypdec\\fypdec\\FYP\\backend")
print("   • Start the server:")
print("     python app.py")
print("   • Wait for message: 'Running on http://0.0.0.0:5001'")

print("\n2️⃣  CHECK CONNECTION:")
print("   • Open browser and go to: http://localhost:5001/")
print("   • You should see a response (not 'Cannot connect')")

print("\n3️⃣  TEST ADMIN LOGIN:")
print("   • Go to: http://localhost:5173/admin/login")
print("   • OR go to: http://localhost:3000/admin/login")
print("   • Enter credentials:")
print("     Email: admin@snipx.com")
print("     Password: admin123")

print("\n4️⃣  COMMON ISSUES:")
print("   ❌ 'Invalid credentials' error:")
print("      → Backend is running but password is wrong")
print("      → Run: python create_admin.py (to reset password)")
print()
print("   ❌ 'Cannot connect' or 'Network error':")
print("      → Backend is NOT running")
print("      → Start backend server (step 1)")
print()
print("   ❌ Frontend shows wrong port:")
print("      → Check frontend is using port 5001")
print("      → Check: src/pages/AdminLogin.tsx")
print("      → Should have: API_URL = 'http://localhost:5001'")

print("\n5️⃣  RESET ADMIN PASSWORD:")
print("   • Navigate to backend:")
print("     cd c:\\Users\\Acer\\Downloads\\fypdec\\fypdec\\FYP\\backend")
print("   • Run:")
print("     python create_admin.py")
print("   • This will reset password to: admin123")

print("\n" + "=" * 60)
print("🔍 QUICK TEST:")
print("=" * 60)

# Test MongoDB connection
try:
    from pymongo import MongoClient
    from dotenv import load_dotenv
    import os
    import bcrypt
    
    load_dotenv()
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    
    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
    client.server_info()
    
    db = client.snipx
    admin = db.admins.find_one({'email': 'admin@snipx.com'})
    
    if admin:
        print("✅ Database: Connected")
        print("✅ Admin: Found")
        
        # Test password
        is_valid = bcrypt.checkpw('admin123'.encode('utf-8'), admin['password_hash'])
        print(f"✅ Password: {'Valid ✓' if is_valid else 'INVALID ✗'}")
        
        if not is_valid:
            print("\n⚠️  PASSWORD ISSUE DETECTED!")
            print("Run: python create_admin.py")
    else:
        print("❌ Admin not found in database")
        print("Run: python create_admin.py")
    
    client.close()
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("Make sure MongoDB is running!")

print("\n" + "=" * 60)

# Test if backend is running
try:
    import requests
    response = requests.get('http://localhost:5001/', timeout=2)
    print("✅ Backend: Running on port 5001")
except requests.exceptions.ConnectionError:
    print("❌ Backend: NOT running")
    print("   → Start it with: python app.py")
except Exception as e:
    print(f"⚠️  Backend check failed: {e}")

print("=" * 60)
