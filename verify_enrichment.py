import requests
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'
AUTH_URL = f'{BASE_URL}/auth/login'

def run():
    session = requests.Session()
    
    # 1. Login
    print("--- 1. Login ---")
    res = session.post(AUTH_URL, json={"username": "admin", "password": "admin123"})
    if res.status_code != 200:
        print(f"Login failed: {res.text}")
        return
    token = res.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    print("Login successful.")

    # 2. Create Patient
    print("\n--- 2. Create Patient ---")
    patient_data = {
        "first_name": "Jean",
        "last_name": "Dupont",
        "date_of_birth": "1980-01-01",
        "contact_number": "0123456789",
        "email": "jean.dupont@example.com",
        "medical_history": "None"
    }
    res = session.post(f'{BASE_URL}/v2/patients', json=patient_data, headers=headers)
    if res.status_code != 201:
        print(f"Create Patient failed: {res.text}")
        return
    patient_id = res.json()['id']
    print(f"Patient created with ID: {patient_id}")

    # 3. Create Appointment (Urgent)
    print("\n--- 3. Create Appointment (Urgent) ---")
    today_str = datetime.now().isoformat()
    apt_data = {
        "patient_id": patient_id,
        "appointment_date": today_str,
        "notes": "Douleur intense, urgence",
        "type": "Urgence",
        "status": "Scheduled"
    }
    res = session.post(f'{BASE_URL}/v2/appointments', json=apt_data, headers=headers)
    if res.status_code != 201:
        print(f"Create Appointment failed: {res.text}")
        return
    apt = res.json()
    print(f"Appointment created. Type: {apt.get('type')}, Status: {apt.get('status')}")
    if apt.get('type') != 'Urgence' or apt.get('status') != 'Scheduled':
        print("FAIL: Fields incorrect!")
        return

    # 4. Check Dashboard
    print("\n--- 4. Check Dashboard ---")
    res = session.get(f'{BASE_URL}/v2/dashboard/summary', headers=headers)
    dashboard = res.json()
    appointments = dashboard.get('appointments', [])
    print(f"Dashboard Appointments: {len(appointments)}")
    
    found = False
    for a in appointments:
        print(f" - Apt: {a['patient']}, Type: {a['type']}, Urgent: {a.get('urgent')}")
        if a['type'] == 'Urgence' and a['urgent'] is True:
            found = True
    
    if found:
        print("SUCCESS: Dashboard correctly flags the urgent appointment.")
    else:
        print("FAIL: Dashboard did not flag urgency.")

if __name__ == '__main__':
    run()
