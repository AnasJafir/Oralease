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

    # 2. Create Patient and Dependent Data (Appointment)
    print("\n--- 2. Create Patient & Appointment ---")
    patient_data = {
        "first_name": "Cascade",
        "last_name": "Test",
        "date_of_birth": "1990-01-01",
        "contact_number": "0000000000",
        "email": "cascade@test.com",
        "medical_history": "None"
    }
    res = session.post(f'{BASE_URL}/v2/patients', json=patient_data, headers=headers)
    if res.status_code == 201:
        patient_id = res.json()['id']
        print(f"Patient created ID: {patient_id}")
    else:
        print("Create patient failed")
        return

    # Create Appointment linked to patient
    apt_data = {
        "patient_id": patient_id,
        "appointment_date": "2025-12-25 10:00:00",
        "type": "Consultation",
        "status": "Scheduled"
    }
    res = session.post(f'{BASE_URL}/v2/appointments', json=apt_data, headers=headers)
    if res.status_code == 201:
        print("Appointment created.")
    else:
        print(f"Appointment failed: {res.text}")

    # 3. Delete Patient
    print(f"\n--- 3. Delete Patient {patient_id} ---")
    res = session.delete(f'{BASE_URL}/v2/patients/{patient_id}', headers=headers)
    
    print(f"Delete Status: {res.status_code}")
    if res.status_code == 200:
        print("SUCCESS: Patient and dependencies deleted.")
    else:
        print(f"FAIL: {res.text}")

if __name__ == '__main__':
    run()
