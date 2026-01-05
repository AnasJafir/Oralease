// src/services/authService.js
import { api } from '../lib/api';

export async function login(username, password) {
  try {
    const res = await api.post('/api/auth/login', { username, password });
    if (res.status !== 200 || !res.data.access_token) {
      throw new Error(res.data.msg || 'Réponse inattendue du serveur');
    }
    const { access_token, role } = res.data;
    localStorage.setItem('token', access_token);
    localStorage.setItem('role', role);
    api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    return { token: access_token, role };
  } catch (err) {
    const message = err.response?.data?.msg || err.message || 'Erreur inconnue';
    throw new Error(message);
  }
}

export function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  delete api.defaults.headers.common['Authorization'];
}

export function initAuth() {
  const token = localStorage.getItem('token');
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    return { token, role: localStorage.getItem('role') };
  }
  return null;
}
