import { api } from '../lib/api';

export async function fetchInvoices(patientId = null) {
  const url = patientId 
    ? `/api/v2/invoices?patient_id=${patientId}` 
    : '/api/v2/invoices';
  const res = await api.get(url);
  return res.data;
}

export async function fetchInvoice(id) {
  const res = await api.get(`/api/v2/invoices/${id}`);
  return res.data;
}

export async function createInvoice(payload) {
  const res = await api.post('/api/v2/invoices', payload);
  return res.data;
}

export async function updateInvoice(id, payload) {
  const res = await api.put(`/api/v2/invoices/${id}`, payload);
  return res.data;
}

export async function deleteInvoice(id) {
  const res = await api.delete(`/api/v2/invoices/${id}`);
  return res.data;
}
