// frontend/src/pages/Inventory.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Search, Package, AlertTriangle, Pencil, Trash2, Loader2 } from 'lucide-react';
import { fetchInventory, deleteInventoryItem } from '../services/inventoryService';

const Inventory = () => {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState('');
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const data = await fetchInventory();
        setItems(Array.isArray(data) ? data : []);
      } catch (e) {
        setError(e.message || 'Erreur de chargement');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const filtered = items.filter(item => {
    const q = query.toLowerCase();
    return item.name?.toLowerCase().includes(q);
  });

  const handleDelete = async (id) => {
    if (!window.confirm('Supprimer cet article ?')) return;
    try {
      setDeletingId(id);
      await deleteInventoryItem(id);
      setItems(items.filter(i => i.id !== id));
    } catch (e) {
      alert(e.message || 'Erreur suppression');
    } finally {
      setDeletingId(null);
    }
  };

  const isLowStock = (item) => item.quantity <= item.threshold;

  return (
    <div className="space-y-8">
      <header className="sm:flex sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-extrabold text-brand-800 tracking-tight">Inventaire</h1>
          <p className="mt-2 text-sm text-brand-600">Gestion du stock et des fournitures.</p>
        </div>
        <div className="mt-4 sm:mt-0 flex gap-3">
          <div className="relative">
            <Search className="h-4 w-4 absolute left-3 top-1/2 -translate-y-1/2 text-brand-400" />
            <input
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Recherche (nom article)"
              className="pl-9 pr-3 py-2 rounded-md border border-brand-200 focus:border-brand-400 focus:ring-brand-400 text-sm w-56"
            />
          </div>
          <button
            type="button"
            className="flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold px-4 py-2 rounded-md shadow-sm"
            onClick={() => navigate('/inventory/add')}
          >
            <Plus className="h-4 w-4" /> Nouvel Article
          </button>
        </div>
      </header>

      {error && <div className="p-3 rounded-md bg-danger-500/10 text-danger-600 text-sm">{error}</div>}

      {loading ? (
        <div className="flex justify-center py-12"><Loader2 className="h-8 w-8 animate-spin text-brand-600" /></div>
      ) : filtered.length === 0 ? (
        <div className="border border-dashed border-brand-200 rounded-lg p-12 text-center">
          <p className="text-brand-700 font-medium">Aucun article trouvé</p>
          <p className="text-xs text-brand-500 mt-1">Ajoutez votre premier article d'inventaire.</p>
        </div>
      ) : (
        <div className="overflow-hidden rounded-xl border border-brand-200 shadow-sm bg-white">
          <table className="min-w-full divide-y divide-brand-100 text-sm">
            <thead className="bg-brand-50">
              <tr className="text-xs uppercase tracking-wide text-brand-600">
                <th className="px-4 py-3 text-left">Article</th>
                <th className="px-4 py-3 text-left">Unité</th>
                <th className="px-4 py-3 text-left">Quantité</th>
                <th className="px-4 py-3 text-left">Seuil d'alerte</th>
                <th className="px-4 py-3 text-left">Prix vente</th>
                <th className="px-4 py-3 text-left">Statut</th>
                <th className="px-4 py-3 text-left">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-brand-100">
              {filtered.map(item => {
                const lowStock = isLowStock(item);
                return (
                  <tr key={item.id} className="hover:bg-brand-50/50">
                    <td className="px-4 py-3 font-medium text-brand-800">
                      <div className="flex items-center gap-2">
                        <Package className="h-4 w-4 text-brand-400" />
                        {item.name}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-brand-700">{item.unit || '-'}</td>
                    <td className="px-4 py-3 text-brand-700 font-semibold">{item.quantity}</td>
                    <td className="px-4 py-3 text-brand-700">{item.threshold}</td>
                    <td className="px-4 py-3 text-brand-700">
                      {item.sell_price != null
                        ? `${Number(item.sell_price).toFixed(2)} €`
                        : '-'}
                    </td>
                    <td className="px-4 py-3">
                      {lowStock ? (
                        <span className="flex items-center gap-1 text-xs font-medium text-warning-600">
                          <AlertTriangle className="h-4 w-4" /> Stock bas
                        </span>
                      ) : (
                        <span className="text-xs font-medium text-success-600">OK</span>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        <button
                          onClick={() => navigate(`/inventory/${item.id}/edit`)}
                          className="text-accent-500 hover:text-accent-600"
                          title="Modifier"
                        >
                          <Pencil className="h-4 w-4" />
                        </button>
                        <button
                          disabled={deletingId === item.id}
                          onClick={() => handleDelete(item.id)}
                          className="text-danger-500 hover:text-danger-600 disabled:opacity-50"
                          title="Supprimer"
                        >
                          {deletingId === item.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <Trash2 className="h-4 w-4" />}
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

export default Inventory;
