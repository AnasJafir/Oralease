// src/services/patientsService.js
import { api } from '../lib/api';

export async function fetchPatients() {
  const res = await api.get('/api/v2/patients');
  return res.data; // marshmallow returns decrypted fields
}

export async function createPatient(payload) {
  const res = await api.post('/api/v2/patients', payload);
  return res.data;
}

export async function updatePatient(id, payload) {
  const res = await api.put(`/api/v2/patients/${id}`, payload);
  return res.data;
}

export async function deletePatient(id) {
  const res = await api.delete(`/api/v2/patients/${id}`);
  return res.data;
}
