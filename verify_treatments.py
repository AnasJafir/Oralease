import requests
import time

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

    # 2. Get or Create Patient
    print("\n--- 2. Get/Create Patient ---")
    res = session.get(f'{BASE_URL}/v2/patients', headers=headers)
    patients = res.json()
    if len(patients) > 0:
        patient_id = patients[0]['id']
        print(f"Using existing patient ID: {patient_id}")
    else:
        patient_data = {
            "first_name": "Test",
            "last_name": "Treatment",
            "date_of_birth": "1990-01-01",
            "contact_number": "0000000000",
            "email": "treatment@test.com",
            "medical_history": "None"
        }
        res = session.post(f'{BASE_URL}/v2/patients', json=patient_data, headers=headers)
        patient_id = res.json()['id']
        print(f"Created patient ID: {patient_id}")

    # 3. Create Treatment
    print("\n--- 3. Create Treatment ---")
    treatment_data = {
        "patient_id": patient_id,
        "diagnosis": "Carie profonde",
        "treatment_details": "Obturation composite",
        "status": "In Progress"
    }
    res = session.post(f'{BASE_URL}/v2/treatments', json=treatment_data, headers=headers)
    if res.status_code != 201:
        print(f"Create Treatment failed: {res.text}")
        return
    treatment_id = res.json()['id']
    print(f"Treatment created ID: {treatment_id}")

    # 4. Get Treatment By ID (The new endpoint)
    print("\n--- 4. Verify GET /treatments/<id> ---")
    res = session.get(f'{BASE_URL}/v2/treatments/{treatment_id}', headers=headers)
    if res.status_code == 200:
        t = res.json()
        print(f"SUCCESS: Fetched treatment {t['id']}")
        print(f" - Diagnosis: {t['diagnosis']}")
        print(f" - Patient: {t.get('patient', {}).get('first_name')}")
    else:
        print(f"FAIL: Could not fetch treatment {treatment_id}. Status: {res.status_code}")
        print(res.text)

if __name__ == '__main__':
    run()
