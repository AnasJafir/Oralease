import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { fetchTreatment, deleteTreatment } from '../services/treatmentsService';
import { ArrowLeft, Edit, Trash2 } from 'lucide-react';

const ViewTreatment = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [treatment, setTreatment] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [confirmDelete, setConfirmDelete] = useState(false);

    useEffect(() => {
        const loadData = async () => {
            try {
                const data = await fetchTreatment(id);
                setTreatment(data);
            } catch (err) {
                console.error("Error loading treatment", err);
                setError("Plan de traitement introuvable.");
            } finally {
                setLoading(false);
            }
        };
        loadData();
    }, [id]);

    const handleDelete = async () => {
        try {
            await deleteTreatment(id);
            navigate('/treatments');
        } catch (err) {
            console.error(err);
            alert("Erreur lors de la suppression: " + (err.message || "Erreur inconnue"));
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'Completed': return 'bg-green-100 text-green-800';
            case 'In Progress': return 'bg-blue-100 text-blue-800';
            default: return 'bg-yellow-100 text-yellow-800';
        }
    };

    if (loading) return <div className="p-8 text-center">Chargement...</div>;
    if (error) return <div className="p-8 text-center text-red-600">{error}</div>;
    if (!treatment) return <div className="p-8 text-center">Introuvable</div>;

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
                    <h1 className="text-2xl font-bold text-gray-900">Détails du Traitement</h1>
                </div>
                <div className="flex space-x-3">
                    <button
                        onClick={() => navigate(`/treatments/${id}/edit`)}
                        className="inline-flex items-center px-4 py-2 border border-brand-200 rounded-md shadow-sm text-sm font-medium text-brand-700 bg-white hover:bg-brand-50"
                    >
                        <Edit className="h-4 w-4 mr-2" /> Modifier
                    </button>

                    {/* Delete with Confirmation State */}
                    {confirmDelete ? (
                        <div className="flex items-center space-x-2">
                            <span className="text-sm text-gray-500">Sûr ?</span>
                            <button
                                onClick={handleDelete}
                                className="inline-flex items-center px-3 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700"
                            >
                                Oui, supprimer
                            </button>
                            <button
                                onClick={() => setConfirmDelete(false)}
                                className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                            >
                                Non
                            </button>
                        </div>
                    ) : (
                        <button
                            onClick={() => setConfirmDelete(true)}
                            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700"
                        >
                            <Trash2 className="h-4 w-4 mr-2" /> Supprimer
                        </button>
                    )}
                </div>
            </div>

            <div className="bg-white shadow overflow-hidden sm:rounded-lg border border-gray-200">
                <div className="px-4 py-5 sm:px-6 flex justify-between items-center">
                    <div>
                        <h3 className="text-lg leading-6 font-medium text-gray-900">
                            Plan #{treatment.id}
                        </h3>
                        <p className="mt-1 max-w-2xl text-sm text-gray-500">
                            Créé le {new Date().toLocaleDateString()} {/* Date creation not in model yet */}
                        </p>
                    </div>
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(treatment.status)}`}>
                        {treatment.status}
                    </span>
                </div>
                <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
                    <dl className="sm:divide-y sm:divide-gray-200">
                        <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt className="text-sm font-medium text-gray-500">Patient</dt>
                            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                {treatment.patient ? `${treatment.patient.first_name} ${treatment.patient.last_name}` : `Patient #${treatment.patient_id}`}
                            </dd>
                        </div>
                        <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt className="text-sm font-medium text-gray-500">Diagnostic</dt>
                            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                                {treatment.diagnosis}
                            </dd>
                        </div>
                        <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                            <dt className="text-sm font-medium text-gray-500">Détails du soin</dt>
                            <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2 whitespace-pre-wrap">
                                {treatment.treatment_details}
                            </dd>
                        </div>
                    </dl>
                </div>
            </div>
        </div>
    );
};

export default ViewTreatment;
