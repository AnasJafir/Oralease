// frontend/src/App.jsx
import React, { useState, useEffect, createContext, useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
// import { api } from './lib/api'; // Removed unused direct reference, handled in services
import { initAuth, login as authLogin, logout as authLogout } from './services/authService';

// --- Import des Pages ---
import Patients from './pages/Patients';
import AddPatient from './pages/AddPatient';
import ViewPatient from './pages/ViewPatient';
import EditPatient from './pages/EditPatient';
import Appointments from './pages/Appointments';
import AddAppointment from './pages/AddAppointment';
import EditAppointment from './pages/EditAppointment';
import InventoryList from './pages/InventoryList';
import AddInventoryItemNew from './pages/AddInventoryItemNew';
import EditInventoryItem from './pages/EditInventoryItem';
import Treatments from './pages/Treatments';
import AddTreatment from './pages/AddTreatment';
import ViewTreatment from './pages/ViewTreatment';
import EditTreatment from './pages/EditTreatment';
import Invoices from './pages/Invoices';
import CreateInvoice from './pages/CreateInvoice';
import Dashboard from './pages/Dashboard';

import {
  LayoutDashboard, Users, CalendarDays, Package, Activity, LogOut, DollarSign
} from 'lucide-react';

// --- Contexte d'Authentification ---
const AuthContext = createContext(null);

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const session = initAuth();
    if (session) {
      // Defer both state updates
      Promise.resolve().then(() => {
        setUser(session);
        setLoading(false);
      });
    } else {
      Promise.resolve().then(() => setLoading(false));
    }
  }, []);

  const login = async (username, password) => {
    const session = await authLogin(username, password);
    setUser(session);
    return true;
  };

  const logout = () => {
    authLogout();
    setUser(null);
  };

  if (loading) return <div className="flex h-screen items-center justify-center text-brand-600 animate-pulse">Chargement...</div>;

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

const useAuth = () => useContext(AuthContext);

const ProtectedRoute = ({ children }) => {
  const { user } = useAuth();
  const location = useLocation();
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />;
  return children;
};

// --- Composants UI ---
const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await login(username, password);
      navigate('/');
    } catch (e) {
      setError(e.message);
    }
  };
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-brand-50 to-brand-100">
      <form onSubmit={handleSubmit} className="bg-white/90 backdrop-blur border border-brand-100 p-10 rounded-xl shadow-card w-full max-w-md">
        <div className="text-center mb-8">
          <div className="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-brand-100 mb-4">
            <Activity className="h-10 w-10 text-brand-600" />
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-brand-800">Oralease</h1>
          <p className="text-sm text-brand-600 mt-2">Plateforme clinique sécurisée</p>
        </div>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Nom d'utilisateur</label>
            <input className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400" placeholder="" value={username} onChange={e => setUsername(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm font-medium text-brand-700 mb-1">Mot de passe</label>
            <input type="password" className="block w-full rounded-md border-brand-200 focus:border-brand-400 focus:ring-brand-400" value={password} onChange={e => setPassword(e.target.value)} />
          </div>
          {error && <div className="text-sm text-danger-500 bg-danger-500/10 p-2 rounded">{error}</div>}
          <button className="w-full bg-brand-600 hover:bg-brand-700 text-white font-semibold rounded-md py-2 transition shadow-sm">Se connecter</button>
        </div>
      </form>
    </div>
  );
};

const Layout = ({ children }) => {
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const navigation = [
    { name: 'Tableau de bord', href: '/', icon: LayoutDashboard },
    { name: 'Patients', href: '/patients', icon: Users },
    { name: 'Agenda', href: '/appointments', icon: CalendarDays },
    { name: 'Traitements', href: '/treatments', icon: Activity },
    { name: 'Inventaire', href: '/inventory', icon: Package },
    { name: 'Finance', href: '/invoices', icon: DollarSign },
  ];
  return (
    <div className="min-h-screen bg-brand-50 flex">
      <aside className="hidden md:flex md:w-64 md:flex-col fixed inset-y-0 bg-white border-r shadow-sm">
        <div className="flex items-center p-5 h-20 border-b bg-gradient-to-r from-brand-50 to-brand-100">
          <Activity className="text-brand-600 mr-2" /> <span className="font-bold text-xl text-brand-800">Oralease</span>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {navigation.map((item) => {
            const active = location.pathname === item.href;
            return (
              <button key={item.name} onClick={() => navigate(item.href)} className={`w-full flex items-center px-3 py-2 rounded-md text-sm font-medium transition ${active ? 'bg-brand-600 text-white shadow-sm' : 'text-brand-700 hover:bg-brand-100'}`}>
                <item.icon className={`mr-3 h-5 w-5 ${active ? 'text-white' : 'text-brand-500'}`} /> {item.name}
              </button>
            );
          })}
        </nav>
        <div className="p-4 border-t bg-white/50">
          <div className="text-xs uppercase tracking-wide text-brand-500 mb-2">Session</div>
          <div className="text-sm font-medium text-brand-700 mb-3">Rôle : {user?.role}</div>
          <button onClick={() => { logout(); navigate('/login') }} className="flex items-center justify-center text-sm font-medium bg-danger-500/10 text-danger-500 w-full py-2 rounded-md hover:bg-danger-500/20 transition">
            <LogOut className="mr-2 h-4 w-4" /> Déconnexion
          </button>
        </div>
      </aside>
      <main className="flex-1 md:pl-64 p-8">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
};

// Removed misplaced import

// --- Application Principale ---

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />

          {/* Routes Protégées */}
          <Route path="/" element={<ProtectedRoute><Layout><Dashboard /></Layout></ProtectedRoute>} />

          <Route path="/patients" element={<ProtectedRoute><Layout><Patients /></Layout></ProtectedRoute>} />
          <Route path="/patients/add" element={<ProtectedRoute><Layout><AddPatient /></Layout></ProtectedRoute>} />
          <Route path="/patients/:id" element={<ProtectedRoute><Layout><ViewPatient /></Layout></ProtectedRoute>} />
          <Route path="/patients/:id/edit" element={<ProtectedRoute><Layout><EditPatient /></Layout></ProtectedRoute>} />

          <Route path="/appointments" element={<ProtectedRoute><Layout><Appointments /></Layout></ProtectedRoute>} />
          <Route path="/appointments/add" element={<ProtectedRoute><Layout><AddAppointment /></Layout></ProtectedRoute>} />
          <Route path="/appointments/:id/edit" element={<ProtectedRoute><Layout><EditAppointment /></Layout></ProtectedRoute>} />

          <Route path="/inventory" element={<ProtectedRoute><Layout><InventoryList /></Layout></ProtectedRoute>} />
          <Route path="/inventory/add" element={<ProtectedRoute><Layout><AddInventoryItemNew /></Layout></ProtectedRoute>} />
          <Route path="/inventory/:id/edit" element={<ProtectedRoute><Layout><EditInventoryItem /></Layout></ProtectedRoute>} />

          <Route path="/treatments" element={<ProtectedRoute><Layout><Treatments /></Layout></ProtectedRoute>} />
          <Route path="/treatments/add" element={<ProtectedRoute><Layout><AddTreatment /></Layout></ProtectedRoute>} />
          <Route path="/treatments/:id" element={<ProtectedRoute><Layout><ViewTreatment /></Layout></ProtectedRoute>} />
          <Route path="/treatments/:id/edit" element={<ProtectedRoute><Layout><EditTreatment /></Layout></ProtectedRoute>} />

          <Route path="/invoices" element={<ProtectedRoute><Layout><Invoices /></Layout></ProtectedRoute>} />
          <Route path="/invoices/create" element={<ProtectedRoute><Layout><CreateInvoice /></Layout></ProtectedRoute>} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;