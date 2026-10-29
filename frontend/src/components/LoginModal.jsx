import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { 
  X, 
  Lock, 
  User, 
  ArrowRight, 
  AlertCircle,
  GraduationCap
} from 'lucide-react';

export default function LoginModal({ isOpen, onClose, onSwitchToRegister, onSuccess }) {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username.trim(), password);
      onClose();
      if (onSuccess) onSuccess();
    } catch (err) {
      const msg = err.message || '';
      if (msg.includes('No active account') || msg.includes('not found') || msg.includes('credentials')) {
        setError("Foydalanuvchi nomi yoki parol noto‘g‘ri kiritildi. Iltimos, qayta tekshirib ko'ring.");
      } else if (msg.includes('disabled') || msg.includes('inactive')) {
        setError("Sizning hisobingiz faolsizlantirilgan. Iltimos, maktab ma'muriyatiga murojaat qiling.");
      } else {
        setError(msg || "Tizimga kirishda xatolik yuz berdi.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div 
        className="relative w-full max-w-md bg-white rounded-3xl shadow-2xl border border-slate-100 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="relative bg-gradient-to-br from-blue-700 via-indigo-700 to-slate-900 px-6 pt-7 pb-6 text-white text-center">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-1.5 rounded-full text-blue-200 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
          <div className="w-12 h-12 rounded-2xl bg-white/15 backdrop-blur-sm mx-auto flex items-center justify-center mb-3 shadow-inner">
            <GraduationCap className="w-7 h-7 text-white" />
          </div>
          <h2 className="text-xl font-bold tracking-tight">9-Maktab Tizimiga Kirish</h2>
          <p className="text-xs text-blue-100 mt-1">
            Yagona raqamli ta'lim va boshqaruv platformasi
          </p>
        </div>

        {/* Form Body */}
        <div className="p-6">
          {error && (
            <div className="mb-4 p-3.5 rounded-xl bg-rose-50 border border-rose-200 flex items-start gap-2.5 text-xs text-rose-800 animate-in fade-in">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Login / Foydalanuvchi nomi yoki Email *
              </label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="text"
                  required
                  autoFocus
                  value={username}
                  onChange={(e) => { setUsername(e.target.value); setError(''); }}
                  placeholder="Foydalanuvchi nomingizni kiriting"
                  className="w-full pl-10 pr-4 py-2.5 text-xs sm:text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 focus:border-blue-600 transition-all text-slate-900"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Parol *
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => { setPassword(e.target.value); setError(''); }}
                  placeholder="••••••••••••"
                  className="w-full pl-10 pr-4 py-2.5 text-xs sm:text-sm bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 focus:border-blue-600 transition-all text-slate-900"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl font-bold text-xs sm:text-sm text-white bg-blue-600 hover:bg-blue-700 shadow-md shadow-blue-600/25 transition-all flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer active:scale-[0.99]"
            >
              {loading ? (
                <span>Kirilmoqda...</span>
              ) : (
                <>
                  <span>Kabinetga kirish</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Registration link */}
          <div className="mt-6 pt-5 border-t border-slate-100 text-center">
            <span className="text-xs text-slate-500">Hisobingiz mavjud emasmi? </span>
            <button
              type="button"
              onClick={() => {
                onClose();
                if (onSwitchToRegister) onSwitchToRegister();
              }}
              className="text-xs font-bold text-blue-600 hover:text-blue-800 transition-colors cursor-pointer"
            >
              Ro‘yxatdan o‘tish
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
