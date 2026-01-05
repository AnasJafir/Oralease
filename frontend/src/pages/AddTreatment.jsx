import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createTreatment } from '../services/treatmentsService';
import { fetchPatients } from '../services/patientsService';
import { ArrowLeft, Save } from 'lucide-react';

const AddTreatment = () => {
    const navigate = useNavigate();
    const [patients, setPatients] = useState([]);
    const [formData, setFormData] = useState({
        patient_id: '',
        diagnosis: '',
        treatment_details: '',
        status: 'Pending'
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
                setError("Impossible de charger la liste des patients.");
            }
        };
        loadPatients();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            await createTreatment(formData);
            navigate('/treatments');
        } catch (err) {
            console.error(err);
            setError("Erreur lors de la création du plan de traitement.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                    <button
                        onClick={() => navigate('/treatments')}
                        className="p-2 rounded-full hover:bg-gray-100 transition"
                    >
                        <ArrowLeft className="h-6 w-6 text-gray-500" />
                    </button>
                    <h1 className="text-2xl font-bold text-gray-900">Nouveau Plan de Traitement</h1>
                </div>
            </div>

            <div className="bg-white shadow rounded-lg p-6 max-w-2xl mx-auto border border-gray-200">
                {error && (
                    <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Patient</label>
                        <select
                            name="patient_id"
                            value={formData.patient_id}
                            onChange={handleChange}
                            required
                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm p-2 border"
                        >
                            <option value="">Sélectionner un patient</option>
                            {patients.map(p => (
                                <option key={p.id} value={p.id}>
                                    {p.first_name} {p.last_name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Diagnostic</label>
                        <textarea
                            name="diagnosis"
                            value={formData.diagnosis}
                            onChange={handleChange}
                            required
                            rows={3}
                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm p-2 border"
                            placeholder="Description du diagnostic..."
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Détails du Traitement</label>
                        <textarea
                            name="treatment_details"
                            value={formData.treatment_details}
                            onChange={handleChange}
                            required
                            rows={5}
                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm p-2 border"
                            placeholder="Étapes, médicaments, procédures..."
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Statut Initial</label>
                        <select
                            name="status"
                            value={formData.status}
                            onChange={handleChange}
                            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-brand-500 focus:ring-brand-500 sm:text-sm p-2 border"
                        >
                            <option value="Pending">En attente</option>
                            <option value="In Progress">En cours</option>
                            <option value="Completed">Terminé</option>
                            <option value="Cancelled">Annulé</option>
                        </select>
                    </div>

                    <div className="flex justify-end pt-4">
                        <button
                            type="button"
                            onClick={() => navigate('/treatments')}
                            className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 mr-3"
                        >
                            Annuler
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 disabled:opacity-50"
                        >
                            {loading ? 'Enregistrement...' : (
                                <>
                                    <Save className="mr-2 h-4 w-4" /> Enregistrer
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default AddTreatment;
