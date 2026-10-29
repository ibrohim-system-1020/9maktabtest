import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LoginModal from './components/LoginModal';
import LandingPage from './pages/LandingPage';
import DashboardPage from './pages/DashboardPage';

function MainApp() {
  const { isAuthenticated } = useAuth();
  const [activeSection, setActiveSection] = useState('home');
  const [loginModalOpen, setLoginModalOpen] = useState(false);

  const handleNavigate = (sectionId) => {
    setActiveSection(sectionId);
    if (sectionId === 'home') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (sectionId === 'dashboard') {
      // open dashboard
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      // scroll to section on landing page
      const el = document.getElementById(sectionId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 selection:bg-blue-500 selection:text-white">
      {/* Navigation */}
      <Navbar
        onOpenLogin={() => setLoginModalOpen(true)}
        activeSection={activeSection}
        onNavigate={handleNavigate}
      />

      {/* Main Content Area */}
      <main className="flex-1">
        {activeSection === 'dashboard' && isAuthenticated ? (
          <DashboardPage onNavigateHome={() => handleNavigate('home')} />
        ) : (
          <LandingPage
            onOpenLogin={() => setLoginModalOpen(true)}
            onOpenDashboard={() => handleNavigate('dashboard')}
            scrollToSection={handleNavigate}
          />
        )}
      </main>

      {/* Footer */}
      <Footer onNavigate={handleNavigate} />

      {/* Login Modal */}
      <LoginModal
        isOpen={loginModalOpen}
        onClose={() => setLoginModalOpen(false)}
        onSuccess={() => handleNavigate('dashboard')}
      />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  );
}
