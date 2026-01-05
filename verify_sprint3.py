import requests
import datetime

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

    # 2. Get Initial Revenue
    print("\n--- 2. Check Initial Revenue ---")
    res = session.get(f'{BASE_URL}/v2/dashboard/summary', headers=headers)
    initial_revenue_str = res.json()['stats']['revenue']
    print(f"Initial Revenue: {initial_revenue_str}")

    # 3. Create Paid Invoice (200.00 EUR)
    print("\n--- 3. Create Paid Invoice (200 €) ---")
    
    # Need patient
    res = session.get(f'{BASE_URL}/v2/patients', headers=headers)
    patients = res.json()
    if not patients:
        print("No patients found, cannot create invoice.")
        return
    patient_id = patients[0]['id']

    invoice_data = {
        "patient_id": patient_id,
        "total_amount": 200.0,
        "status": "Paid",
        "items": [{"description": "Sprint 3 Test", "quantity": 1, "price": 200.0}]
    }
    
    res = session.post(f'{BASE_URL}/v2/invoices', json=invoice_data, headers=headers)
    if res.status_code != 201:
        print(f"Invoice creation failed: {res.text}")
        return
    print("Invoice Created & Paid.")

    # 4. Check Updated Revenue
    print("\n--- 4. Check Updated Revenue ---")
    res = session.get(f'{BASE_URL}/v2/dashboard/summary', headers=headers)
    updated_revenue_str = res.json()['stats']['revenue']
    print(f"Updated Revenue: {updated_revenue_str}")
    
    # Parse and compare
    # "1 450,00 €" -> 1450.00
    try:
        initial = float(initial_revenue_str.replace(' €', '').replace(' ', '').replace(',', '.'))
        updated = float(updated_revenue_str.replace(' €', '').replace(' ', '').replace(',', '.'))
        diff = updated - initial
        print(f"Difference: {diff:.2f}")
        
        if abs(diff - 200.0) < 0.01:
            print("SUCCESS: Revenue updated correctly.")
        else:
            print("FAIL: Revenue did not update correctly.")
    except Exception as e:
        print(f"Error parsing revenue: {e}")

if __name__ == '__main__':
    run()
