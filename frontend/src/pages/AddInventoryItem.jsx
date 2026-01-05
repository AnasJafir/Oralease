// frontend/src/pages/AddInventoryItem.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { Save, ArrowLeft } from 'lucide-react';

const AddInventoryItem = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    quantity: 0,
    threshold: 10,
    unit: 'pièce',
    description: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/api/v2/inventory', formData);
      navigate('/inventory');
    } catch (err) {
      alert("Erreur lors de l'ajout");
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Ajouter au Stock</h1>
        <button onClick={() => navigate('/inventory')} className="text-gray-600 hover:text-gray-900 flex items-center">
          <ArrowLeft className="h-4 w-4 mr-1" /> Retour
        </button>
      </div>

      <form onSubmit={handleSubmit} className="bg-white shadow-sm ring-1 ring-gray-900/5 sm:rounded-xl p-6 space-y-6">
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
          <div className="sm:col-span-2">
            <label className="block text-sm font-medium text-gray-700">Nom de l'article</label>
            <input type="text" name="name" required className="input-field" onChange={handleChange} placeholder="Ex: Gants Latex (Taille M)" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Quantité Initiale</label>
            <input type="number" name="quantity" min="0" required className="input-field" onChange={handleChange} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Seuil d'alerte</label>
            <input type="number" name="threshold" min="0" required className="input-field" value={formData.threshold} onChange={handleChange} />
            <p className="text-xs text-gray-500 mt-1">Alerte rouge si stock inférieur à ce nombre.</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Unité</label>
            <input type="text" name="unit" className="input-field" value={formData.unit} onChange={handleChange} placeholder="boîte, litre, pièce..." />
          </div>
          <div className="sm:col-span-2">
            <label className="block text-sm font-medium text-gray-700">Description</label>
            <textarea name="description" rows={2} className="input-field" onChange={handleChange} />
          </div>
        </div>
        <div className="flex justify-end pt-4">
          <button type="submit" className="btn-primary w-auto flex items-center">
            <Save className="h-4 w-4 mr-2" /> Ajouter l'article
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddInventoryItem;