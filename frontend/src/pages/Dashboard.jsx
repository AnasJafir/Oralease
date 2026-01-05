import React from 'react';
import {
    Users, Calendar, Activity, DollarSign,
    Clock, AlertCircle, CheckCircle, ArrowRight,
    PlusCircle, FileText, Package
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const navigate = useNavigate();
    const currentDate = new Date().toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });

    const [stats, setStats] = React.useState([
        { label: 'Patients du jour', value: '0', icon: Users, color: 'text-blue-600', bg: 'bg-blue-100' },
        { label: 'Chiffre d\'affaires', value: '1 450 €', icon: DollarSign, color: 'text-green-600', bg: 'bg-green-100' },
        { label: 'Taux d\'occupation', value: '85%', icon: Activity, color: 'text-purple-600', bg: 'bg-purple-100' },
    ]);
    const [appointments, setAppointments] = React.useState([]);

    React.useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('/api/v2/dashboard/summary', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const data = await response.json();

                    // Update stats with real data
                    setStats([
                        { label: 'Patients du jour', value: data.stats.patients_today.toString(), icon: Users, color: 'text-blue-600', bg: 'bg-blue-100' },
                        { label: 'Chiffre d\'affaires', value: data.stats.revenue, icon: DollarSign, color: 'text-green-600', bg: 'bg-green-100' },
                        { label: 'Taux d\'occupation', value: data.stats.occupancy, icon: Activity, color: 'text-purple-600', bg: 'bg-purple-100' },
                    ]);

                    setAppointments(data.appointments);
                }
            } catch (error) {
                console.error("Erreur chargement dashboard:", error);
            }
        };

        fetchDashboardData();
    }, []);

    // Calcule des infos pour le brief
    const patientCount = stats.find(s => s.label === 'Patients du jour')?.value || '0';
    const urgentAppointment = appointments.find(apt => apt.urgent);
    const hasUrgency = !!urgentAppointment;

    return (
        <div className="space-y-8">
            {/* Hero Section with Glassmorphism */}
            <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-brand-600 to-blue-500 text-white shadow-lg">
                <div className="absolute inset-0 bg-white/10 backdrop-blur-sm"></div>
                <div className="relative p-8 sm:p-10">
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center">
                        <div>
                            <p className="text-blue-100 font-medium mb-1 capitalize">{currentDate}</p>
                            <h1 className="text-3xl sm:text-4xl font-bold mb-2">Bonjour, Dr. Jafir</h1>
                            <p className="text-blue-50 text-lg max-w-2xl">
                                Vous avez <span className="font-bold text-white">{patientCount} patients</span> aujourd'hui.
                                {hasUrgency ? (
                                    <> Attention, <span className="font-bold text-yellow-300">1 urgence</span> signalée à {urgentAppointment.time}.</>
                                ) : (
                                    <> Aucune urgence signalée pour le moment.</>
                                )}
                            </p>
                        </div>
                        <div className="mt-6 sm:mt-0">
                            <button className="bg-white text-brand-600 px-6 py-3 rounded-full font-semibold shadow-md hover:bg-blue-50 transition flex items-center">
                                <Activity className="w-5 h-5 mr-2" />
                                Démarrer la journée
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {stats.map((stat, index) => (
                    <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition duration-200">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-500">{stat.label}</p>
                                <p className="text-3xl font-bold text-gray-900 mt-1">{stat.value}</p>
                            </div>
                            <div className={`p-3 rounded-full ${stat.bg}`}>
                                <stat.icon className={`w-6 h-6 ${stat.color}`} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Timeline / Agenda */}
                <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                    <div className="p-6 border-b border-gray-100 flex justify-between items-center">
                        <h2 className="text-lg font-bold text-gray-900 flex items-center">
                            <Clock className="w-5 h-5 mr-2 text-brand-500" />
                            Prochains Rendez-vous
                        </h2>
                        <button onClick={() => navigate('/appointments')} className="text-sm text-brand-600 hover:text-brand-700 font-medium flex items-center">
                            Voir l'agenda <ArrowRight className="w-4 h-4 ml-1" />
                        </button>
                    </div>
                    <div className="divide-y divide-gray-50">
                        {appointments.map((apt, index) => (
                            <div key={index} className="p-4 hover:bg-gray-50 transition flex items-center justify-between group">
                                <div className="flex items-center space-x-4">
                                    <div className="text-gray-900 font-bold w-16 text-lg">{apt.time}</div>
                                    <div>
                                        <p className="font-semibold text-gray-900 text-base">{apt.patient}</p>
                                        <p className="text-sm text-gray-500 font-medium">{apt.type}</p>
                                    </div>
                                </div>
                                <div className="flex items-center space-x-3">
                                    {apt.urgent && (
                                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                            Urgent
                                        </span>
                                    )}
                                    <button
                                        onClick={() => navigate(`/treatments?patientId=${apt.patient_id}`)}
                                        className="text-sm text-brand-600 hover:text-brand-700 font-medium flex items-center bg-brand-50 hover:bg-brand-100 px-3 py-1.5 rounded-lg transition"
                                    >
                                        <FileText className="w-4 h-4 mr-1.5" />
                                        Voir soin
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Quick Actions & Notifications */}
                <div className="space-y-6">
                    {/* Quick Actions */}
                    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
                        <h2 className="text-lg font-bold text-gray-900 mb-4">Actions Rapides</h2>
                        <div className="grid grid-cols-2 gap-4">
                            <button onClick={() => navigate('/patients/add')} className="flex flex-col items-center justify-center p-4 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 transition border border-blue-100">
                                <PlusCircle className="w-6 h-6 mb-2" />
                                <span className="text-sm font-medium">Nouveau Patient</span>
                            </button>
                            <button onClick={() => navigate('/appointments/add')} className="flex flex-col items-center justify-center p-4 rounded-lg bg-purple-50 hover:bg-purple-100 text-purple-700 transition border border-purple-100">
                                <Calendar className="w-6 h-6 mb-2" />
                                <span className="text-sm font-medium">Nouveau RDV</span>
                            </button>
                            <button onClick={() => navigate('/treatments/add')} className="flex flex-col items-center justify-center p-4 rounded-lg bg-teal-50 hover:bg-teal-100 text-teal-700 transition border border-teal-100">
                                <FileText className="w-6 h-6 mb-2" />
                                <span className="text-sm font-medium">Devis / Soin</span>
                            </button>
                            <button onClick={() => navigate('/inventory')} className="flex flex-col items-center justify-center p-4 rounded-lg bg-orange-50 hover:bg-orange-100 text-orange-700 transition border border-orange-100">
                                <Package className="w-6 h-6 mb-2" />
                                <span className="text-sm font-medium">Commande</span>
                            </button>
                        </div>
                    </div>

                    {/* AI Insights / Notifications */}
                    <div className="bg-gradient-to-br from-indigo-50 to-white rounded-xl shadow-sm border border-indigo-100 p-6">
                        <h2 className="text-lg font-bold text-indigo-900 mb-4 flex items-center">
                            <Activity className="w-5 h-5 mr-2 text-indigo-500" />
                            Assistant IA
                        </h2>
                        <div className="space-y-3">
                            <div className="flex items-start space-x-3 p-3 bg-white rounded-lg shadow-sm border border-indigo-50">
                                <AlertCircle className="w-5 h-5 text-yellow-500 flex-shrink-0 mt-0.5" />
                                <div>
                                    <p className="text-sm text-gray-800 font-medium">Stock faible : Anesthésiques</p>
                                    <p className="text-xs text-gray-500 mt-1">Il reste moins de 10 boîtes. Commander ?</p>
                                </div>
                            </div>
                            <div className="flex items-start space-x-3 p-3 bg-white rounded-lg shadow-sm border border-indigo-50">
                                <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                                <div>
                                    <p className="text-sm text-gray-800 font-medium">Devis accepté</p>
                                    <p className="text-xs text-gray-500 mt-1">M. Thomas a signé le devis #452 (Implant).</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
