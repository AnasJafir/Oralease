import requests
import json
import random
import datetime

BASE_URL = "http://127.0.0.1:5000/api/v2"

def get_auth_token():
    try:
        response = requests.post("http://127.0.0.1:5000/api/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        print(f"Login failed: {response.text}")
        return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def get_revenue(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/dashboard/summary", headers=headers)
    if response.status_code == 200:
        rev_str = response.json()["stats"]["revenue"]
        # Convert "1 200,00 €" to float
        rev_clean = rev_str.replace(" €", "").replace(" ", "").replace(",", ".")
        return float(rev_clean)
    return 0.0

def create_invoice(token, status="Draft", amount=100.00):
    headers = {"Authorization": f"Bearer {token}"}
    # Need a valid patient ID. Assuming patient 1 exists or I fetch one.
    # I'll create a dummy patient to be safe.
    pat_res = requests.post(f"{BASE_URL}/patients", headers=headers, json={
        "first_name": "Rev", "last_name": f"Test{random.randint(1000,9999)}",
        "email": f"rev{random.randint(1000,9999)}@test.com", "phone": "123", "date_of_birth": "1990-01-01"
    })
    pat_id = pat_res.json()["id"]

    data = {
        "patient_id": pat_id,
        "total_amount": amount,
        "status": status,
        "issue_date": datetime.date.today().isoformat(),
        "items": [{"description": "Test", "quantity": 1, "price": amount}]
    }
    res = requests.post(f"{BASE_URL}/invoices", headers=headers, json=data)
    if res.status_code == 201:
        return res.json()
    print(f"Create Invoice Failed: {res.text}")
    return None

def update_invoice(token, invoice_id, status):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.put(f"{BASE_URL}/invoices/{invoice_id}", headers=headers, json={"status": status})
    return res.status_code == 200

def run_verification():
    print("--- 1. Login ---")
    token = get_auth_token()
    if not token: return

    print("--- 2. Initial Revenue ---")
    initial_rev = get_revenue(token)
    print(f"Initial Revenue: {initial_rev}")

    print("--- 3. Create Draft Invoice (100.00) ---")
    inv_draft = create_invoice(token, "Draft", 100.00)
    if not inv_draft: return
    print(f"Created Invoice {inv_draft['id']} (Draft)")

    print("--- 4. Check Revenue (Should be unchanged) ---")
    rev_after_draft = get_revenue(token)
    print(f"Revenue: {rev_after_draft}")
    if rev_after_draft != initial_rev:
        print("FAIL: Revenue changed after Draft invoice!")
    else:
        print("SUCCESS: Revenue unchanged.")

    print("--- 5. Update Invoice to Paid ---")
    update_invoice(token, inv_draft['id'], "Paid")
    
    print("--- 6. Check Revenue (Should increase by 100) ---")
    rev_after_paid = get_revenue(token)
    print(f"Revenue: {rev_after_paid}")
    if abs(rev_after_paid - (initial_rev + 100.0)) < 0.01:
        print("SUCCESS: Revenue increased correctly.")
    else:
        print(f"FAIL: Revenue mismatch. Expected {initial_rev + 100.0}, got {rev_after_paid}")

    print("--- 7. Create Paid Invoice (200.00) ---")
    inv_paid = create_invoice(token, "Paid", 200.00)
    
    print("--- 8. Check Revenue (Should increase by 200) ---")
    rev_final = get_revenue(token)
    print(f"Revenue: {rev_final}")
    if abs(rev_final - (initial_rev + 300.0)) < 0.01:
        print("SUCCESS: Final Revenue correct.")
    else:
        print(f"FAIL: Revenue mismatch. Expected {initial_rev + 300.0}, got {rev_final}")

if __name__ == "__main__":
    run_verification()
