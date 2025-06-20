import { useState, useEffect } from 'react';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import ModularNav from './components/Navigation/ModularNav';
import ModuleLoader from './components/ModuleLoader';
import apiService from './services/api';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [currentView, setCurrentView] = useState('login');
  const [currentModule, setCurrentModule] = useState('dashboard');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const checkAuth = async () => {
      if (apiService.isAuthenticated()) {
        try {
          const response = await apiService.getCurrentUser();
          setUser(response.user);
        } catch (error) {
          console.error('Auth check failed:', error);
          apiService.clearToken();
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    apiService.clearToken();
    setUser(null);
    setCurrentView('login');
    setCurrentModule('dashboard');
  };

  const handleModuleSelect = (moduleName, moduleData) => {
    if (moduleName === 'logout') {
      handleLogout();
      return;
    }
    setCurrentModule(moduleName);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (user) {
    return (
      <div className="app-container">
        <ModularNav 
          user={user} 
          onModuleSelect={handleModuleSelect}
          currentModule={currentModule}
        />
        <main className="app-main">
          <ModuleLoader 
            moduleName={currentModule}
            user={user}
          />
        </main>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="auth-container">
        {currentView === 'login' ? (
          <LoginForm 
            onSuccess={handleLoginSuccess}
            onSwitchToRegister={() => setCurrentView('register')}
          />
        ) : (
          <RegisterForm 
            onSuccess={handleLoginSuccess}
            onSwitchToLogin={() => setCurrentView('login')}
          />
        )}
      </div>
    </div>
  );
}

export default App;
