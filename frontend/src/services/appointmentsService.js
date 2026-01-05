// src/services/appointmentsService.js
import { api } from '../lib/api';

export async function fetchAppointments() {
  const res = await api.get('/api/v2/appointments');
  return res.data;
}

export async function fetchAppointment(id) {
  const res = await api.get(`/api/v2/appointments/${id}`);
  return res.data;
}

export async function createAppointment(payload) {
  const res = await api.post('/api/v2/appointments', payload);
  return res.data;
}

export async function updateAppointment(id, payload) {
  const res = await api.put(`/api/v2/appointments/${id}`, payload);
  return res.data;
}

export async function deleteAppointment(id) {
  const res = await api.delete(`/api/v2/appointments/${id}`);
  return res.data;
}
