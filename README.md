# 9-MAKTAB — ULTRA-PRO MAX SMART SCHOOL MANAGEMENT PLATFORM

> **Toshkent shahri Yunusobod tumani 9-sonli umumiy o‘rta ta‘lim maktabining yagona raqamli ta'lim, boshqaruv va tahliliy monitoring platformasi.**

---

## 🌟 1. Loyiha haqida va Asosiy Imkoniyatlar

**9-Maktab Ultra-Pro Max** — bu zamonaviy ta'lim muassasasi ehtiyojlariga moslashtirilgan, o'quvchilar, o'qituvchilar, ota-onalar va maktab ma'muriyatini yagona ekotizimda birlashtiruvchi to'liq funksional dasturiy majmuadir.

### Asosiy Imkoniyatlar:
1. **Rasmiy Institutsional Veb-Portal:**
   - Maktab tarixi, rahbariyat, pedagogik jamoa va kafedralar
   - Dolzarb yangiliklar, e'lonlar, maktab tadbirlari va xalqaro olimpiada yutuqlari
   - Raqamli kutubxona (elektron darsliklar va metodik qo'llanmalar, yuklab olish hisoblagichi)
   - Ko'p beriladigan savollar (FAQ) va qidiruv tizimi
   - Fuqarolar va ota-onalar uchun onlayn murojaat shakli (Inquiry form)

2. **Rollar Asosidagi Xavfsiz Boshqaruv (RBAC):**
   - **Bosh Administrator (Super Admin):** Tizim to'liq nazorati, audit jurnali, foydalanuvchilar boshqaruvi
   - **Maktab Administratori:** Sinflar, dars jadvali, fanlar va hisobotlar boshqaruvi
   - **Direktor / Rahbariyat:** Boshqaruv statistikasi va pedagogik monitoring
   - **O'qituvchi:** O'z sinflari, tezkor davomat olish, uy vazifalari e'lon qilish, topshiriqlarni tekshirish va baholash (BSB / CHSB)
   - **O'quvchi:** Shaxsiy dars jadvali, topshiriqlar topshirish, olingan baholar va o'zlashtirish tahlili
   - **Ota-ona (Guardian):** Farzandiga bog'langan profil, real vaqt davomati, baholari va dars jadvali

3. **Ultra Tahlil va Statistika Dvigateli (Analytics Engine):**
   - Real ma'lumotlar bazasi so'rovlari asosida ishlovchi tahlillar
   - **Davomat formulasi:** `(Hozir + Kechikkan) / Jami qaydlar * 100`
   - 14 kunlik interaktiv davomat grafigi (Area Chart)
   - Milliy 5 balli tizim bo'yicha baholar taqsimoti (Grade 5, 4, 3, 2 Bar Chart)
   - Fanlar va sinflar bo'yicha sifat ko'rsatkichi (`(5+4)/Jami * 100`) va o'zlashtirish foizi
   - Surunkali dars qoldiruvchi o'quvchilar bo'yicha avtomatik ogohlantirishlar
   - 1-klikda CSV eksport: Davomat, Baholar, O'quvchilar ro'yxati

---

## 🛠️ 2. Texnologik Stek

- **Backend:** Python, Django 6.1, Django REST Framework, SimpleJWT, WhiteNoise
- **Ma'lumotlar bazasi:** SQLite (mahalliy ishlanma uchun), PostgreSQL (ishlab chiqarish uchun tayyor)
- **Frontend:** React 19, Vite, Tailwind CSS, Lucide React, Recharts
- **API Hujjatlari:** OpenAPI / Swagger UI interaktiv interfeysi (`/api/docs/`)
- **Tizim monitoringi:** Healthcheck endpoint (`/health/`, `/api/health/`)

---

## 🚀 3. Tizimni Ishga Tushirish (Windows)

### 3.1. Backendni ishga tushirish:
```powershell
# 1. Loyiha papkasiga o'ting
cd E:\9-maktab\backend

# 2. Migratsiyalarni tekshiring va qo'llang
python manage.py migrate

# 3. Namunaviy ma'lumotlarni bazaga yuklang (agar hali yuklanmagan bo'lsa)
python manage.py seed_demo_data

# 4. Django serverini ishga tushiring
python manage.py runserver 127.0.0.1:8000
```

Backend manzillari:
- **Asosiy sahifa (Frontend integratsiyasi):** `http://127.0.0.1:8000/`
- **Swagger API Hujjatlari:** `http://127.0.0.1:8000/api/docs/`
- **Tizim holati (Healthcheck):** `http://127.0.0.1:8000/health/`
- **Django Admin:** `http://127.0.0.1:8000/admin/`

---

### 3.2. Frontendni ishga tushirish (Ishlab chiquvchi rejimi):
```powershell
# 1. Frontend papkasiga o'ting
cd E:\9-maktab\frontend

# 2. Vite serverini ishga tushiring
cmd /c npm run dev
```

Frontend rivojlantirish manzili:
- `http://localhost:5173/`

### 3.3. Frontendni ishlab chiqarish uchun yig'ish (Production Build):
```powershell
cd E:\9-maktab\frontend
cmd /c npm run build
```
*(Yig'ilgan `dist/index.html` avtomatik tarzda Django orqali `http://127.0.0.1:8000/` manzilida ham xizmat ko'rsatadi).*

---

## 🔑 4. Namunaviy Test Akkauntlari

Tizimni tezkor sinash uchun quyidagi oldindan tayyorlangan profillardan foydalanishingiz mumkin:

| Rol | Login / Username | Parol | Mas'ul shaxs |
| :--- | :--- | :--- | :--- |
| **Bosh Administrator** | `admin` | `Password123!` | Bosh Administrator |
| **Maktab Admini** | `school_admin` | `Password123!` | Nozima Qosimova |
| **Direktor** | `direktor` | `Password123!` | Abdullayev Rustam Karimovich |
| **O'qituvchi** | `teacher_math` | `Password123!` | Nilufar Sobirova (Matematika) |
| **O'quvchi (9-A)** | `student_jasur` | `Password123!` | Jasur Alimov (9M-2026-001) |
| **Ota-ona** | `parent_alimov` | `Password123!` | Otabek Alimov (Jasurning otasi) |

*Kirish oynasida har bir rol uchun **1-klikda to'ldirish** tugmalari mavjud.*

---

## 🧪 5. Avtomatlashtirilgan Testlar

Loyiha bo'yicha backend testlarini ishga tushirish:
```powershell
cd E:\9-maktab
python backend/manage.py test tests
```
Barcha 6 ta asosiy sinov (JWT autentifikatsiya, ruxsatlar izolyatsiyasi, davomat formulalari, vazifalar hayotiy sikli va murojaat ish oqimi) 100% muvaffaqiyatli o'tadi.
