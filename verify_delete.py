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

    # 2. Create Patient & Treatment
    print("\n--- 2. Create Treatment to Delete ---")
    patient_data = {
        "first_name": "Delete",
        "last_name": "Me",
        "date_of_birth": "1990-01-01",
        "contact_number": "0000000000",
        "email": "delete.me@test.com",
        "medical_history": "None"
    }
    # Check if patient exists first to avoid unique constraint error
    # Actually just POST, if fails 500/400 maybe it exists.
    # We'll assume fresh DB or handle error.
    res = session.post(f'{BASE_URL}/v2/patients', json=patient_data, headers=headers)
    if res.status_code == 201:
        patient_id = res.json()['id']
    else:
        # Try to find him
        print("Patient creation failed (maybe exists), trying to finding him...")
        res = session.get(f'{BASE_URL}/v2/patients', headers=headers)
        patients = res.json()
        target = next((p for p in patients if p['email'] == 'delete.me@test.com'), None)
        if target:
            patient_id = target['id']
        else:
            print("Could not find or create patient.")
            return

    treatment_data = {
        "patient_id": patient_id,
        "diagnosis": "To Delete",
        "treatment_details": "Delete this",
        "status": "In Progress"
    }
    res = session.post(f'{BASE_URL}/v2/treatments', json=treatment_data, headers=headers)
    if res.status_code != 201:
        print(f"Create Treatment failed: {res.text}")
        return
    treatment_id = res.json()['id']
    print(f"Treatment created ID: {treatment_id}")

    # 3. Try to Delete
    print(f"\n--- 3. Delete Treatment {treatment_id} ---")
    res = session.delete(f'{BASE_URL}/v2/treatments/{treatment_id}', headers=headers)
    
    print(f"Delete Status: {res.status_code}")
    print(f"Delete Response: {res.text}")
    
    if res.status_code == 200:
        print("SUCCESS: Deleted.")
    else:
        print("FAIL: Check backend logs.")

if __name__ == '__main__':
    run()
