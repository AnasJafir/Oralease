// frontend/src/pages/AddPatient.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { Save, ArrowLeft } from 'lucide-react';

const AddPatient = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    date_of_birth: '',
    contact_number: '',
    email: '',
    medical_history: ''
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/api/v2/patients', formData);
      navigate('/patients'); // Retour à la liste après succès
    } catch (err) {
      setError(err.response?.data?.message || "Erreur lors de la création");
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Nouveau Patient</h1>
        <button onClick={() => navigate('/patients')} className="text-gray-600 hover:text-gray-900 flex items-center">
          <ArrowLeft className="h-4 w-4 mr-1" /> Retour
        </button>
      </div>

      <form onSubmit={handleSubmit} className="bg-white shadow-sm ring-1 ring-gray-900/5 sm:rounded-xl p-6 space-y-6">
        {error && <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm">{error}</div>}
        
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div>
            <label className="block text-sm font-medium text-gray-700">Prénom</label>
            <input type="text" name="first_name" required className="input-field" onChange={handleChange} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Nom</label>
            <input type="text" name="last_name" required className="input-field" onChange={handleChange} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Date de Naissance</label>
            <input type="date" name="date_of_birth" required className="input-field" onChange={handleChange} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Téléphone</label>
            <input type="tel" name="contact_number" required className="input-field" onChange={handleChange} />
          </div>
          <div className="sm:col-span-2">
            <label className="block text-sm font-medium text-gray-700">Email</label>
            <input type="email" name="email" required className="input-field" onChange={handleChange} />
          </div>
          <div className="sm:col-span-2">
            <label className="block text-sm font-medium text-gray-700">Antécédents Médicaux</label>
            <textarea name="medical_history" rows={4} className="input-field" onChange={handleChange} placeholder="Allergies, traitements en cours..." />
          </div>
        </div>

        <div className="flex justify-end pt-4">
          <button type="submit" className="btn-primary w-auto flex items-center">
            <Save className="h-4 w-4 mr-2" /> Enregistrer le dossier
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddPatient;