import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import { 
  X, 
  Lock, 
  User, 
  Mail, 
  Phone, 
  GraduationCap, 
  Users, 
  ArrowRight, 
  AlertCircle, 
  CheckCircle,
  Hash
} from 'lucide-react';

export default function RegisterModal({ isOpen, onClose, onSwitchToLogin, onSuccess }) {
  const { register } = useAuth();
  const [accountType, setAccountType] = useState('student'); // 'student' or 'guardian'
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Form Fields
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    phone_number: '',
    password: '',
    confirm_password: '',
    classroom_id: '',
    student_id_code: '',
    child_student_id: '',
    relationship: 'father',
  });

  useEffect(() => {
    if (isOpen) {
      api.getClassrooms()
        .then((res) => {
          const list = res.results || res || [];
          setClasses(list);
          if (list.length > 0 && !formData.classroom_id) {
            setFormData((prev) => ({ ...prev, classroom_id: list[0].id }));
          }
        })
        .catch(console.error);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirm_password) {
      setError("Kiritilgan parollar bir-biriga mos kelmadi.");
      return;
    }
    if (formData.password.length < 6) {
      setError("Parol kamida 6 belgidan iborat bo'lishi kerak.");
      return;
    }

    setLoading(true);
    try {
      const payload = {
        account_type: accountType,
        first_name: formData.first_name,
        last_name: formData.last_name,
        username: formData.username,
        email: formData.email,
        phone_number: formData.phone_number,
        password: formData.password,
        confirm_password: formData.confirm_password,
        ...(accountType === 'student' ? {
          classroom_id: parseInt(formData.classroom_id),
          student_id_code: formData.student_id_code,
        } : {
          child_student_id: formData.child_student_id,
          relationship: formData.relationship,
        }),
      };

      await register(payload);
      onClose();
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.message || "Ro'yxatdan o'tishda xatolik yuz berdi.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div 
        className="relative w-full max-w-lg bg-white rounded-3xl shadow-2xl border border-slate-100 overflow-hidden max-h-[92vh] flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="relative bg-gradient-to-br from-blue-700 via-indigo-700 to-slate-900 px-6 py-6 text-white text-center shrink-0">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-1.5 rounded-full text-blue-200 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
          <div className="w-11 h-11 rounded-xl bg-white/15 backdrop-blur-sm mx-auto flex items-center justify-center mb-2 shadow-inner">
            <GraduationCap className="w-6 h-6 text-white" />
          </div>
          <h2 className="text-xl font-bold tracking-tight">9-Maktabda Ro‘yxatdan O‘tish</h2>
          <p className="text-xs text-blue-100 mt-0.5">
            O'quvchi yoki ota-ona sifatida profilingizni yarating
          </p>
        </div>

        {/* Scrollable Body */}
        <div className="p-6 overflow-y-auto space-y-5">
          {error && (
            <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 flex items-start gap-2.5 text-xs text-rose-800">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {/* QUESTION: Siz kim bo'lib ro'yxatdan o'tmoqchisiz? */}
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
              Siz kim bo‘lib ro‘yxatdan o‘tmoqchisiz? *
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => { setAccountType('student'); setError(''); }}
                className={`p-3.5 rounded-2xl border text-left flex items-center gap-3 transition-all cursor-pointer ${
                  accountType === 'student'
                    ? 'border-blue-600 bg-blue-50/70 text-blue-900 ring-2 ring-blue-600/20 shadow-xs'
                    : 'border-slate-200 hover:border-slate-300 text-slate-700 bg-slate-50/50'
                }`}
              >
                <div className={`p-2 rounded-xl shrink-0 ${accountType === 'student' ? 'bg-blue-600 text-white' : 'bg-slate-200 text-slate-600'}`}>
                  <GraduationCap className="w-5 h-5" />
                </div>
                <div>
                  <div className="font-bold text-xs">O‘quvchi</div>
                  <div className="text-[10px] text-slate-500">Darslar & Baholar</div>
                </div>
              </button>

              <button
                type="button"
                onClick={() => { setAccountType('guardian'); setError(''); }}
                className={`p-3.5 rounded-2xl border text-left flex items-center gap-3 transition-all cursor-pointer ${
                  accountType === 'guardian'
                    ? 'border-indigo-600 bg-indigo-50/70 text-indigo-900 ring-2 ring-indigo-600/20 shadow-xs'
                    : 'border-slate-200 hover:border-slate-300 text-slate-700 bg-slate-50/50'
                }`}
              >
                <div className={`p-2 rounded-xl shrink-0 ${accountType === 'guardian' ? 'bg-indigo-600 text-white' : 'bg-slate-200 text-slate-600'}`}>
                  <Users className="w-5 h-5" />
                </div>
                <div>
                  <div className="font-bold text-xs">Ota-ona</div>
                  <div className="text-[10px] text-slate-500">Farzand nazorati</div>
                </div>
              </button>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* First & Last Name */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Ismingiz *
                </label>
                <input
                  type="text"
                  required
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  placeholder="Masalan: Jasur"
                  className="w-full px-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Familiyangiz *
                </label>
                <input
                  type="text"
                  required
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  placeholder="Masalan: Alimov"
                  className="w-full px-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900"
                />
              </div>
            </div>

            {/* Username & Phone/Email */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Login / Username *
                </label>
                <div className="relative">
                  <User className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
                  <input
                    type="text"
                    required
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    placeholder="student_jasur2"
                    className="w-full pl-9 pr-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  {accountType === 'student' ? 'Elektron pochta (ixtiyoriy)' : 'Telefon raqamingiz *'}
                </label>
                <div className="relative">
                  {accountType === 'student' ? (
                    <Mail className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
                  ) : (
                    <Phone className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
                  )}
                  <input
                    type={accountType === 'student' ? 'email' : 'tel'}
                    required={accountType === 'guardian'}
                    name={accountType === 'student' ? 'email' : 'phone_number'}
                    value={accountType === 'student' ? formData.email : formData.phone_number}
                    onChange={handleChange}
                    placeholder={accountType === 'student' ? 'pochta@misol.uz' : '+998 90 123 45 67'}
                    className="w-full pl-9 pr-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900"
                  />
                </div>
              </div>
            </div>

            {/* STUDENT SPECIFIC FIELDS */}
            {accountType === 'student' && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 p-3.5 rounded-2xl bg-blue-50/50 border border-blue-100">
                <div>
                  <label className="block text-xs font-bold text-blue-900 mb-1">
                    Sinfingiz *
                  </label>
                  <select
                    name="classroom_id"
                    value={formData.classroom_id}
                    onChange={handleChange}
                    className="w-full px-3.5 py-2.5 text-xs bg-white border border-blue-200 rounded-xl text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-600/30 font-semibold"
                  >
                    {classes.map((c) => (
                      <option key={c.id} value={c.id}>{c.name} sinfi</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-blue-900 mb-1">
                    O‘quvchi ID kodi *
                  </label>
                  <div className="relative">
                    <Hash className="w-3.5 h-3.5 text-blue-500 absolute left-3 top-3" />
                    <input
                      type="text"
                      required
                      name="student_id_code"
                      value={formData.student_id_code}
                      onChange={handleChange}
                      placeholder="Masalan: 9M-2026-007"
                      className="w-full pl-9 pr-3.5 py-2.5 text-xs bg-white border border-blue-200 rounded-xl text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-600/30 font-mono font-bold uppercase"
                    />
                  </div>
                  <span className="text-[10px] text-blue-600">Maktab bergan shaxsiy guvohnoma ID kodi</span>
                </div>
              </div>
            )}

            {/* GUARDIAN SPECIFIC FIELDS */}
            {accountType === 'guardian' && (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 p-3.5 rounded-2xl bg-indigo-50/50 border border-indigo-100">
                <div>
                  <label className="block text-xs font-bold text-indigo-900 mb-1">
                    Farzandingizning ID kodi *
                  </label>
                  <div className="relative">
                    <Hash className="w-3.5 h-3.5 text-indigo-500 absolute left-3 top-3" />
                    <input
                      type="text"
                      required
                      name="child_student_id"
                      value={formData.child_student_id}
                      onChange={handleChange}
                      placeholder="Masalan: 9M-2026-001"
                      className="w-full pl-9 pr-3.5 py-2.5 text-xs bg-white border border-indigo-200 rounded-xl text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-600/30 font-mono font-bold uppercase"
                    />
                  </div>
                  <span className="text-[10px] text-indigo-600">Farzandingizning maktab ID kodi</span>
                </div>

                <div>
                  <label className="block text-xs font-bold text-indigo-900 mb-1">
                    Qarindoshlik darajasi *
                  </label>
                  <select
                    name="relationship"
                    value={formData.relationship}
                    onChange={handleChange}
                    className="w-full px-3.5 py-2.5 text-xs bg-white border border-indigo-200 rounded-xl text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-600/30 font-semibold"
                  >
                    <option value="father">Otasi</option>
                    <option value="mother">Onasi</option>
                    <option value="guardian">Qonuniy vasiysi</option>
                  </select>
                </div>
              </div>
            )}

            {/* Passwords */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Parol *
                </label>
                <div className="relative">
                  <Lock className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
                  <input
                    type="password"
                    required
                    minLength={6}
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Kamida 6 belgi"
                    className="w-full pl-9 pr-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Parolni tasdiqlang *
                </label>
                <div className="relative">
                  <Lock className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-3" />
                  <input
                    type="password"
                    required
                    minLength={6}
                    name="confirm_password"
                    value={formData.confirm_password}
                    onChange={handleChange}
                    placeholder="Qayta kiriting"
                    className="w-full pl-9 pr-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900"
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl font-bold text-xs text-white bg-blue-600 hover:bg-blue-700 shadow-md shadow-blue-600/25 transition-all flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer"
            >
              {loading ? (
                <span>Ro‘yxatdan o‘tkazilmoqda...</span>
              ) : (
                <>
                  <span>Ro‘yxatdan o‘tish va Kirish</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Switch to login */}
          <div className="text-center pt-3 border-t border-slate-100">
            <span className="text-xs text-slate-500">Allaqachon hisobingiz bormi? </span>
            <button
              type="button"
              onClick={() => { onClose(); onSwitchToLogin(); }}
              className="text-xs font-bold text-blue-600 hover:text-blue-800 transition-colors cursor-pointer"
            >
              Tizimga kiring
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
