// frontend/src/pages/Treatments.jsx
import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';
import { Activity, Plus, Search, Filter } from 'lucide-react';
import { useNavigate, useSearchParams } from 'react-router-dom';

const Treatments = () => {
  const [treatments, setTreatments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const patientIdFilter = searchParams.get('patientId');

  useEffect(() => {
    const fetchTreatments = async () => {
      try {
        const response = await api.get('/api/v2/treatments');
        setTreatments(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchTreatments();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'Completed': return 'bg-green-100 text-green-800';
      case 'In Progress': return 'bg-blue-100 text-blue-800';
      case 'Cancelled': return 'bg-red-100 text-red-800';
      default: return 'bg-yellow-100 text-yellow-800';
    }
  };

  const filteredTreatments = treatments.filter(plan => {
    const patientName = plan.patient ? `${plan.patient.first_name} ${plan.patient.last_name}` : '';
    const matchesSearch = patientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      plan.diagnosis.toLowerCase().includes(searchTerm.toLowerCase());

    // Filter by patient ID if provided in URL
    const matchesPatient = patientIdFilter
      ? (plan.patient_id?.toString() === patientIdFilter || plan.patient?.id?.toString() === patientIdFilter)
      : true;

    return matchesSearch && matchesPatient;
  });

  if (loading) return <div className="p-8 text-center">Chargement...</div>;

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Suivi Clinique</h1>
          <p className="mt-1 text-sm text-gray-500">Gestion des plans de traitement en cours</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button
            onClick={() => navigate('/treatments/add')}
            className="inline-flex items-center justify-center rounded-md border border-transparent bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 sm:w-auto"
          >
            <Plus className="h-4 w-4 mr-2" /> Nouveau Traitement
          </button>
        </div>
      </div>

      {/* Filters & Search */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-brand-500 focus:border-brand-500 sm:text-sm"
            placeholder="Rechercher par patient ou diagnostic..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <button className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
          <Filter className="h-4 w-4 mr-2 text-gray-500" /> Filtres
        </button>
      </div>

      {/* Data Table */}
      <div className="bg-white shadow overflow-hidden sm:rounded-lg border border-gray-200">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Patient
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Diagnostic
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Détails du soin
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Statut
              </th>
              <th scope="col" className="relative px-6 py-3">
                <span className="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredTreatments.map((plan) => (
              <tr
                key={plan.id}
                className="hover:bg-gray-50 cursor-pointer transition"
                onClick={() => navigate(`/treatments/${plan.id}`)}
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="flex-shrink-0 h-10 w-10 rounded-full bg-brand-100 flex items-center justify-center text-brand-600 font-bold">
                      {plan.patient ? plan.patient.first_name[0] : '#'}
                    </div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-gray-900">
                        {plan.patient ? `${plan.patient.first_name} ${plan.patient.last_name}` : `Patient #${plan.patient_id}`}
                      </div>
                      <div className="text-sm text-gray-500">
                        ID: {plan.id}
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="text-sm text-gray-900 font-medium">{plan.diagnosis}</div>
                </td>
                <td className="px-6 py-4">
                  <div className="text-sm text-gray-500 line-clamp-2 max-w-xs">{plan.treatment_details}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(plan.status)}`}>
                    {plan.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button onClick={(e) => { e.stopPropagation(); navigate(`/treatments/${plan.id}`); }} className="text-brand-600 hover:text-brand-900">
                    Voir
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filteredTreatments.length === 0 && (
          <div className="text-center py-10 text-gray-500">
            Aucun traitement trouvé.
          </div>
        )}
      </div>
    </div>
  );
};

export default Treatments;