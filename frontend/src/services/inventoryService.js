// src/services/inventoryService.js
import { api } from '../lib/api';

export async function fetchInventory() {
  const res = await api.get('/api/v2/inventory');
  return res.data;
}

export async function fetchInventoryItem(id) {
  const res = await api.get(`/api/v2/inventory/${id}`);
  return res.data;
}

export async function createInventoryItem(payload) {
  const res = await api.post('/api/v2/inventory', payload);
  return res.data;
}

export async function updateInventoryItem(id, payload) {
  const res = await api.put(`/api/v2/inventory/${id}`, payload);
  return res.data;
}

export async function deleteInventoryItem(id) {
  const res = await api.delete(`/api/v2/inventory/${id}`);
  return res.data;
}
