// frontend/src/pages/EditPatient.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, Loader2 } from 'lucide-react';
import { api } from '../lib/api';
import { updatePatient } from '../services/patientsService';

const EditPatient = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({
    first_name: '',
    last_name: '',
    date_of_birth: '',
    contact_number: '',
    email: '',
    medical_history: ''
  });

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/api/v2/patients/${id}`);
        setForm({
          first_name: res.data.first_name || '',
          last_name: res.data.last_name || '',
          date_of_birth: res.data.date_of_birth || '',
          contact_number: res.data.contact_number || '',
          email: res.data.email || '',
          medical_history: res.data.medical_history || ''
        });
      } catch (e) {
        setError(e.message || 'Erreur de chargement');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      await updatePatient(id, form);
      navigate(`/patients/${id}`);
    } catch (e) {
      alert(e.message || 'Erreur lors de la modification');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-brand-600" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        <button onClick={() => navigate('/patients')} className="flex items-center gap-2 text-brand-600 hover:text-brand-800">
          <ArrowLeft className="h-4 w-4" /> Retour
        </button>
        <div className="p-4 rounded-md bg-danger-500/10 text-danger-600">{error}</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <button onClick={() => navigate(`/patients/${id}`)} className="flex items-center gap-2 text-brand-600 hover:text-brand-800 transition-colors">
          <ArrowLeft className="h-4 w-4" /> Annuler
        </button>
        <div>
          <h1 className="text-2xl font-bold text-brand-800">Modifier le patient</h1>
          <p className="text-sm text-brand-600 mt-1">Dossier #{id}</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-card border border-brand-100 p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Prénom *</label>
            <input
              required
              value={form.first_name}
              onChange={e => setForm({ ...form, first_name: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Nom *</label>
            <input
              required
              value={form.last_name}
              onChange={e => setForm({ ...form, last_name: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Date de naissance *</label>
            <input
              required
              type="date"
              value={form.date_of_birth}
              onChange={e => setForm({ ...form, date_of_birth: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Téléphone *</label>
            <input
              required
              value={form.contact_number}
              onChange={e => setForm({ ...form, contact_number: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-brand-700 mb-1">Email *</label>
            <input
              required
              type="email"
              value={form.email}
              onChange={e => setForm({ ...form, email: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-brand-700 mb-1">Historique médical</label>
            <textarea
              rows={4}
              value={form.medical_history}
              onChange={e => setForm({ ...form, medical_history: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
              placeholder="Antécédents médicaux, conditions, traitements en cours..."
            />
          </div>
        </div>

        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate(`/patients/${id}`)}
            className="px-4 py-2 border border-brand-200 text-brand-700 rounded-md hover:bg-brand-50 transition-colors"
          >
            Annuler
          </button>
          <button
            type="submit"
            disabled={saving}
            className="flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 rounded-md font-semibold disabled:opacity-50 transition-colors"
          >
            {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
            Enregistrer
          </button>
        </div>
      </form>
    </div>
  );
};

export default EditPatient;
