// frontend/src/pages/AddInventoryItem.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Save, Loader2 } from 'lucide-react';
import { createInventoryItem } from '../services/inventoryService';

const AddInventoryItem = () => {
  const navigate = useNavigate();
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    name: '',
    quantity: '',
    threshold: '25',
    unit: '',
    description: '',
    sell_price: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      await createInventoryItem({
        name: form.name,
        quantity: parseInt(form.quantity),
        threshold: parseInt(form.threshold),
        unit: form.unit || null,
        description: form.description || null,
        sell_price: form.sell_price ? parseFloat(form.sell_price) : null
      });
      navigate('/inventory');
    } catch (e) {
      alert(e.message || 'Erreur lors de la création');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <button onClick={() => navigate('/inventory')} className="flex items-center gap-2 text-brand-600 hover:text-brand-800 transition-colors">
          <ArrowLeft className="h-4 w-4" /> Retour
        </button>
        <div>
          <h1 className="text-2xl font-bold text-brand-800">Nouvel article</h1>
          <p className="text-sm text-brand-600 mt-1">Ajouter un article à l'inventaire</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-card border border-brand-100 p-6">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Nom de l'article *</label>
            <input
              required
              value={form.name}
              onChange={e => setForm({ ...form, name: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
              placeholder="Ex: Gants latex taille M"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-brand-700 mb-1">Quantité *</label>
              <input
                required
                type="number"
                min="0"
                value={form.quantity}
                onChange={e => setForm({ ...form, quantity: e.target.value })}
                className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-brand-700 mb-1">Seuil d'alerte *</label>
              <input
                required
                type="number"
                min="0"
                value={form.threshold}
                onChange={e => setForm({ ...form, threshold: e.target.value })}
                className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
              />
              <p className="text-xs text-brand-500 mt-1">Alerte si quantité ≤ seuil</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-brand-700 mb-1">Unité</label>
              <input
                value={form.unit}
                onChange={e => setForm({ ...form, unit: e.target.value })}
                className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
                placeholder="Ex: boîte, pièce"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-brand-700 mb-1">Prix de vente unitaire</label>
              <input
                type="number"
                min="0"
                step="0.01"
                value={form.sell_price}
                onChange={e => setForm({ ...form, sell_price: e.target.value })}
                className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
                placeholder="Ex: 50.00"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Description</label>
            <textarea
              value={form.description}
              onChange={e => setForm({ ...form, description: e.target.value })}
              className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400"
              rows={3}
              placeholder="Notes internes sur l'article, référence fournisseur, etc."
            />
          </div>
        </div>

        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate('/inventory')}
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
            Ajouter
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddInventoryItem;
