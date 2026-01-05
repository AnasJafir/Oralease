// src/services/treatmentsService.js
import { api } from '../lib/api';

export async function fetchTreatments(patientId = null) {
  const url = patientId 
    ? `/api/v2/treatments?patient_id=${patientId}` 
    : '/api/v2/treatments';
  const res = await api.get(url);
  return res.data;
}

export async function fetchTreatment(id) {
  const res = await api.get(`/api/v2/treatments/${id}`);
  return res.data;
}

export async function createTreatment(payload) {
  const res = await api.post('/api/v2/treatments', payload);
  return res.data;
}

export async function updateTreatment(id, payload) {
  const res = await api.put(`/api/v2/treatments/${id}`, payload);
  return res.data;
}

export async function deleteTreatment(id) {
  const res = await api.delete(`/api/v2/treatments/${id}`);
  return res.data;
}
