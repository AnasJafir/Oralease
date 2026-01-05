// frontend/src/pages/Patients.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, FileText, Pencil, Trash2, Phone, Mail, Loader2 } from 'lucide-react';
import { fetchPatients, deletePatient } from '../services/patientsService';

const Patients = () => {
  const navigate = useNavigate(); // Hook de navigation
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState('');
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const data = await fetchPatients();
        setPatients(Array.isArray(data) ? data : []);
      } catch (e) {
        setError(e.message || 'Erreur de chargement');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const filtered = patients.filter(p => {
    const q = query.toLowerCase();
    return (
      p.first_name?.toLowerCase().includes(q) ||
      p.last_name?.toLowerCase().includes(q) ||
      p.email?.toLowerCase().includes(q)
    );
  });

  const handleDelete = async (id) => {
    if (!window.confirm('Supprimer ce patient ?')) return;
    try {
      setDeletingId(id);
      await deletePatient(id);
      setPatients(patients.filter(p => p.id !== id));
    } catch (e) {
      alert(e.message || 'Erreur suppression');
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="space-y-8">
      <header className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-extrabold text-brand-800 tracking-tight">Dossiers Patients</h1>
          <p className="mt-2 text-sm text-brand-600">Accès sécurisé aux informations cliniques.</p>
        </div>
        <div className="mt-4 sm:mt-0 flex gap-3">
          <div className="relative">
            <Search className="h-4 w-4 absolute left-3 top-1/2 -translate-y-1/2 text-brand-400" />
            <input
              value={query}
              onChange={e=>setQuery(e.target.value)}
              placeholder="Recherche (nom, email)"
              className="pl-9 pr-3 py-2 rounded-md border border-brand-200 focus:border-brand-400 focus:ring-brand-400 text-sm w-56"
            />
          </div>
          <button
            type="button"
            className="flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold px-4 py-2 rounded-md shadow-sm"
            onClick={() => navigate('/patients/add')}
          >
            <Plus className="h-4 w-4" /> Nouveau
          </button>
        </div>
      </header>

      {error && <div className="p-3 rounded-md bg-danger-500/10 text-danger-600 text-sm">{error}</div>}

      {loading ? (
        <div className="flex justify-center py-12"><Loader2 className="h-8 w-8 animate-spin text-brand-600" /></div>
      ) : filtered.length === 0 ? (
        <div className="border border-dashed border-brand-200 rounded-lg p-12 text-center">
          <p className="text-brand-700 font-medium">Aucun patient trouvé</p>
          <p className="text-xs text-brand-500 mt-1">Ajoutez votre premier patient pour commencer.</p>
        </div>
      ) : (
        <div className="overflow-hidden rounded-xl border border-brand-200 shadow-sm bg-white">
          <table className="min-w-full divide-y divide-brand-100 text-sm">
            <thead className="bg-brand-50">
              <tr className="text-xs uppercase tracking-wide text-brand-600">
                <th className="px-4 py-3 text-left">Nom</th>
                <th className="px-4 py-3 text-left">Naissance</th>
                <th className="px-4 py-3 text-left">Téléphone</th>
                <th className="px-4 py-3 text-left">Email</th>
                <th className="px-4 py-3 text-left">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-brand-100">
              {filtered.map(p => (
                <tr key={p.id} className="hover:bg-brand-50/50">
                  <td className="px-4 py-3 font-medium text-brand-800">{p.first_name} {p.last_name}</td>
                  <td className="px-4 py-3 text-brand-700">{p.date_of_birth}</td>
                  <td className="px-4 py-3 text-brand-700">
                    <div className="flex items-center gap-2">
                      <Phone className="h-4 w-4 text-brand-400" /> 
                      <span>{p.contact_number || '—'}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-brand-700">
                    <div className="flex items-center gap-2">
                      <Mail className="h-4 w-4 text-brand-400" /> 
                      <span>{p.email || '—'}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-3">
                      <button 
                        onClick={() => navigate(`/patients/${p.id}`)}
                        className="text-brand-600 hover:text-brand-800 transition-colors" 
                        title="Voir dossier"
                      >
                        <FileText className="h-4 w-4" />
                      </button>
                      <button 
                        onClick={() => navigate(`/patients/${p.id}/edit`)}
                        className="text-accent-500 hover:text-accent-600 transition-colors" 
                        title="Modifier"
                      >
                        <Pencil className="h-4 w-4" />
                      </button>
                      <button
                        disabled={deletingId===p.id}
                        onClick={()=>handleDelete(p.id)}
                        className="text-danger-500 hover:text-danger-600 disabled:opacity-50 transition-colors"
                        title="Supprimer"
                      >
                        {deletingId===p.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Trash2 className="h-4 w-4" />}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Patients;