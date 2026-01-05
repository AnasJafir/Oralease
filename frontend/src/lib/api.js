// frontend/src/lib/api.js
import axios from 'axios';

// Base URL configurable via variable d'environnement Vite
// Use relative path by default to leverage Vite proxy in dev
const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Intercepteur pour gérer les erreurs globales (ex: Token expiré)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      if (error.response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        window.location.href = '/login';
      }
    } else {
      console.error('Erreur réseau ou serveur injoignable');
    }
    return Promise.reject(error);
  }
);