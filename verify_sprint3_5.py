import requests

BASE_URL = 'http://localhost:5000/api'
AUTH_URL = f'{BASE_URL}/auth/login'

def run():
    session = requests.Session()
    
    # 1. Login
    print("--- 1. Login ---")
    res = session.post(AUTH_URL, json={"username": "admin", "password": "admin123"})
    token = res.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # 2. Create Patient
    print("\n--- 2. Create Patient ---")
    patient_data = {
        "first_name": "Link",
        "last_name": "Test",
        "date_of_birth": "1990-01-01",
        "contact_number": "0000",
        "email": "link@test.com",
        "medical_history": "None"
    }
    res = session.post(f'{BASE_URL}/v2/patients', json=patient_data, headers=headers)
    patient_id = res.json()['id']
    print(f"Patient ID: {patient_id}")

    # 3. Create Treatment Plan
    print("\n--- 3. Create Treatment Plan ---")
    plan_data = {
        "patient_id": patient_id,
        "diagnosis": "Root Canal",
        "treatment_details": "Complex procedure",
        "status": "Pending"
    }
    res = session.post(f'{BASE_URL}/v2/treatments', json=plan_data, headers=headers)
    plan_id = res.json()['id']
    print(f"Treatment Plan ID: {plan_id}")

    # 4. Create Invoice Linked to Plan
    print("\n--- 4. Create Linked Invoice ---")
    invoice_data = {
        "patient_id": patient_id,
        "treatment_plan_id": plan_id,
        "total_amount": 500.0,
        "status": "Draft",
        "items": [{"description": "Root Canal 1", "quantity": 1, "price": 500.0}]
    }
    res = session.post(f'{BASE_URL}/v2/invoices', json=invoice_data, headers=headers)
    
    if res.status_code == 201:
        inv = res.json()
        print(f"Invoice Created: {inv['id']}")
        if inv.get('treatment_plan_id') == plan_id:
            print("SUCCESS: Invoice is linked to Treatment Plan.")
        else:
            print(f"FAIL: Invoice link missing. Got: {inv.get('treatment_plan_id')}")
    else:
        print(f"FAIL: Invoice creation error: {res.text}")

if __name__ == '__main__':
    run()
