// frontend/src/pages/Inventory.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { Plus, Package, AlertTriangle, Trash2, Edit2 } from 'lucide-react';

const Inventory = () => {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  // ... (états)

  // ... (useEffect, fetch, delete)

  // ...

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        {/* ... Titre ... */}
        <div>
            <h1 className="text-2xl font-bold text-gray-900">Inventaire</h1>
            <p className="mt-2 text-sm text-gray-700">Suivi du matériel.</p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button 
            className="btn-primary flex items-center gap-2"
            onClick={() => navigate('/inventory/add')} // NAVIGATION ACTIVÉE
          >
            <Plus className="h-4 w-4" /> Nouvel Article
          </button>
        </div>
      </div>

      {/* ... Tableau stock inchangé ... */}
      
    </div>
  );
};

export default Inventory;