"""
Test admin login API endpoint
"""
import requests
import json

def test_api_login():
    url = "http://localhost:5000/api/admin/login"
    
    data = {
        "email": "admin@snipx.com",
        "password": "admin123"
    }
    
    print(f"🌐 Testing API endpoint: {url}")
    print(f"📧 Email: {data['email']}")
    print(f"🔑 Password: {data['password']}")
    
    try:
        response = requests.post(url, json=data)
        
        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📄 Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\n✅ Login successful!")
        else:
            print(f"\n❌ Login failed: {response.json().get('error')}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to server. Is Flask app running?")
        print("💡 Run: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    test_api_login()
