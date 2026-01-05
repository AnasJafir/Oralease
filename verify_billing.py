import requests

BASE_URL = 'http://localhost:5000/api'
AUTH_URL = f'{BASE_URL}/auth/login'

def run():
    session = requests.Session()
    
    # 1. Login
    print("--- 1. Login ---")
    try:
        res = session.post(AUTH_URL, json={"username": "admin", "password": "admin123"})
        if res.status_code != 200:
            print(f"Login failed: {res.text}")
            return
        token = res.json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        print("Login successful.")
    except Exception as e:
        print(f"Connection error: {e}")
        return

    # 2. Get Patient (We just reset DB, need to create one)
    print("\n--- 2. Create Patient ---")
    patient_data = {
        "first_name": "Billing",
        "last_name": "Test",
        "date_of_birth": "2000-01-01",
        "contact_number": "0000000000",
        "email": "billing@test.com",
        "medical_history": "None"
    }
    res = session.post(f'{BASE_URL}/v2/patients', json=patient_data, headers=headers)
    if res.status_code == 201:
        patient_id = res.json()['id']
        print(f"Created Patient ID: {patient_id}")
    else:
        print(f"Patient creation failed: {res.text}")
        return

    # 3. Create Invoice
    print("\n--- 3. Create Invoice ---")
    invoice_data = {
        "patient_id": patient_id,
        "total_amount": 150.0,
        "items": [
            {"description": "Consultation", "quantity": 1, "price": 50.0},
            {"description": "Cleaning", "quantity": 1, "price": 100.0}
        ],
        "status": "Draft"
    }
    res = session.post(f'{BASE_URL}/v2/invoices', json=invoice_data, headers=headers)
    print(f"Create Invoice Status: {res.status_code}")
    if res.status_code == 201:
        invoice_id = res.json()['id']
        print(f"Invoice Created ID: {invoice_id}")
        print(f"Items: {res.json()['items']}")
    else:
        print(f"Response: {res.text}")
        return

    # 4. Update Invoice Status
    print("\n--- 4. Update Status to Paid ---")
    res = session.put(f'{BASE_URL}/v2/invoices/{invoice_id}', json={"status": "Paid"}, headers=headers)
    if res.status_code == 200:
        print(f"Status Updated: {res.json()['status']}")
    else:
        print(f"Update Failed: {res.text}")

    # 5. List Invoices
    print("\n--- 5. List Invoices ---")
    res = session.get(f'{BASE_URL}/v2/invoices', headers=headers)
    print(f"Count: {len(res.json())}")

if __name__ == '__main__':
    run()
