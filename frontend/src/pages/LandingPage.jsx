import React, { useState, useEffect } from 'react';
import { api } from '../api/client';
import { 
  GraduationCap, 
  BookOpen, 
  Users, 
  Award, 
  Calendar, 
  Download, 
  Search, 
  ArrowRight, 
  Send, 
  CheckCircle, 
  Laptop, 
  Trophy, 
  FileText, 
  HelpCircle, 
  Sparkles,
  ChevronRight,
  Clock,
  MapPin,
  Flame
} from 'lucide-react';

export default function LandingPage({ onOpenLogin, onOpenDashboard, scrollToSection }) {
  const [schoolInfo, setSchoolInfo] = useState(null);
  const [announcements, setAnnouncements] = useState([]);
  const [events, setEvents] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [achievements, setAchievements] = useState([]);
  const [resources, setResources] = useState([]);
  const [faqs, setFaqs] = useState([]);
  const [faqSearch, setFaqSearch] = useState('');
  const [activeFaq, setActiveFaq] = useState(null);

  // Inquiry form state
  const [inquiry, setInquiry] = useState({
    full_name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  });
  const [inquiryStatus, setInquiryStatus] = useState({ loading: false, success: false, error: null });

  useEffect(() => {
    // Fetch public school data
    api.getSchoolInfo().then(setSchoolInfo).catch(console.error);
    api.getAnnouncements().then((res) => setAnnouncements(res.results || res || [])).catch(console.error);
    api.getEvents().then((res) => setEvents(res.results || res || [])).catch(console.error);
    api.getTeachers().then((res) => setTeachers(res.results || res || [])).catch(console.error);
    api.getSubjects().then((res) => setSubjects(res.results || res || [])).catch(console.error);
    api.getAchievements().then((res) => setAchievements(res.results || res || [])).catch(console.error);
    api.getResources().then((res) => setResources(res.results || res || [])).catch(console.error);
    api.getFAQs().then((res) => setFaqs(res.results || res || [])).catch(console.error);
  }, []);

  const handleInquirySubmit = async (e) => {
    e.preventDefault();
    setInquiryStatus({ loading: true, success: false, error: null });
    try {
      await api.submitInquiry(inquiry);
      setInquiryStatus({ loading: false, success: true, error: null });
      setInquiry({ full_name: '', email: '', phone: '', subject: '', message: '' });
    } catch (err) {
      setInquiryStatus({ loading: false, success: false, error: err.message || 'Murojaat yuborishda xatolik' });
    }
  };

  const handleDownload = async (resource) => {
    try {
      await api.trackDownload(resource.id);
      window.open(resource.resource_url, '_blank');
      // Update count locally
      setResources((prev) => prev.map((r) => r.id === resource.id ? { ...r, downloads_count: r.downloads_count + 1 } : r));
    } catch {
      window.open(resource.resource_url, '_blank');
    }
  };

  const filteredFaqs = faqs.filter((f) => 
    f.question.toLowerCase().includes(faqSearch.toLowerCase()) || 
    f.answer.toLowerCase().includes(faqSearch.toLowerCase())
  );

  return (
    <div className="space-y-24 pb-20">
      {/* 1. HERO SECTION */}
      <section className="relative overflow-hidden pt-12 pb-20 lg:pt-20 lg:pb-28 bg-gradient-to-b from-blue-50/60 via-white to-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-100 text-blue-800 text-xs font-bold border border-blue-200">
                <Sparkles className="w-3.5 h-3.5 text-blue-600" />
                <span>O‘zbekiston Respublikasi Xalq Ta’limi A’lochisi</span>
              </div>

              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-slate-900 tracking-tight leading-tight">
                9-Sonli Umumiy O‘rta <br className="hidden sm:block" />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-700 via-indigo-600 to-sky-600">
                  Ta‘lim Maktabi
                </span>
              </h1>

              <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto lg:mx-0 leading-relaxed">
                {schoolInfo?.hero_subtitle || "9-Maktab — raqamli innovatsiyalar, chuqurlashtirilgan aniq fanlar va iqtidorli yoshlar akademiyasi. Kelajak liderlari uchun nufuzli ta'lim dargohi."}
              </p>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center justify-center lg:justify-start gap-3.5 pt-2">
                <button
                  onClick={onOpenLogin}
                  className="px-6 py-3.5 rounded-xl font-bold text-sm text-white bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-600/30 hover:shadow-xl hover:shadow-blue-600/40 transition-all flex items-center gap-2 cursor-pointer"
                >
                  <GraduationCap className="w-5 h-5" />
                  <span>O‘quvchi & O‘qituvchi Portali</span>
                </button>
                <button
                  onClick={() => {
                    const el = document.getElementById('contact');
                    if (el) el.scrollIntoView({ behavior: 'smooth' });
                  }}
                  className="px-6 py-3.5 rounded-xl font-bold text-sm text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 shadow-xs hover:border-slate-400 transition-all cursor-pointer"
                >
                  Qabul va murojaat
                </button>
              </div>

              {/* Mini Stats Ribbon */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-6 border-t border-slate-200">
                <div>
                  <div className="text-2xl sm:text-3xl font-extrabold text-blue-700">1,450+</div>
                  <div className="text-xs font-medium text-slate-500">Iqtidorli o‘quvchilar</div>
                </div>
                <div>
                  <div className="text-2xl sm:text-3xl font-extrabold text-indigo-700">85+</div>
                  <div className="text-xs font-medium text-slate-500">Oliy toifali ustozlar</div>
                </div>
                <div>
                  <div className="text-2xl sm:text-3xl font-extrabold text-sky-700">98.4%</div>
                  <div className="text-xs font-medium text-slate-500">OTMga kirish natijasi</div>
                </div>
                <div>
                  <div className="text-2xl sm:text-3xl font-extrabold text-emerald-700">40 yil</div>
                  <div className="text-xs font-medium text-slate-500">Boy tarixiy tajriba</div>
                </div>
              </div>
            </div>

            {/* Right Card / Visual Showcase */}
            <div className="lg:col-span-5 relative">
              <div className="relative rounded-3xl bg-gradient-to-tr from-slate-900 to-indigo-950 p-6 sm:p-8 text-white shadow-2xl border border-slate-800">
                <div className="flex items-center justify-between pb-6 border-b border-slate-800">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold">
                      9M
                    </div>
                    <div>
                      <h4 className="font-bold text-sm">Smart Boshqaruv Tizimi</h4>
                      <p className="text-xs text-slate-400">Yagona raqamli ekotizim</p>
                    </div>
                  </div>
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold border border-emerald-500/20">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    Onlayn
                  </span>
                </div>

                <div className="space-y-3.5 py-6">
                  <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400">
                        <Calendar className="w-4 h-4" />
                      </div>
                      <div>
                        <p className="text-xs font-semibold">Elektron Dars Jadvali</p>
                        <p className="text-[11px] text-slate-400">Har bir sinf va o'qituvchi uchun</p>
                      </div>
                    </div>
                    <span className="text-xs text-blue-400 font-bold">1-chorak</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                        <CheckCircle className="w-4 h-4" />
                      </div>
                      <div>
                        <p className="text-xs font-semibold">Tezkor Davomat Qaydi</p>
                        <p className="text-[11px] text-slate-400">Ota-onalar bilan SMS va onlayn integratsiya</p>
                      </div>
                    </div>
                    <span className="text-xs text-emerald-400 font-bold">94.8%</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-slate-800/60 border border-slate-700/60 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
                        <Trophy className="w-4 h-4" />
                      </div>
                      <div>
                        <p className="text-xs font-semibold">BSB va CHSB Baholash</p>
                        <p className="text-[11px] text-slate-400">Shaffof milliy baholash tizimi</p>
                      </div>
                    </div>
                    <span className="text-xs text-amber-400 font-bold">A'lo daraja</span>
                  </div>
                </div>

                <div className="pt-4 border-t border-slate-800">
                  <button
                    onClick={onOpenLogin}
                    className="w-full py-3 rounded-xl font-bold text-xs text-slate-900 bg-white hover:bg-slate-100 transition-colors flex items-center justify-center gap-2 cursor-pointer"
                  >
                    <span>Namunaviy Kabinetga Kirish</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. ANNOUNCEMENTS & NEWS */}
      <section id="announcements" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-blue-600 mb-1">
              <Flame className="w-4 h-4 text-amber-500" />
              <span>Dolzarb e'lonlar</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Maktab Yangiliklari va Xabarnomalari
            </h2>
          </div>
          <p className="text-xs text-slate-500 max-w-xs">
            Maktab hayoti, o'quv rejalari va muhim tadbirlar haqida rasmiy ma'lumotlar.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {announcements.slice(0, 6).map((ann) => (
            <div
              key={ann.id}
              className={`rounded-2xl border p-6 flex flex-col justify-between transition-all hover:shadow-md ${
                ann.is_pinned 
                  ? 'bg-gradient-to-br from-blue-50/80 to-indigo-50/50 border-blue-200' 
                  : 'bg-white border-slate-200'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full ${
                    ann.category === 'academic' ? 'bg-blue-100 text-blue-800' :
                    ann.category === 'urgent' ? 'bg-rose-100 text-rose-800' :
                    'bg-slate-100 text-slate-700'
                  }`}>
                    {ann.category_display || ann.category}
                  </span>
                  {ann.is_pinned && (
                    <span className="text-[11px] font-bold text-amber-700 bg-amber-100 px-2 py-0.5 rounded-full">
                      Muhim
                    </span>
                  )}
                </div>

                <h3 className="font-bold text-base text-slate-900 mb-2 leading-snug line-clamp-2">
                  {ann.title}
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed mb-4 line-clamp-3">
                  {ann.summary || ann.content}
                </p>
              </div>

              <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span>{new Date(ann.published_at).toLocaleDateString('uz-UZ')}</span>
                <span className="font-medium text-slate-600">{ann.views_count} marta o'qildi</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 3. UPCOMING EVENTS */}
      <section id="events" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-br from-slate-900 to-indigo-950 rounded-3xl p-8 sm:p-12 text-white">
          <div className="max-w-3xl mb-8">
            <span className="text-xs font-bold uppercase tracking-wider text-sky-400 mb-2 block">
              Maktab kalendari
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Yaqinlashib Kelayotgan Tadbirlar va Musobaqalar
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {events.slice(0, 4).map((evt) => (
              <div 
                key={evt.id}
                className="p-5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 hover:bg-white/15 transition-all"
              >
                <div className="flex items-start gap-4">
                  <div className="w-14 h-14 rounded-xl bg-blue-600 flex flex-col items-center justify-center text-white shrink-0 font-bold shadow-md">
                    <span className="text-base leading-none">{new Date(evt.event_date).getDate()}</span>
                    <span className="text-[10px] uppercase font-semibold">
                      {new Date(evt.event_date).toLocaleString('uz-UZ', { month: 'short' })}
                    </span>
                  </div>

                  <div className="space-y-1.5 flex-1">
                    <h4 className="font-bold text-sm sm:text-base leading-tight">
                      {evt.title}
                    </h4>
                    <p className="text-xs text-slate-300 leading-relaxed line-clamp-2">
                      {evt.description}
                    </p>
                    <div className="flex flex-wrap items-center gap-3 text-[11px] text-slate-400 pt-1">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-blue-400" />
                        {evt.start_time?.slice(0, 5)}
                      </span>
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-blue-400" />
                        {evt.location}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 4. TEACHERS & FACULTY */}
      <section id="teachers" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <span className="text-xs font-bold uppercase tracking-wider text-blue-600 mb-1 block">
            Pedagogik jamoa
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Tajribali va Fidoyi O‘qituvchilarimiz
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 mt-2">
            9-Maktab o'quvchilariga xalqaro standartlar asosida ta'lim beruvchi oliy toifali ustozlar.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {teachers.slice(0, 8).map((tch) => (
            <div 
              key={tch.id}
              className="bg-white rounded-2xl border border-slate-200 p-6 text-center shadow-xs hover:shadow-md transition-all group"
            >
              <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-blue-100 to-indigo-100 text-blue-800 font-bold text-xl mx-auto flex items-center justify-center mb-4 group-hover:scale-105 transition-transform border border-blue-200">
                {tch.user?.first_name?.[0] || 'U'}{tch.user?.last_name?.[0] || 'T'}
              </div>
              <h4 className="font-bold text-base text-slate-900 group-hover:text-blue-600 transition-colors">
                {tch.full_name || tch.user?.full_name}
              </h4>
              <p className="text-xs text-blue-600 font-semibold mt-0.5">
                {tch.specialization}
              </p>
              <span className="inline-block text-[11px] text-slate-500 bg-slate-100 px-2.5 py-0.5 rounded-full mt-2">
                {tch.qualification}
              </span>
              <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-400">
                Xona: <span className="font-semibold text-slate-700">{tch.room_number || "Xona 204"}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 5. ACHIEVEMENTS & OLYMPIADS */}
      <section id="achievements" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-amber-600 mb-1 block">
              G'alabalar va e'tiroflar
            </span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              O‘quvchilarimiz Erishgan Yutuqlar
            </h2>
          </div>
          <p className="text-xs text-slate-500 max-w-xs">
            Xalqaro va Respublika olimpiadalari, sport hamda fan musobaqalaridagi faxrli o'rinlar.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {achievements.map((ach) => (
            <div 
              key={ach.id}
              className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs hover:border-amber-300 hover:shadow-md transition-all flex items-start gap-4"
            >
              <div className="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center shrink-0 border border-amber-200">
                <Trophy className="w-6 h-6" />
              </div>
              <div className="space-y-1">
                <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md bg-amber-100 text-amber-800">
                  {ach.category_display || ach.category}
                </span>
                <h4 className="font-bold text-sm text-slate-900 pt-1 leading-snug">
                  {ach.title}
                </h4>
                <p className="text-xs text-blue-600 font-semibold">
                  {ach.winner_name} ({ach.grade_or_role})
                </p>
                <p className="text-xs text-slate-500 leading-relaxed pt-1">
                  {ach.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 6. DIGITAL LIBRARY & LEARNING RESOURCES */}
      <section id="resources" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-slate-50 rounded-3xl p-8 sm:p-12 border border-slate-200">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-blue-600 mb-1 block">
                Elektron resurslar
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                Raqamli Kutubxona va Darsliklar
              </h2>
            </div>
            <p className="text-xs text-slate-500 max-w-sm">
              9-Maktab o'quvchilari va o'qituvchilari uchun tavsiya etilgan darsliklar, taqdimotlar va metodik qo'llanmalar.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resources.map((res) => (
              <div 
                key={res.id}
                className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs flex flex-col justify-between hover:border-blue-400 transition-all"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-[11px] font-semibold text-blue-700 bg-blue-50 px-2 py-0.5 rounded">
                      {res.subject_name || "Fan"}
                    </span>
                    <span className="text-[11px] font-medium text-slate-400">
                      {res.grade_level}-sinf
                    </span>
                  </div>
                  <h4 className="font-bold text-sm text-slate-900 mb-1.5 leading-snug">
                    {res.title}
                  </h4>
                  <p className="text-xs text-slate-500 line-clamp-2">
                    {res.description || "Elektron ta'lim materiali"}
                  </p>
                </div>

                <div className="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-[11px] text-slate-400">
                    {res.downloads_count} marta yuklangan
                  </span>
                  <button
                    onClick={() => handleDownload(res)}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-blue-600 bg-blue-50 hover:bg-blue-100 transition-colors cursor-pointer"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Yuklab olish</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 7. FAQ ACCORDION */}
      <section id="faq" className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <span className="text-xs font-bold uppercase tracking-wider text-blue-600 mb-1 block">
            Savollaringiz bormi?
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Ko‘p Beriladigan Savollar (FAQ)
          </h2>
          <div className="relative max-w-md mx-auto mt-4">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              value={faqSearch}
              onChange={(e) => setFaqSearch(e.target.value)}
              placeholder="Savol bo'yicha qidirish..."
              className="w-full pl-10 pr-4 py-2.5 text-xs bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900 shadow-xs"
            />
          </div>
        </div>

        <div className="space-y-3">
          {filteredFaqs.map((faq, idx) => (
            <div 
              key={faq.id || idx}
              className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs"
            >
              <button
                onClick={() => setActiveFaq(activeFaq === idx ? null : idx)}
                className="w-full px-5 py-4 text-left flex items-center justify-between gap-4 font-semibold text-sm text-slate-800 hover:text-blue-700 transition-colors cursor-pointer"
              >
                <span>{faq.question}</span>
                <ChevronRight className={`w-4 h-4 text-slate-400 transition-transform ${activeFaq === idx ? 'rotate-90 text-blue-600' : ''}`} />
              </button>
              {activeFaq === idx && (
                <div className="px-5 pb-5 text-xs text-slate-600 leading-relaxed border-t border-slate-100 pt-3 bg-slate-50/50">
                  {faq.answer}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* 8. PUBLIC INQUIRY & CONTACT */}
      <section id="contact" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 bg-white rounded-3xl border border-slate-200 p-8 sm:p-12 shadow-sm">
          <div className="lg:col-span-5 space-y-5">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-blue-600 mb-1 block">
                Ochiq muloqot
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                Maktab Ma‘muriyatiga Murojaat Qiling
              </h2>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Maktabga qabul, dars jarayonlari, to'garaklar yoki o'quvchilar masalasida o'z savol va takliflaringizni yuboring. Ma'muriyatimiz 24 soat ichida javob beradi.
            </p>

            <div className="space-y-3 pt-2 text-xs text-slate-600">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-blue-50 text-blue-600">
                  <MapPin className="w-4 h-4" />
                </div>
                <span>Toshkent sh., Yunusobod tumani, Amir Temur sh.k., 45-uy</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-blue-50 text-blue-600">
                  <GraduationCap className="w-4 h-4" />
                </div>
                <span>Direktor: Abdullayev Rustam Karimovich</span>
              </div>
            </div>
          </div>

          {/* Form */}
          <div className="lg:col-span-7">
            {inquiryStatus.success ? (
              <div className="p-8 rounded-2xl bg-emerald-50 border border-emerald-200 text-center space-y-3">
                <CheckCircle className="w-12 h-12 text-emerald-600 mx-auto" />
                <h3 className="font-bold text-lg text-emerald-900">
                  Murojaatingiz muvaffaqiyatli qabul qilindi!
                </h3>
                <p className="text-xs text-emerald-700 max-w-sm mx-auto">
                  Maktab ma'muriyati murojaatingizni ko'rib chiqib, ko'rsatilgan elektron pochta yoki telefon raqamingiz orqali bog'lanadi.
                </p>
                <button
                  onClick={() => setInquiryStatus({ loading: false, success: false, error: null })}
                  className="px-4 py-2 text-xs font-semibold text-emerald-800 bg-emerald-100 hover:bg-emerald-200 rounded-lg transition-colors"
                >
                  Yangi murojaat yuborish
                </button>
              </div>
            ) : (
              <form onSubmit={handleInquirySubmit} className="space-y-4">
                {inquiryStatus.error && (
                  <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800">
                    {inquiryStatus.error}
                  </div>
                )}

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      F.I.Sh. *
                    </label>
                    <input
                      type="text"
                      required
                      value={inquiry.full_name}
                      onChange={(e) => setInquiry({ ...inquiry, full_name: e.target.value })}
                      placeholder="Masalan: Azizbek Karimov"
                      className="w-full px-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Telefon raqami *
                    </label>
                    <input
                      type="tel"
                      required
                      value={inquiry.phone}
                      onChange={(e) => setInquiry({ ...inquiry, phone: e.target.value })}
                      placeholder="+998 90 123 45 67"
                      className="w-full px-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Elektron pochta *
                    </label>
                    <input
                      type="email"
                      required
                      value={inquiry.email}
                      onChange={(e) => setInquiry({ ...inquiry, email: e.target.value })}
                      placeholder="email@misol.uz"
                      className="w-full px-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">
                      Murojaat mavzusi *
                    </label>
                    <input
                      type="text"
                      required
                      value={inquiry.subject}
                      onChange={(e) => setInquiry({ ...inquiry, subject: e.target.value })}
                      placeholder="Masalan: Qabul shartlari haqida"
                      className="w-full px-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-700 mb-1">
                    Murojaat matni *
                  </label>
                  <textarea
                    rows={4}
                    required
                    value={inquiry.message}
                    onChange={(e) => setInquiry({ ...inquiry, message: e.target.value })}
                    placeholder="Murojaatingizni batafsil bayon eting..."
                    className="w-full px-3.5 py-2.5 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600/30 text-slate-900"
                  />
                </div>

                <button
                  type="submit"
                  disabled={inquiryStatus.loading}
                  className="px-6 py-3 rounded-xl font-bold text-xs text-white bg-blue-600 hover:bg-blue-700 transition-all flex items-center gap-2 cursor-pointer disabled:opacity-50"
                >
                  <Send className="w-4 h-4" />
                  <span>{inquiryStatus.loading ? "Yuborilmoqda..." : "Murojaatni yuborish"}</span>
                </button>
              </form>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
