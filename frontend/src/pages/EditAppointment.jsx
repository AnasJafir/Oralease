// frontend/src/pages/EditAppointment.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, Loader2 } from 'lucide-react';
import { fetchAppointment, updateAppointment } from '../services/appointmentsService';
import { fetchPatients } from '../services/patientsService';

const EditAppointment = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [patients, setPatients] = useState([]);
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
        setLoading(true);
        const [aptData, patientsData] = await Promise.all([
          fetchAppointment(id),
          fetchPatients()
        ]);

        setPatients(Array.isArray(patientsData) ? patientsData : []);

        // Convertir la date ISO en format datetime-local
        const dateObj = new Date(aptData.appointment_date);
        const localDate = new Date(dateObj.getTime() - dateObj.getTimezoneOffset() * 60000)
          .toISOString()
          .slice(0, 16);

        setForm({
          patient_id: aptData.patient_id || '',
          appointment_date: localDate,
          type: aptData.type || 'Consultation',
          status: aptData.status || 'Scheduled',
          notes: aptData.notes || ''
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
      await updateAppointment(id, {
        ...form,
        patient_id: parseInt(form.patient_id)
      });
      navigate('/appointments');
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
        <button onClick={() => navigate('/appointments')} className="flex items-center gap-2 text-brand-600 hover:text-brand-800">
          <ArrowLeft className="h-4 w-4" /> Retour
        </button>
        <div className="p-4 rounded-md bg-danger-500/10 text-danger-600">{error}</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <button onClick={() => navigate('/appointments')} className="flex items-center gap-2 text-brand-600 hover:text-brand-800 transition-colors">
          <ArrowLeft className="h-4 w-4" /> Annuler
        </button>
        <div>
          <h1 className="text-2xl font-bold text-brand-800">Modifier le rendez-vous</h1>
          <p className="text-sm text-brand-600 mt-1">RDV #{id}</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-card border border-brand-100 p-6">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Patient *</label>
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
            Enregistrer
          </button>
        </div>
      </form>
    </div>
  );
};

export default EditAppointment;
