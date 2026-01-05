import requests

try:
    url = 'http://localhost:5000/api/auth/login'
    data = {"username": "admin", "password": "admin123"}
    headers = {"Content-Type": "application/json"}
    
    print(f"POST {url}")
    response = requests.post(url, json=data, headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
    
except Exception as e:
    print(f"Error: {e}")
