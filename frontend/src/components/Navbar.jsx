import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  GraduationCap, 
  LogIn, 
  LogOut, 
  LayoutDashboard, 
  Menu, 
  X, 
  ShieldCheck,
  ChevronDown
} from 'lucide-react';

export default function Navbar({ onOpenLogin, activeSection, onNavigate }) {
  const { user, isAuthenticated, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { id: 'about', label: 'Maktab haqida' },
    { id: 'teachers', label: "O'qituvchilar" },
    { id: 'subjects', label: 'Fanlar' },
    { id: 'announcements', label: 'Yangiliklar' },
    { id: 'events', label: 'Tadbirlar' },
    { id: 'achievements', label: 'Yutuqlar' },
    { id: 'resources', label: 'Kutubxona' },
    { id: 'faq', label: 'FAQ' },
    { id: 'contact', label: 'Aloqa' },
  ];

  const getRoleBadge = (role) => {
    switch (role) {
      case 'super_admin': return { label: 'Bosh Administrator', bg: 'bg-purple-100 text-purple-800 border-purple-200' };
      case 'school_admin': return { label: 'Maktab Administratori', bg: 'bg-indigo-100 text-indigo-800 border-indigo-200' };
      case 'principal': return { label: 'Direktor', bg: 'bg-amber-100 text-amber-800 border-amber-200' };
      case 'teacher': return { label: "O'qituvchi", bg: 'bg-emerald-100 text-emerald-800 border-emerald-200' };
      case 'student': return { label: "O'quvchi", bg: 'bg-blue-100 text-blue-800 border-blue-200' };
      case 'guardian': return { label: 'Ota-ona', bg: 'bg-rose-100 text-rose-800 border-rose-200' };
      default: return { label: 'Foydalanuvchi', bg: 'bg-slate-100 text-slate-800 border-slate-200' };
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo & School Branding */}
          <div 
            onClick={() => onNavigate('home')}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-blue-700 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20 group-hover:scale-105 transition-transform">
              <GraduationCap className="w-7 h-7" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-xl tracking-tight text-slate-900 group-hover:text-blue-700 transition-colors">
                  9-MAKTAB
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
                  Ultra Pro Max
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium">
                Toshkent sh. Yunusobod tumani
              </p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden xl:flex items-center gap-1">
            <button
              onClick={() => onNavigate('home')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeSection === 'home' ? 'text-blue-700 bg-blue-50/80 font-semibold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              Bosh sahifa
            </button>
            {navLinks.map((item) => (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  activeSection === item.id ? 'text-blue-700 bg-blue-50/80 font-semibold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                {item.label}
              </button>
            ))}
          </nav>

          {/* Auth Actions */}
          <div className="hidden sm:flex items-center gap-3">
            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <button
                  onClick={() => onNavigate('dashboard')}
                  className={`flex items-center gap-2 px-4 py-2.5 rounded-xl font-semibold text-sm shadow-xs transition-all ${
                    activeSection === 'dashboard'
                      ? 'bg-blue-700 text-white shadow-blue-600/30'
                      : 'bg-slate-900 text-white hover:bg-slate-800'
                  }`}
                >
                  <LayoutDashboard className="w-4 h-4" />
                  <span>Kabinet</span>
                </button>

                {/* Profile Pill */}
                <div className="flex items-center gap-2.5 px-3 py-1.5 rounded-xl border border-slate-200 bg-slate-50/80">
                  <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 font-bold flex items-center justify-center text-xs">
                    {user?.first_name?.[0] || user?.username?.[0] || 'U'}
                  </div>
                  <div className="text-left text-xs">
                    <p className="font-semibold text-slate-800 leading-tight">
                      {user?.full_name || user?.username}
                    </p>
                    <span className={`inline-block text-[10px] font-medium px-1.5 py-0.2 rounded border ${getRoleBadge(user?.role).bg}`}>
                      {getRoleBadge(user?.role).label}
                    </span>
                  </div>
                  <button
                    onClick={logout}
                    title="Tizimdan chiqish"
                    className="ml-1 p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ) : (
              <button
                onClick={onOpenLogin}
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-sm text-white bg-blue-600 hover:bg-blue-700 shadow-md shadow-blue-600/20 hover:shadow-lg hover:shadow-blue-600/30 transition-all cursor-pointer"
              >
                <LogIn className="w-4 h-4" />
                <span>Tizimga kirish</span>
              </button>
            )}
          </div>

          {/* Mobile menu toggle */}
          <div className="flex xl:hidden items-center gap-2">
            {isAuthenticated && (
              <button
                onClick={() => onNavigate('dashboard')}
                className="p-2 rounded-lg bg-blue-50 text-blue-700 font-semibold text-xs flex items-center gap-1.5"
              >
                <LayoutDashboard className="w-4 h-4" />
                <span>Kabinet</span>
              </button>
            )}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="xl:hidden border-t border-slate-200 bg-white px-4 pt-3 pb-6 space-y-2 shadow-xl animate-in slide-in-from-top-2">
          <button
            onClick={() => { onNavigate('home'); setMobileMenuOpen(false); }}
            className="w-full text-left px-3 py-2 rounded-lg font-medium text-slate-700 hover:bg-slate-50"
          >
            Bosh sahifa
          </button>
          {navLinks.map((item) => (
            <button
              key={item.id}
              onClick={() => { onNavigate(item.id); setMobileMenuOpen(false); }}
              className="w-full text-left px-3 py-2 rounded-lg font-medium text-slate-700 hover:bg-slate-50"
            >
              {item.label}
            </button>
          ))}
          <div className="pt-4 border-t border-slate-100 flex flex-col gap-2">
            {isAuthenticated ? (
              <div className="flex items-center justify-between p-3 bg-slate-50 rounded-xl">
                <div>
                  <p className="font-semibold text-slate-800 text-sm">{user?.full_name}</p>
                  <span className={`text-[11px] font-medium px-2 py-0.5 rounded border ${getRoleBadge(user?.role).bg}`}>
                    {getRoleBadge(user?.role).label}
                  </span>
                </div>
                <button
                  onClick={() => { logout(); setMobileMenuOpen(false); }}
                  className="px-3 py-1.5 text-xs text-rose-600 font-semibold bg-rose-50 rounded-lg"
                >
                  Chiqish
                </button>
              </div>
            ) : (
              <button
                onClick={() => { onOpenLogin(); setMobileMenuOpen(false); }}
                className="w-full py-2.5 text-center font-semibold text-sm text-white bg-blue-600 rounded-xl shadow-sm"
              >
                Tizimga kirish
              </button>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
