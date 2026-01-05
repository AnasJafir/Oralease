// frontend/src/pages/ViewPatient.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Phone, Mail, Calendar, FileText, Pencil, Loader2 } from 'lucide-react';
import { api } from '../lib/api';

const ViewPatient = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [patient, setPatient] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/api/v2/patients/${id}`);
        setPatient(res.data);
      } catch (e) {
        setError(e.message || 'Erreur de chargement');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

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

  if (!patient) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <button onClick={() => navigate('/patients')} className="flex items-center gap-2 text-brand-600 hover:text-brand-800 transition-colors">
          <ArrowLeft className="h-4 w-4" /> Retour à la liste
        </button>
        <button 
          onClick={() => navigate(`/patients/${id}/edit`)}
          className="flex items-center gap-2 bg-accent-500 hover:bg-accent-600 text-white px-4 py-2 rounded-md text-sm font-semibold transition-colors"
        >
          <Pencil className="h-4 w-4" /> Modifier
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-card border border-brand-100 overflow-hidden">
        <div className="bg-gradient-to-r from-brand-600 to-brand-700 p-6 text-white">
          <h1 className="text-2xl font-bold">{patient.first_name} {patient.last_name}</h1>
          <p className="text-brand-100 text-sm mt-1">Dossier Patient #{patient.id}</p>
        </div>

        <div className="p-6 space-y-6">
          {/* Informations personnelles */}
          <section>
            <h2 className="text-lg font-semibold text-brand-800 mb-4 flex items-center gap-2">
              <FileText className="h-5 w-5 text-brand-500" />
              Informations personnelles
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-medium text-brand-500 uppercase tracking-wide">Date de naissance</label>
                <div className="flex items-center gap-2 mt-1 text-brand-800">
                  <Calendar className="h-4 w-4 text-brand-400" />
                  <span>{patient.date_of_birth}</span>
                </div>
              </div>
              <div>
                <label className="text-xs font-medium text-brand-500 uppercase tracking-wide">Téléphone</label>
                <div className="flex items-center gap-2 mt-1 text-brand-800">
                  <Phone className="h-4 w-4 text-brand-400" />
                  <span>{patient.contact_number || '—'}</span>
                </div>
              </div>
              <div className="md:col-span-2">
                <label className="text-xs font-medium text-brand-500 uppercase tracking-wide">Email</label>
                <div className="flex items-center gap-2 mt-1 text-brand-800">
                  <Mail className="h-4 w-4 text-brand-400" />
                  <span>{patient.email || '—'}</span>
                </div>
              </div>
            </div>
          </section>

          {/* Historique médical */}
          {patient.medical_history && (
            <section>
              <h2 className="text-lg font-semibold text-brand-800 mb-4">Historique médical</h2>
              <div className="bg-brand-50 rounded-lg p-4 text-brand-700 whitespace-pre-wrap">
                {patient.medical_history}
              </div>
            </section>
          )}
        </div>
      </div>
    </div>
  );
};

export default ViewPatient;
