// frontend/src/pages/AddAppointment.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, Loader2 } from 'lucide-react';
import { createAppointment } from '../services/appointmentsService';
import { fetchPatients } from '../services/patientsService';

const AddAppointment = () => {
  const navigate = useNavigate();
  const [saving, setSaving] = useState(false);
  const [patients, setPatients] = useState([]);
  const [loadingPatients, setLoadingPatients] = useState(true);
  const [form, setForm] = useState({
    patient_id: '',
    appointment_date: '',
    type: 'Consultation',
    status: 'Scheduled',
    notes: ''
  });

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchPatients();
        setPatients(Array.isArray(data) ? data : []);
      } catch (e) {
        console.error('Erreur chargement patients:', e);
      } finally {
        setLoadingPatients(false);
      }
    };
    load();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      await createAppointment({
        ...form,
        patient_id: parseInt(form.patient_id)
      });
      navigate('/appointments');
    } catch (e) {
      alert(e.message || 'Erreur lors de la création');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <button onClick={() => navigate('/appointments')} className="flex items-center gap-2 text-brand-600 hover:text-brand-800 transition-colors">
          <ArrowLeft className="h-4 w-4" /> Retour
        </button>
        <div>
          <h1 className="text-2xl font-bold text-brand-800">Nouveau rendez-vous</h1>
          <p className="text-sm text-brand-600 mt-1">Planifier un rendez-vous patient</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-card border border-brand-100 p-6">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Patient *</label>
            {loadingPatients ? (
              <div className="text-sm text-brand-500">Chargement...</div>
            ) : (
              <select
                required
                value={form.patient_id}
                onChange={e => setForm({ ...form, patient_id: e.target.value })}
                className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
              >
                <option value="">Sélectionner un patient</option>
                {patients.map(p => (
                  <option key={p.id} value={p.id}>
                    {p.first_name} {p.last_name}
                  </option>
                ))}
              </select>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Date et heure *</label>
            <input
              required
              type="datetime-local"
              value={form.appointment_date}
              onChange={e => setForm({ ...form, appointment_date: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Type de rendez-vous *</label>
            <select
              required
              value={form.type}
              onChange={e => setForm({ ...form, type: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
            >
              <option value="Consultation">Consultation</option>
              <option value="Détartrage">Détartrage</option>
              <option value="Urgence">Urgence</option>
              <option value="Chirurgie">Chirurgie</option>
              <option value="Orthodontie">Orthodontie</option>
              <option value="Autre">Autre</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Statut *</label>
            <select
              required
              value={form.status}
              onChange={e => setForm({ ...form, status: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
            >
              <option value="Scheduled">Programmé</option>
              <option value="Confirmed">Confirmé</option>
              <option value="Cancelled">Annulé</option>
              <option value="Completed">Terminé</option>
              <option value="No Show">Absent</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Notes</label>
            <textarea
              rows={4}
              value={form.notes}
              onChange={e => setForm({ ...form, notes: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
              placeholder="Raison de la visite, procédures prévues..."
            />
          </div>
        </div>

        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate('/appointments')}
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
            Créer
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddAppointment;