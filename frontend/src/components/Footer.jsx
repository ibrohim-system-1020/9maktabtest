import React from 'react';
import { GraduationCap, Phone, Mail, MapPin, ExternalLink, Heart } from 'lucide-react';

export default function Footer({ onNavigate }) {
  return (
    <footer className="bg-slate-900 text-slate-400 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
          {/* Col 1: School Identity */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white">
                <GraduationCap className="w-6 h-6" />
              </div>
              <div>
                <span className="font-bold text-lg text-white tracking-tight">
                  9-MAKTAB
                </span>
                <p className="text-[11px] text-blue-400 font-medium">
                  Umumiy o‘rta ta‘lim maktabi
                </p>
              </div>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Toshkent shahar Yunusobod tumanidagi chuqurlashtirilgan aniq fanlar va zamonaviy AKT texnologiyalariga ixtisoslashgan yetakchi ta'lim muassasasi.
            </p>
            <div className="text-xs text-slate-500">
              © {new Date().getFullYear()} 9-Maktab. Barcha huquqlar himoyalangan.
            </div>
          </div>

          {/* Col 2: Navigation */}
          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4">
              Tezkor o'tish
            </h4>
            <ul className="space-y-2 text-xs">
              <li>
                <button onClick={() => onNavigate('about')} className="hover:text-white transition-colors">
                  Maktab tarixi va ma'muriyati
                </button>
              </li>
              <li>
                <button onClick={() => onNavigate('teachers')} className="hover:text-white transition-colors">
                  Pedagogik jamoa
                </button>
              </li>
              <li>
                <button onClick={() => onNavigate('subjects')} className="hover:text-white transition-colors">
                  O'quv dasturlari va fanlar
                </button>
              </li>
              <li>
                <button onClick={() => onNavigate('announcements')} className="hover:text-white transition-colors">
                  Rasmiy yangiliklar va e'lonlar
                </button>
              </li>
              <li>
                <button onClick={() => onNavigate('resources')} className="hover:text-white transition-colors">
                  Raqamli kutubxona va darsliklar
                </button>
              </li>
              <li>
                <button onClick={() => onNavigate('faq')} className="hover:text-white transition-colors">
                  Ko'p beriladigan savollar (FAQ)
                </button>
              </li>
            </ul>
          </div>

          {/* Col 3: Official Portals */}
          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4">
              Davlat portallari
            </h4>
            <ul className="space-y-2.5 text-xs">
              <li>
                <a 
                  href="https://uzedu.uz" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 hover:text-white transition-colors"
                >
                  <span>Maktabgacha va maktab ta'limi vazirligi</span>
                  <ExternalLink className="w-3 h-3 text-slate-600" />
                </a>
              </li>
              <li>
                <a 
                  href="https://my.maktab.uz" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 hover:text-white transition-colors"
                >
                  <span>Elektron maktab qabuli (my.maktab.uz)</span>
                  <ExternalLink className="w-3 h-3 text-slate-600" />
                </a>
              </li>
              <li>
                <a 
                  href="https://kundalik.com" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 hover:text-white transition-colors"
                >
                  <span>eMaktab / Kundalik tizimi</span>
                  <ExternalLink className="w-3 h-3 text-slate-600" />
                </a>
              </li>
              <li>
                <a 
                  href="https://gov.uz" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 hover:text-white transition-colors"
                >
                  <span>O'zbekiston Respublikasi Hukumati</span>
                  <ExternalLink className="w-3 h-3 text-slate-600" />
                </a>
              </li>
            </ul>
          </div>

          {/* Col 4: Contact info */}
          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-4">
              Bog'lanish
            </h4>
            <ul className="space-y-3 text-xs">
              <li className="flex items-start gap-2.5">
                <MapPin className="w-4 h-4 text-blue-500 shrink-0 mt-0.5" />
                <span>Toshkent shahri, Yunusobod tumani, Amir Temur shoh ko‘chasi, 45-uy</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Phone className="w-4 h-4 text-blue-500 shrink-0" />
                <span>+998 (71) 234-56-78</span>
              </li>
              <li className="flex items-center gap-2.5">
                <Mail className="w-4 h-4 text-blue-500 shrink-0" />
                <span>info@9maktab.uz</span>
              </li>
            </ul>
            <div className="mt-4 p-2.5 rounded-lg bg-slate-800/60 border border-slate-700/50 text-[11px] text-slate-300">
              <span className="font-semibold text-white">Qabul kunlari:</span> Dushanba — Juma, 08:30 - 17:00
            </div>
          </div>
        </div>

        <div className="mt-12 pt-6 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-3">
          <p>
            9-Maktab Smart School Management Platform — Ultra Pro Max Edition
          </p>
          <p className="flex items-center gap-1">
            <span>O'zbekiston yoshlari uchun yaratildi</span>
            <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500" />
          </p>
        </div>
      </div>
    </footer>
  );
}
