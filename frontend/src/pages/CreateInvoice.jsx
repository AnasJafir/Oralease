import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createInvoice } from '../services/invoicesService';
import { fetchPatients } from '../services/patientsService';
import { fetchTreatments } from '../services/treatmentsService';
import { ArrowLeft, Save, Plus, Trash2 } from 'lucide-react';

const CreateInvoice = () => {
    const navigate = useNavigate();
    const [patients, setPatients] = useState([]);
    const [treatments, setTreatments] = useState([]);
    const [formData, setFormData] = useState({
        patient_id: '',
        treatment_plan_id: '',
        status: 'Draft',
        items: [{ description: '', quantity: 1, price: 0 }]
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadPatients = async () => {
            try {
                const data = await fetchPatients();
                setPatients(data);
            } catch (err) {
                console.error("Error loading patients", err);
            }
        };
        loadPatients();
    }, []);

    // Load treatments when patient changes
    useEffect(() => {
        const loadTreatments = async () => {
            if (formData.patient_id) {
                try {
                    const data = await fetchTreatments(formData.patient_id);
                    setTreatments(data);
                } catch (err) {
                    console.error("Error loading treatments", err);
                    setTreatments([]);
                }
            } else {
                setTreatments([]);
            }
        };
        loadTreatments();
    }, [formData.patient_id]);

    const handleItemChange = (index, field, value) => {
        const newItems = [...formData.items];
        newItems[index][field] = value;
        setFormData({ ...formData, items: newItems });
    };

    const addItem = () => {
        setFormData({
            ...formData,
            items: [...formData.items, { description: '', quantity: 1, price: 0 }]
        });
    };

    const removeItem = (index) => {
        const newItems = formData.items.filter((_, i) => i !== index);
        setFormData({ ...formData, items: newItems });
    };

    const calculateTotal = () => {
        return formData.items.reduce((sum, item) => sum + (item.quantity * item.price), 0);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        const total = calculateTotal();
        const payload = {
            patient_id: formData.patient_id,
            total_amount: total,
            items: formData.items,
            status: formData.status
        };

        if (formData.treatment_plan_id) {
            payload.treatment_plan_id = formData.treatment_plan_id;
        }

        try {
            await createInvoice(payload);
            navigate('/invoices');
        } catch (err) {
            console.error(err);
            setError("Erreur lors de la création de la facture.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                    <button onClick={() => navigate('/invoices')} className="p-2 rounded-full hover:bg-gray-100 transition">
                        <ArrowLeft className="h-6 w-6 text-gray-500" />
                    </button>
                    <h1 className="text-2xl font-bold text-gray-900">Nouvelle Facture</h1>
                </div>
            </div>

            <div className="bg-white shadow rounded-lg p-6 max-w-4xl mx-auto border border-gray-200">
                {error && <div className="mb-4 bg-red-50 text-red-700 px-4 py-3 rounded border border-red-200">{error}</div>}

                <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Client / Patient Selection */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Client / Patient <span className="text-xs text-gray-400 ml-1">(الزبون)</span>
                            </label>
                            <select
                                value={formData.patient_id}
                                onChange={(e) => setFormData({ ...formData, patient_id: e.target.value, treatment_plan_id: '' })}
                                required
                                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm p-2 border"
                            >
                                <option value="">Sélectionner un patient</option>
                                {patients.map(p => (
                                    <option key={p.id} value={p.id}>{p.first_name} {p.last_name}</option>
                                ))}
                            </select>
                        </div>

                        {/* Treatment Plan Selection (Optional) */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Plan de Traitement (Optionnel)</label>
                            <select
                                value={formData.treatment_plan_id}
                                onChange={(e) => setFormData({ ...formData, treatment_plan_id: e.target.value })}
                                disabled={!formData.patient_id}
                                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm p-2 border disabled:bg-gray-100 disabled:text-gray-400"
                            >
                                <option value="">Aucun (Facture isolée)</option>
                                {treatments.map(t => (
                                    <option key={t.id} value={t.id}>
                                        Plan #{t.id} - {t.diagnosis} ({t.status})
                                    </option>
                                ))}
                            </select>
                            <p className="mt-1 text-xs text-gray-500">Lier cette facture à un plan de traitement existant.</p>
                        </div>
                    </div>

                    {/* Status Selection */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Statut du ticket de vente
                        </label>
                        <select
                            value={formData.status}
                            onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                            className="block w-full max-w-xs rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm p-2 border"
                        >
                            <option value="Draft">Brouillon (Draft)</option>
                            <option value="Issued">Emise (Issued)</option>
                            <option value="Paid">Payée (Paid)</option>
                        </select>
                        <p className="mt-1 text-xs text-gray-500">Seules les factures "Payée" comptent dans le CA.</p>
                    </div>

                    {/* Line Items / Détails de la vente */}
                    <div>
                        <div className="flex justify-between items-center mb-2">
                            <label className="block text-sm font-medium text-gray-700">
                                Lignes de vente / المنتجات المباعة
                            </label>
                            <button type="button" onClick={addItem} className="text-sm text-brand-600 hover:text-brand-800 font-medium flex items-center">
                                <Plus className="h-4 w-4 mr-1" /> Ajouter une ligne
                            </button>
                        </div>
                        <div className="space-y-2">
                            {formData.items.map((item, index) => (
                                <div key={index} className="flex gap-4 items-end bg-gray-50 p-3 rounded-md border border-gray-100">
                                    <div className="flex-1">
                                        <label className="block text-xs font-medium text-gray-500 mb-1">
                                            Article / Produit
                                        </label>
                                        <input
                                            type="text"
                                            value={item.description}
                                            onChange={(e) => handleItemChange(index, 'description', e.target.value)}
                                            required
                                            className="block w-full rounded-md border-gray-300 shadow-sm sm:text-sm p-1.5 border"
                                            placeholder="Ex: Consultation"
                                        />
                                    </div>
                                    <div className="w-24">
                                        <label className="block text-xs font-medium text-gray-500 mb-1">Qté</label>
                                        <input
                                            type="number"
                                            min="1"
                                            value={item.quantity}
                                            onChange={(e) => handleItemChange(index, 'quantity', parseInt(e.target.value) || 0)}
                                            required
                                            className="block w-full rounded-md border-gray-300 shadow-sm sm:text-sm p-1.5 border"
                                        />
                                    </div>
                                    <div className="w-32">
                                        <label className="block text-xs font-medium text-gray-500 mb-1">
                                            Prix U. (€)
                                        </label>
                                        <input
                                            type="number"
                                            min="0"
                                            step="0.01"
                                            value={item.price}
                                            onChange={(e) => handleItemChange(index, 'price', parseFloat(e.target.value) || 0)}
                                            required
                                            className="block w-full rounded-md border-gray-300 shadow-sm sm:text-sm p-1.5 border"
                                        />
                                    </div>
                                    <div className="w-24 text-right pb-2 font-medium text-gray-700">
                                        {(item.quantity * item.price).toFixed(2)} €
                                    </div>
                                    <button
                                        type="button"
                                        onClick={() => removeItem(index)}
                                        className="mb-1 p-1 text-red-500 hover:bg-red-50 rounded"
                                        disabled={formData.items.length === 1}
                                    >
                                        <Trash2 className="h-5 w-5" />
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Total */}
                    <div className="flex justify-end pt-4 border-t border-gray-200">
                        <div className="text-xl font-bold text-gray-900">
                            Total: {calculateTotal().toFixed(2)} €
                        </div>
                    </div>

                    <div className="flex justify-end pt-4">
                        <button
                            type="button"
                            onClick={() => navigate('/invoices')}
                            className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 mr-3"
                        >
                            Annuler
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 disabled:opacity-50"
                        >
                            {loading ? 'Enregistrement...' : <><Save className="mr-2 h-4 w-4" /> Enregistrer (Brouillon)</>}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default CreateInvoice;
