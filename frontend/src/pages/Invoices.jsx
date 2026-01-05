import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';
import { Plus, Search, Filter, DollarSign, FileText, Check } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { fetchInvoices, updateInvoice } from '../services/invoicesService';
// Assuming fetchPatients needed for names if not populated, but backend schema dumps Patient nested.

const Invoices = () => {
    const [invoices, setInvoices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        loadInvoices();
    }, []);

    const loadInvoices = async () => {
        try {
            const data = await fetchInvoices();
            setInvoices(data);
        } catch (err) {
            console.error("Error loading invoices", err);
        } finally {
            setLoading(false);
        }
    };

    const handleMarkAsPaid = async (e, invoiceId) => {
        e.stopPropagation(); // Prevent row click
        if (window.confirm("Marquer cette facture comme Payée ?")) {
            try {
                await updateInvoice(invoiceId, { status: 'Paid' });
                loadInvoices(); // Reload to update UI and Revenue (if dashboard is separate)
            } catch (err) {
                console.error("Error updating invoice", err);
                alert("Erreur lors de la mise à jour.");
            }
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'Paid': return 'bg-green-100 text-green-800';
            case 'Issued': return 'bg-blue-100 text-blue-800';
            case 'Cancelled': return 'bg-red-100 text-red-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    const filteredInvoices = invoices.filter(inv => {
        const patientName = inv.patient ? `${inv.patient.first_name} ${inv.patient.last_name}` : '';
        return patientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
            inv.id.toString().includes(searchTerm);
    });

    if (loading) return <div className="p-8 text-center">Chargement...</div>;

    return (
        <div className="space-y-6">
            <div className="sm:flex sm:items-center sm:justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-gray-900">Facturation</h1>
                    <p className="mt-1 text-sm text-gray-500">Gestion des factures et paiements</p>
                </div>
                <div className="mt-4 sm:mt-0">
                    <button
                        onClick={() => navigate('/invoices/create')}
                        className="inline-flex items-center justify-center rounded-md border border-transparent bg-brand-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2 sm:w-auto"
                    >
                        <Plus className="h-4 w-4 mr-2" /> Créer une Facture
                    </button>
                </div>
            </div>

            {/* Filters */}
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 flex flex-col sm:flex-row gap-4">
                <div className="relative flex-1">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Search className="h-5 w-5 text-gray-400" />
                    </div>
                    <input
                        type="text"
                        className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-brand-500 focus:border-brand-500 sm:text-sm"
                        placeholder="Rechercher par patient ou N° facture..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            {/* Table */}
            <div className="bg-white shadow overflow-hidden sm:rounded-lg border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">N° Facture</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Patient</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Montant</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Traitement</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Statut</th>
                            <th className="relative px-6 py-3"><span className="sr-only">Actions</span></th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {filteredInvoices.map((invoice) => (
                            <tr key={invoice.id} className="hover:bg-gray-50 cursor-pointer" onClick={() => navigate(`/invoices/${invoice.id}`)}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                    #{invoice.id}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                    {invoice.patient ? `${invoice.patient.first_name} ${invoice.patient.last_name}` : 'Inconnu'}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {invoice.issue_date ? new Date(invoice.issue_date).toLocaleDateString() : '-'}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900">
                                    {invoice.total_amount.toFixed(2)} €
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {invoice.treatment_plan_id ? <span className="bg-purple-100 text-purple-800 px-2 py-0.5 rounded text-xs">Plan #{invoice.treatment_plan_id}</span> : '-'}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(invoice.status)}`}>
                                        {invoice.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium flex items-center justify-end space-x-2">
                                    {invoice.status !== 'Paid' && (
                                        <button
                                            onClick={(e) => handleMarkAsPaid(e, invoice.id)}
                                            className="text-green-600 hover:text-green-800 p-1 rounded hover:bg-green-50"
                                            title="Marquer comme payée"
                                        >
                                            <Check className="h-5 w-5" />
                                        </button>
                                    )}
                                    <button className="text-brand-600 hover:text-brand-900">Voir</button>
                                </td>
                            </tr>
                        ))}
                        {filteredInvoices.length === 0 && (
                            <tr>
                                <td colSpan="6" className="px-6 py-10 text-center text-gray-500">
                                    Aucune facture trouvée.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Invoices;
