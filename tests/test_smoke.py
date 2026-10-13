# tests/test_smoke.py
"""
Tests de fumée : le harnais démarre l'app et l'authentification fonctionne.
Ce ne sont PAS les tests de la fonctionnalité (détection de conflit) — juste
la preuve que l'environnement de test est câblé.
"""


def test_status_endpoint_is_public(client):
    resp = client.get("/status")
    assert resp.status_code == 200
    assert resp.get_json()["status"].startswith("API V2")


def test_protected_endpoint_reachable_with_token(client, auth):
    resp = client.get("/api/v2/appointments", headers=auth("doctor"))
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_patient_fixture_persists(client, patient):
    assert patient.id is not None
