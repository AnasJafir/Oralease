// frontend/src/pages/Appointments.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, User, Clock, Pencil, Trash2, Loader2 } from 'lucide-react';
import { fetchAppointments, deleteAppointment } from '../services/appointmentsService';
import { fetchPatients } from '../services/patientsService';

const Appointments = () => {
  const navigate = useNavigate();
  const [appointments, setAppointments] = useState([]);
  const [patients, setPatients] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState('');
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const [appointmentsData, patientsData] = await Promise.all([
          fetchAppointments(),
          fetchPatients()
        ]);

        setAppointments(Array.isArray(appointmentsData) ? appointmentsData : []);

        // Créer un mapping patient_id -> patient
        const patientMap = {};
        if (Array.isArray(patientsData)) {
          patientsData.forEach(p => {
            patientMap[p.id] = p;
          });
        }
        setPatients(patientMap);
      } catch (e) {
        setError(e.message || 'Erreur de chargement');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const filtered = appointments.filter(apt => {
    const q = query.toLowerCase();
    const patient = patients[apt.patient_id];
    return (
      patient?.first_name?.toLowerCase().includes(q) ||
      patient?.last_name?.toLowerCase().includes(q) ||
      apt.notes?.toLowerCase().includes(q)
    );
  });

  const handleDelete = async (id) => {
    if (!window.confirm('Supprimer ce rendez-vous ?')) return;
    try {
      setDeletingId(id);
      await deleteAppointment(id);
      setAppointments(appointments.filter(a => a.id !== id));
    } catch (e) {
      alert(e.message || 'Erreur suppression');
    } finally {
      setDeletingId(null);
    }
  };

  const formatDate = (dateStr) => {
    const d = new Date(dateStr);
    return d.toLocaleString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="space-y-8">
      <header className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-extrabold text-brand-800 tracking-tight">Agenda</h1>
          <p className="mt-2 text-sm text-brand-600">Gestion des rendez-vous patients.</p>
        </div>
        <div className="mt-4 sm:mt-0 flex gap-3">
          <div className="relative">
            <Search className="h-4 w-4 absolute left-3 top-1/2 -translate-y-1/2 text-brand-400" />
            <input
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Recherche (patient, notes)"
              className="pl-9 pr-3 py-2 rounded-md border border-brand-200 focus:border-brand-400 focus:ring-brand-400 text-sm w-56"
            />
          </div>
          <button
            type="button"
            className="flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold px-4 py-2 rounded-md shadow-sm"
            onClick={() => navigate('/appointments/add')}
          >
            <Plus className="h-4 w-4" /> Nouveau RDV
          </button>
        </div>
      </header>

      {error && <div className="p-3 rounded-md bg-danger-500/10 text-danger-600 text-sm">{error}</div>}

      {loading ? (
        <div className="flex justify-center py-12"><Loader2 className="h-8 w-8 animate-spin text-brand-600" /></div>
      ) : filtered.length === 0 ? (
        <div className="border border-dashed border-brand-200 rounded-lg p-12 text-center">
          <p className="text-brand-700 font-medium">Aucun rendez-vous trouvé</p>
          <p className="text-xs text-brand-500 mt-1">Planifiez votre premier rendez-vous.</p>
        </div>
      ) : (
        <div className="overflow-hidden rounded-xl border border-brand-200 shadow-sm bg-white">
          <table className="min-w-full divide-y divide-brand-100 text-sm">
            <thead className="bg-brand-50">
              <tr className="text-xs uppercase tracking-wide text-brand-600">
                <th className="px-4 py-3 text-left">Patient</th>
                <th className="px-4 py-3 text-left">Date & Heure</th>
                <th className="px-4 py-3 text-left">Type</th>
                <th className="px-4 py-3 text-left">Statut</th>
                <th className="px-4 py-3 text-left">Notes</th>
                <th className="px-4 py-3 text-left">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-brand-100">
              {filtered.map(apt => {
                const patient = patients[apt.patient_id];
                const getStatusColor = (s) => {
                  switch (s) {
                    case 'Confirmed': return 'bg-green-100 text-green-800';
                    case 'Completed': return 'bg-blue-100 text-blue-800';
                    case 'Cancelled': return 'bg-red-100 text-red-800';
                    case 'No Show': return 'bg-orange-100 text-orange-800';
                    default: return 'bg-gray-100 text-gray-800'; // Scheduled
                  }
                };

                return (
                  <tr key={apt.id} className="hover:bg-brand-50/50">
                    <td className="px-4 py-3 font-medium text-brand-800">
                      <div className="flex items-center gap-2">
                        <User className="h-4 w-4 text-brand-400" />
                        {patient ? `${patient.first_name} ${patient.last_name}` : `Patient #${apt.patient_id}`}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-brand-700">
                      <div className="flex items-center gap-2">
                        <Clock className="h-4 w-4 text-brand-400" />
                        {formatDate(apt.appointment_date)}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-brand-700">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-brand-50 text-brand-700 border border-brand-100">
                        {apt.type}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-brand-700">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(apt.status)}`}>
                        {apt.status === 'Confirmed' ? 'Confirmé' :
                          apt.status === 'Completed' ? 'Terminé' :
                            apt.status === 'Cancelled' ? 'Annulé' :
                              apt.status === 'No Show' ? 'Absent' : 'Programmé'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-brand-700">
                      {apt.notes ? (
                        <span className="text-sm">{apt.notes.substring(0, 50)}{apt.notes.length > 50 ? '...' : ''}</span>
                      ) : '—'}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        <button
                          onClick={() => navigate(`/appointments/${apt.id}/edit`)}
                          className="text-accent-500 hover:text-accent-600"
                          title="Modifier"
                        >
                          <Pencil className="h-4 w-4" />
                        </button>
                        <button
                          disabled={deletingId === apt.id}
                          onClick={() => handleDelete(apt.id)}
                          className="text-danger-500 hover:text-danger-600 disabled:opacity-50"
                          title="Supprimer"
                        >
                          {deletingId === apt.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Trash2 className="h-4 w-4" />}
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Appointments;