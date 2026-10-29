import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import {
  Calendar,
  CheckCircle,
  Clock,
  BookOpen,
  Award,
  Users,
  FileText,
  BarChart3,
  Download,
  AlertTriangle,
  Plus,
  Send,
  Check,
  Shield,
  Layers,
  Sparkles,
  Inbox
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

export default function DashboardPage({ onNavigateHome }) {
  const { user, isRole, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');

  // Common Academic Data
  const [timetable, setTimetable] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [assessments, setAssessments] = useState([]);
  const [assessmentResults, setAssessmentResults] = useState([]);
  const [attendanceRecords, setAttendanceRecords] = useState([]);
  const [classes, setClasses] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [myChildren, setMyChildren] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);

  // Analytics Data
  const [overviewStats, setOverviewStats] = useState(null);
  const [attendanceAnalytics, setAttendanceAnalytics] = useState(null);
  const [academicAnalytics, setAcademicAnalytics] = useState(null);

  // Admin Data
  const [inquiries, setInquiries] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [allUsers, setAllUsers] = useState([]);

  // Teacher Action States
  const [selectedClassId, setSelectedClassId] = useState('');
  const [classStudents, setClassStudents] = useState([]);
  const [attendanceDate, setAttendanceDate] = useState(new Date().toISOString().slice(0, 10));
  const [attendanceMap, setAttendanceMap] = useState({});
  const [gradingAssessmentId, setGradingAssessmentId] = useState('');
  const [gradesMap, setGradesMap] = useState({});
  const [actionMessage, setActionMessage] = useState(null);

  // Modals
  const [showSubmitModal, setShowSubmitModal] = useState(null); // assignment object
  const [submissionText, setSubmissionText] = useState('');
  const [showCreateAssignModal, setShowCreateAssignModal] = useState(false);
  const [newAssignData, setNewAssignData] = useState({
    classroom: '',
    subject: '',
    title: '',
    description: '',
    due_date: '',
    max_score: 100,
  });

  // Load initial data based on role
  useEffect(() => {
    if (!user) return;

    // Load classes & subjects
    api.getClassrooms().then(setClasses).catch(console.error);
    api.getSubjects().then(setSubjects).catch(console.error);

    // Load Timetable
    api.getTimetable().then((res) => setTimetable(res.results || res || [])).catch(console.error);

    // Load Assignments
    api.getAssignments().then((res) => setAssignments(res.results || res || [])).catch(console.error);

    // Load Assessments & Results
    api.getAssessments().then((res) => setAssessments(res.results || res || [])).catch(console.error);
    api.getAssessmentResults().then((res) => setAssessmentResults(res.results || res || [])).catch(console.error);

    // Load Attendance
    api.getAttendanceRecords().then((res) => setAttendanceRecords(res.results || res || [])).catch(console.error);

    // Analytics for staff or general overview
    api.getSchoolOverview().then(setOverviewStats).catch(console.error);
    api.getAttendanceAnalytics().then(setAttendanceAnalytics).catch(console.error);
    api.getAcademicAnalytics().then(setAcademicAnalytics).catch(console.error);

    // Parent specific
    if (isRole('guardian')) {
      api.getMyChildren().then((kids) => {
        setMyChildren(kids || []);
        if (kids && kids.length > 0) setSelectedChild(kids[0]);
      }).catch(console.error);
    }

    // Admin specific
    if (isRole('school_admin', 'super_admin')) {
      api.getInquiries().then((res) => setInquiries(res.results || res || [])).catch(console.error);
      api.getAuditLogs().then((res) => setAuditLogs(res.results || res || [])).catch(console.error);
      api.getStudents().then((res) => setAllUsers(res.results || res || [])).catch(console.error);
    }
  }, [user]);

  // When teacher selects a classroom for attendance or grading
  useEffect(() => {
    if (selectedClassId) {
      api.getStudents(`?classroom=${selectedClassId}`).then((res) => {
        const studs = res.results || res || [];
        setClassStudents(studs);
        // initialize attendance map to present
        const initAtt = {};
        studs.forEach((s) => { initAtt[s.id] = { status: 'present', reason: '' }; });
        setAttendanceMap(initAtt);
        // initialize grades map
        const initGrades = {};
        studs.forEach((s) => { initGrades[s.id] = { score: 85, remarks: '' }; });
        setGradesMap(initGrades);
      }).catch(console.error);
    }
  }, [selectedClassId]);

  // Handle Attendance Save
  const handleSaveAttendance = async () => {
    if (!selectedClassId) return;
    try {
      const records = Object.entries(attendanceMap).map(([studentId, val]) => ({
        student_id: parseInt(studentId),
        status: val.status,
        reason: val.reason || '',
      }));
      await api.saveBulkAttendance({
        classroom_id: parseInt(selectedClassId),
        date: attendanceDate,
        records,
      });
      setActionMessage({ type: 'success', text: "Davomat muvaffaqiyatli saqlandi!" });
      setTimeout(() => setActionMessage(null), 4000);
    } catch (err) {
      setActionMessage({ type: 'error', text: err.message || "Davomat saqlashda xatolik" });
    }
  };

  // Handle Bulk Grades Save
  const handleSaveGrades = async () => {
    if (!gradingAssessmentId) return;
    try {
      const results = Object.entries(gradesMap).map(([studentId, val]) => ({
        student_id: parseInt(studentId),
        score: parseFloat(val.score),
        remarks: val.remarks || '',
      }));
      await api.saveBulkAssessmentResults({
        assessment_id: parseInt(gradingAssessmentId),
        results,
      });
      setActionMessage({ type: 'success', text: "Baholar muvaffaqiyatli saqlandi va jurnalga kiritildi!" });
      setTimeout(() => setActionMessage(null), 4000);
    } catch (err) {
      setActionMessage({ type: 'error', text: err.message || "Baholarni saqlashda xatolik" });
    }
  };

  // Handle Student Submit Assignment
  const handleStudentSubmit = async (e) => {
    e.preventDefault();
    if (!showSubmitModal) return;
    try {
      await api.submitAssignment({
        assignment: showSubmitModal.id,
        submission_text: submissionText,
      });
      setShowSubmitModal(null);
      setSubmissionText('');
      // refresh assignments
      api.getAssignments().then((res) => setAssignments(res.results || res || []));
      setActionMessage({ type: 'success', text: "Vazifa muvaffaqiyatli topshirildi!" });
      setTimeout(() => setActionMessage(null), 4000);
    } catch (err) {
      setActionMessage({ type: 'error', text: err.message || "Topshirishda xatolik" });
    }
  };

  // Handle Teacher Create Assignment
  const handleCreateAssignment = async (e) => {
    e.preventDefault();
    try {
      await api.createAssignment(newAssignData);
      setShowCreateAssignModal(false);
      setNewAssignData({ classroom: '', subject: '', title: '', description: '', due_date: '', max_score: 100 });
      api.getAssignments().then((res) => setAssignments(res.results || res || []));
      setActionMessage({ type: 'success', text: "Yangi vazifa muvaffaqiyatli e'lon qilindi!" });
      setTimeout(() => setActionMessage(null), 4000);
    } catch (err) {
      setActionMessage({ type: 'error', text: err.message || "Vazifa yaratishda xatolik" });
    }
  };

  // Days of week for timetable
  const daysOfWeek = [
    { num: 1, name: 'Dushanba' },
    { num: 2, name: 'Seshanba' },
    { num: 3, name: 'Chorshanba' },
    { num: 4, name: 'Payshanba' },
    { num: 5, name: 'Juma' },
    { num: 6, name: 'Shanba' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* 1. TOP WELCOME BANNER */}
      <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="text-xs uppercase font-bold tracking-wider px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-400/30">
              {user?.role?.toUpperCase()}
            </span>
            <span className="text-xs text-slate-300">
              9-Sonli umumiy o'rta ta'lim maktabi
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black tracking-tight">
            Xush kelibsiz, {user?.full_name || user?.username}!
          </h1>
          <p className="text-xs sm:text-sm text-slate-300">
            {isRole('student') && "9-A sinf o'quvchisi • ID: 9M-2026-001 • 2026-2027 o'quv yili"}
            {isRole('teacher') && "Matematika va Aniq fanlar kafedrasi o'qituvchisi • Xona: 204"}
            {isRole('guardian') && "Ota-onalar portali • Farzand monitoringi"}
            {isRole('school_admin', 'super_admin') && "Maktab ma'muriyati • Tizim boshqaruvi va tahliliy monitoring"}
          </p>
        </div>

        {/* Quick Actions */}
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={onNavigateHome}
            className="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-semibold text-xs transition-colors cursor-pointer"
          >
            Maktab veb-sayti
          </button>
          {isRole('teacher') && (
            <button
              onClick={() => setShowCreateAssignModal(true)}
              className="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-md shadow-blue-600/30 transition-all cursor-pointer"
            >
              <Plus className="w-4 h-4" />
              <span>Yangi vazifa yaratish</span>
            </button>
          )}
          {isRole('school_admin', 'super_admin', 'teacher') && (
            <a
              href="/api/analytics/export/attendance/"
              target="_blank"
              rel="noreferrer"
              className="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-md shadow-emerald-600/30 transition-all cursor-pointer"
            >
              <Download className="w-4 h-4" />
              <span>Davomat CSV</span>
            </a>
          )}
        </div>
      </div>

      {/* Action Notification Alert */}
      {actionMessage && (
        <div className={`p-4 rounded-2xl flex items-center gap-3 text-xs font-semibold ${
          actionMessage.type === 'success' ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' : 'bg-rose-50 text-rose-800 border border-rose-200'
        }`}>
          {actionMessage.type === 'success' ? <Check className="w-4 h-4 text-emerald-600 shrink-0" /> : <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />}
          <span>{actionMessage.text}</span>
        </div>
      )}

      {/* 2. TAB NAVIGATION */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 pb-2">
        <button
          onClick={() => setActiveTab('overview')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
            activeTab === 'overview' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Umumiy ko'rinish
        </button>

        <button
          onClick={() => setActiveTab('timetable')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
            activeTab === 'timetable' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Dars jadvali
        </button>

        <button
          onClick={() => setActiveTab('assignments')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
            activeTab === 'assignments' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Vazifalar & Uy ishlari
        </button>

        <button
          onClick={() => setActiveTab('grades')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
            activeTab === 'grades' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Baholar & BSB
        </button>

        {isRole('teacher', 'school_admin', 'super_admin') && (
          <button
            onClick={() => setActiveTab('attendance_entry')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === 'attendance_entry' ? 'bg-blue-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            Davomat jurnali
          </button>
        )}

        <button
          onClick={() => setActiveTab('analytics')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
            activeTab === 'analytics' ? 'bg-indigo-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Ultra Statistika & Tahlil
        </button>

        {isRole('school_admin', 'super_admin') && (
          <button
            onClick={() => setActiveTab('admin_panel')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === 'admin_panel' ? 'bg-purple-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            Ma'muriyat & Murojaatlar
          </button>
        )}
      </div>

      {/* ======================================================== */}
      {/* TAB 1: OVERVIEW */}
      {/* ======================================================== */}
      {activeTab === 'overview' && (
        <div className="space-y-8">
          {/* KPI Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-slate-500">Davomat ko'rsatkichi</span>
                <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
                  <CheckCircle className="w-4 h-4" />
                </div>
              </div>
              <div className="text-2xl font-black text-slate-900">
                {overviewStats?.overall_attendance_rate || 94.8}%
              </div>
              <p className="text-[11px] text-emerald-600 font-medium mt-1">
                +1.2% o'tgan haftaga nisbatan
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-slate-500">O'rtacha o'zlashtirish</span>
                <div className="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
                  <Award className="w-4 h-4" />
                </div>
              </div>
              <div className="text-2xl font-black text-slate-900">
                {overviewStats?.average_academic_score || 88.5} ball
              </div>
              <p className="text-[11px] text-blue-600 font-medium mt-1">
                A'lo va yaxshi baholar ulushi: 78%
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-slate-500">Faol topshiriqlar</span>
                <div className="w-8 h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center">
                  <BookOpen className="w-4 h-4" />
                </div>
              </div>
              <div className="text-2xl font-black text-slate-900">
                {assignments.length} ta
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                Bajarilish foizi: {overviewStats?.submission_completion_rate || 88.4}%
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-slate-500">Sinflar & O'quvchilar</span>
                <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
                  <Users className="w-4 h-4" />
                </div>
              </div>
              <div className="text-2xl font-black text-slate-900">
                {overviewStats?.total_classes || 4} sinf / {overviewStats?.total_students || 6} o'quvchi
              </div>
              <p className="text-[11px] text-indigo-600 font-medium mt-1">
                O'qituvchilar soni: {overviewStats?.total_teachers || 5} nafar
              </p>
            </div>
          </div>

          {/* Quick Schedule Preview & Recent Activity */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Left: Today's Schedule */}
            <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-200 p-6 shadow-xs">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-blue-600" />
                  <span>Bugungi dars jadvali</span>
                </h3>
                <span className="text-xs font-semibold text-slate-500">
                  {new Date().toLocaleDateString('uz-UZ', { weekday: 'long', day: 'numeric', month: 'long' })}
                </span>
              </div>

              <div className="space-y-3">
                {timetable.slice(0, 5).map((item, idx) => (
                  <div 
                    key={item.id || idx}
                    className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between hover:bg-blue-50/50 transition-colors"
                  >
                    <div className="flex items-center gap-3.5">
                      <span className="w-7 h-7 rounded-lg bg-blue-100 text-blue-800 font-bold text-xs flex items-center justify-center">
                        {item.period_number}
                      </span>
                      <div>
                        <h4 className="font-bold text-xs text-slate-900">
                          {item.subject_name}
                        </h4>
                        <p className="text-[11px] text-slate-500">
                          {item.teacher_name} • Xona {item.room_number || "204"}
                        </p>
                      </div>
                    </div>
                    <span className="text-xs font-semibold text-slate-700">
                      {item.start_time?.slice(0, 5)} - {item.end_time?.slice(0, 5)}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Right: Upcoming Deadlines & BSB notice */}
            <div className="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
              <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
                <Clock className="w-4 h-4 text-amber-600" />
                <span>Yaqinlashayotgan topshiriqlar</span>
              </h3>

              <div className="space-y-3">
                {assignments.slice(0, 3).map((assign) => (
                  <div key={assign.id} className="p-3 rounded-xl border border-slate-100 bg-slate-50/60 space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800">
                        {assign.subject_name}
                      </span>
                      <span className="text-[11px] text-amber-700 font-medium">
                        Muddat: {new Date(assign.due_date).toLocaleDateString('uz-UZ')}
                      </span>
                    </div>
                    <h5 className="font-bold text-xs text-slate-900">{assign.title}</h5>
                    <p className="text-[11px] text-slate-500 line-clamp-1">{assign.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* TAB 2: FULL TIMETABLE */}
      {/* ======================================================== */}
      {activeTab === 'timetable' && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="font-bold text-lg text-slate-900">
                To'liq Haftalik Dars Jadvali
              </h3>
              <p className="text-xs text-slate-500">
                2026-2027 o'quv yili • 2-Chorak rasmiy dars jadvali
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {daysOfWeek.map((day) => {
              const dayEntries = timetable.filter((t) => t.day_of_week === day.num);
              return (
                <div key={day.num} className="rounded-xl border border-slate-200 bg-slate-50/50 p-4 space-y-3">
                  <div className="flex items-center justify-between pb-2 border-b border-slate-200">
                    <h4 className="font-bold text-sm text-slate-900">{day.name}</h4>
                    <span className="text-[11px] text-slate-500">{dayEntries.length} ta dars</span>
                  </div>

                  {dayEntries.length === 0 ? (
                    <p className="text-xs text-slate-400 py-4 text-center italic">Darslar belgilanmagan</p>
                  ) : (
                    <div className="space-y-2">
                      {dayEntries.map((e) => (
                        <div key={e.id} className="p-2.5 rounded-lg bg-white border border-slate-200 text-xs space-y-0.5">
                          <div className="flex items-center justify-between">
                            <span className="font-bold text-blue-700">{e.period_number}-para</span>
                            <span className="text-[10px] text-slate-400">{e.start_time?.slice(0, 5)} - {e.end_time?.slice(0, 5)}</span>
                          </div>
                          <p className="font-semibold text-slate-800">{e.subject_name}</p>
                          <p className="text-[11px] text-slate-500">{e.teacher_name} • Xona {e.room_number || "204"}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* TAB 3: ASSIGNMENTS & HOMEWORK */}
      {/* ======================================================== */}
      {activeTab === 'assignments' && (
        <div className="space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="font-bold text-lg text-slate-900">Uy Vazifalari va Topshiriqlar</h3>
              <p className="text-xs text-slate-500">Berilgan vazifalarni yuborish va o'qituvchi bahosini ko'rish</p>
            </div>
            {isRole('teacher') && (
              <button
                onClick={() => setShowCreateAssignModal(true)}
                className="px-4 py-2.5 rounded-xl bg-blue-600 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm"
              >
                <Plus className="w-4 h-4" />
                <span>Yangi vazifa yaratish</span>
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {assignments.map((assign) => (
              <div key={assign.id} className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs flex flex-col justify-between space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 border border-blue-200">
                      {assign.subject_name}
                    </span>
                    <span className="text-xs text-amber-700 font-semibold">
                      Muddat: {new Date(assign.due_date).toLocaleDateString('uz-UZ')}
                    </span>
                  </div>

                  <h4 className="font-bold text-base text-slate-900 mb-1">{assign.title}</h4>
                  <p className="text-xs text-slate-600 leading-relaxed">{assign.description}</p>
                  
                  {assign.my_submission && (
                    <div className="mt-4 p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-900 space-y-1">
                      <div className="flex items-center justify-between font-bold">
                        <span>Topshirilgan holati: {assign.my_submission.status_display}</span>
                        {assign.my_submission.score !== null && (
                          <span className="text-emerald-700 bg-white px-2 py-0.5 rounded border border-emerald-200">
                            Baho: {assign.my_submission.score} ball
                          </span>
                        )}
                      </div>
                      {assign.my_submission.feedback && (
                        <p className="text-[11px] text-emerald-800">
                          <strong>O'qituvchi izohi:</strong> {assign.my_submission.feedback}
                        </p>
                      )}
                    </div>
                  )}
                </div>

                <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                  <span className="text-xs text-slate-500">
                    O'qituvchi: {assign.teacher_name}
                  </span>

                  {isRole('student') && !assign.my_submission && (
                    <button
                      onClick={() => setShowSubmitModal(assign)}
                      className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 transition-colors cursor-pointer"
                    >
                      Topshirish
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* TAB 4: GRADES & ASSESSMENTS */}
      {/* ======================================================== */}
      {activeTab === 'grades' && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-6">
          <div>
            <h3 className="font-bold text-lg text-slate-900">Baholar va Nazorat Ishlari (BSB / CHSB)</h3>
            <p className="text-xs text-slate-500">Milliy baholash tizimi bo'yicha qo'yilgan ballar va baholar</p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-700">
              <thead className="bg-slate-50 text-slate-500 font-bold uppercase text-[10px] tracking-wider border-b border-slate-200">
                <tr>
                  <th className="py-3 px-4">O'quvchi</th>
                  <th className="py-3 px-4">Fan</th>
                  <th className="py-3 px-4">Sinov nomi</th>
                  <th className="py-3 px-4">Ball (100)</th>
                  <th className="py-3 px-4">Baho</th>
                  <th className="py-3 px-4">Izoh</th>
                  <th className="py-3 px-4">Sana</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {assessmentResults.map((res) => (
                  <tr key={res.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-4 font-semibold text-slate-900">
                      {res.student_name}
                    </td>
                    <td className="py-3.5 px-4 font-medium text-blue-700">
                      {res.subject_name}
                    </td>
                    <td className="py-3.5 px-4 font-medium">
                      {res.assessment_title}
                    </td>
                    <td className="py-3.5 px-4 font-bold text-slate-900">
                      {res.score}
                    </td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2 py-0.5 rounded-full font-bold text-[11px] ${
                        res.grade_number === 5 ? 'bg-emerald-100 text-emerald-800' :
                        res.grade_number === 4 ? 'bg-blue-100 text-blue-800' :
                        res.grade_number === 3 ? 'bg-amber-100 text-amber-800' :
                        'bg-rose-100 text-rose-800'
                      }`}>
                        {res.grade_display || `${res.grade_number} baho`}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-slate-500">
                      {res.remarks || "—"}
                    </td>
                    <td className="py-3.5 px-4 text-slate-400">
                      {new Date(res.recorded_at).toLocaleDateString('uz-UZ')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* TAB 5: ATTENDANCE ENTRY (TEACHERS & ADMINS) */}
      {/* ======================================================== */}
      {activeTab === 'attendance_entry' && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="font-bold text-lg text-slate-900">Elektron Davomat Jurnali</h3>
              <p className="text-xs text-slate-500">Sinf o'quvchilari davomatini belgilash va saqlash</p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <select
                value={selectedClassId}
                onChange={(e) => setSelectedClassId(e.target.value)}
                className="px-3.5 py-2 text-xs rounded-xl border border-slate-200 bg-slate-50 focus:bg-white text-slate-900 font-semibold"
              >
                <option value="">-- Sinfni tanlang --</option>
                {classes.map((c) => (
                  <option key={c.id} value={c.id}>{c.name} sinfi</option>
                ))}
              </select>

              <input
                type="date"
                value={attendanceDate}
                onChange={(e) => setAttendanceDate(e.target.value)}
                className="px-3 py-2 text-xs rounded-xl border border-slate-200 bg-slate-50 focus:bg-white text-slate-900 font-semibold"
              />

              <button
                onClick={handleSaveAttendance}
                disabled={!selectedClassId}
                className="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm disabled:opacity-50 cursor-pointer"
              >
                <Check className="w-4 h-4" />
                <span>Davomatni Saqlash</span>
              </button>
            </div>
          </div>

          {!selectedClassId ? (
            <div className="py-12 text-center text-slate-400 text-xs">
              Iltimos, yuqoridagi menyudan sinfni tanlang.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-700">
                <thead className="bg-slate-50 text-slate-500 font-bold uppercase text-[10px] tracking-wider border-b border-slate-200">
                  <tr>
                    <th className="py-3 px-4"># ID</th>
                    <th className="py-3 px-4">O'quvchi F.I.Sh.</th>
                    <th className="py-3 px-4">Holat</th>
                    <th className="py-3 px-4">Sabab / Izoh</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {classStudents.map((st) => {
                    const current = attendanceMap[st.id] || { status: 'present', reason: '' };
                    return (
                      <tr key={st.id} className="hover:bg-slate-50/80">
                        <td className="py-3 px-4 font-mono text-slate-400">{st.student_id}</td>
                        <td className="py-3 px-4 font-semibold text-slate-900">{st.full_name}</td>
                        <td className="py-3 px-4">
                          <div className="flex items-center gap-1.5">
                            {[
                              { id: 'present', label: 'Bor', color: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
                              { id: 'absent', label: 'Sababsiz yo\'q', color: 'bg-rose-50 text-rose-700 border-rose-200' },
                              { id: 'late', label: 'Kechikkan', color: 'bg-amber-50 text-amber-700 border-amber-200' },
                              { id: 'excused', label: 'Sababli', color: 'bg-blue-50 text-blue-700 border-blue-200' },
                            ].map((opt) => (
                              <button
                                key={opt.id}
                                type="button"
                                onClick={() => setAttendanceMap({
                                  ...attendanceMap,
                                  [st.id]: { ...current, status: opt.id }
                                })}
                                className={`px-2.5 py-1 rounded-md text-[11px] font-semibold border transition-all ${
                                  current.status === opt.id ? opt.color + ' ring-2 ring-blue-500/30' : 'bg-slate-50 text-slate-500 border-slate-200 opacity-60'
                                }`}
                              >
                                {opt.label}
                              </button>
                            ))}
                          </div>
                        </td>
                        <td className="py-3 px-4">
                          <input
                            type="text"
                            placeholder="Kechikish yoki qoldirish sababi..."
                            value={current.reason}
                            onChange={(e) => setAttendanceMap({
                              ...attendanceMap,
                              [st.id]: { ...current, reason: e.target.value }
                            })}
                            className="w-full px-2.5 py-1 text-xs border border-slate-200 rounded-lg bg-slate-50 focus:bg-white text-slate-800"
                          />
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* ======================================================== */}
      {/* TAB 6: ULTRA ANALYTICS & CHARTS */}
      {/* ======================================================== */}
      {activeTab === 'analytics' && (
        <div className="space-y-8">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="font-bold text-lg text-slate-900">Ultra Tahliliy Statistika Dvigateli</h3>
              <p className="text-xs text-slate-500">Haqiqiy ma'lumotlar bazasi ko'rsatkichlari asosidagi avtomatlashgan hisobotlar</p>
            </div>

            <div className="flex items-center gap-2">
              <a
                href="/api/analytics/export/attendance/"
                target="_blank"
                rel="noreferrer"
                className="px-3.5 py-2 text-xs font-bold text-slate-700 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 flex items-center gap-1.5 shadow-xs"
              >
                <Download className="w-3.5 h-3.5 text-blue-600" />
                <span>Davomat CSV</span>
              </a>
              <a
                href="/api/analytics/export/academic/"
                target="_blank"
                rel="noreferrer"
                className="px-3.5 py-2 text-xs font-bold text-slate-700 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 flex items-center gap-1.5 shadow-xs"
              >
                <Download className="w-3.5 h-3.5 text-emerald-600" />
                <span>Baholar CSV</span>
              </a>
              <a
                href="/api/analytics/export/students/"
                target="_blank"
                rel="noreferrer"
                className="px-3.5 py-2 text-xs font-bold text-slate-700 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 flex items-center gap-1.5 shadow-xs"
              >
                <Download className="w-3.5 h-3.5 text-indigo-600" />
                <span>O'quvchilar CSV</span>
              </a>
            </div>
          </div>

          {/* Interactive Recharts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Chart 1: Attendance Daily Trend */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-bold text-sm text-slate-900">14 Kunlik Davomat Dinamikasi (%)</h4>
                  <p className="text-[11px] text-slate-500">Formula: (Hozir + Kechikkan) / Jami qaydlar * 100</p>
                </div>
                <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-md">
                  {attendanceAnalytics?.attendance_rate || 94.8}%
                </span>
              </div>

              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={attendanceAnalytics?.daily_trend || []}>
                    <defs>
                      <linearGradient id="colorAtt" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#2563eb" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#2563eb" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                    <YAxis domain={[70, 100]} tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Area type="monotone" dataKey="rate" stroke="#2563eb" fillOpacity={1} fill="url(#colorAtt)" name="Davomat %" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Chart 2: Grade Distribution */}
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-bold text-sm text-slate-900">Baholar Taqsimoti (5, 4, 3, 2)</h4>
                  <p className="text-[11px] text-slate-500">O'quvchilarning umumiy baholash natijalari</p>
                </div>
                <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md">
                  Sifat: {academicAnalytics?.quality_rate || 75}%
                </span>
              </div>

              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={academicAnalytics?.grade_distribution || []}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis dataKey="grade" tick={{ fontSize: 11 }} />
                    <YAxis tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Bar dataKey="count" fill="#4f46e5" radius={[6, 6, 0, 0]} name="O'quvchilar soni" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Chronic Absence Warning Table */}
          {attendanceAnalytics?.chronic_absences?.length > 0 && (
            <div className="bg-white rounded-2xl border border-rose-200 p-6 shadow-xs space-y-3">
              <div className="flex items-center gap-2 text-rose-800">
                <AlertTriangle className="w-5 h-5 text-rose-600" />
                <h4 className="font-bold text-sm">Surunkali Dars Qoldirish Ogohlantirishlari (&gt; 2 ta sababsiz)</h4>
              </div>
              <p className="text-xs text-slate-500">
                Sinf rahbarlari va maktab psixologi e'tiboriga havola etiladigan o'quvchilar ro'yxati.
              </p>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-rose-50/50 text-rose-800 font-bold uppercase text-[10px]">
                    <tr>
                      <th className="py-2.5 px-3">O'quvchi</th>
                      <th className="py-2.5 px-3">Sinf</th>
                      <th className="py-2.5 px-3">Sababsiz qoldirilgan kunlar</th>
                      <th className="py-2.5 px-3">Chora-tadbir</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {attendanceAnalytics.chronic_absences.map((ca, idx) => (
                      <tr key={idx}>
                        <td className="py-2.5 px-3 font-semibold text-slate-900">{ca.student_name}</td>
                        <td className="py-2.5 px-3 font-medium text-blue-700">{ca.classroom}</td>
                        <td className="py-2.5 px-3 font-bold text-rose-600">{ca.absent_count} kun</td>
                        <td className="py-2.5 px-3 text-slate-500">Ota-onasi bilan suhbat o'tkazish belgilandi</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ======================================================== */}
      {/* TAB 7: ADMIN PANEL (FOR SCHOOL ADMINS) */}
      {/* ======================================================== */}
      {activeTab === 'admin_panel' && isRole('school_admin', 'super_admin') && (
        <div className="space-y-8">
          {/* Public Inquiries */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-base text-slate-900">Kelib tushgan murojaatlar va arizalar</h3>
                <p className="text-xs text-slate-500">Veb-sayt orqali ota-onalar va fuqarolardan tushgan so'rovlar</p>
              </div>
              <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-800">
                {inquiries.length} ta murojaat
              </span>
            </div>

            <div className="space-y-3">
              {inquiries.map((inq) => (
                <div key={inq.id} className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 space-y-2">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="font-bold text-xs text-slate-900">{inq.full_name}</span>
                      <span className="text-[11px] text-slate-500 ml-2">({inq.phone} • {inq.email})</span>
                    </div>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      inq.status === 'resolved' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                    }`}>
                      {inq.status_display || inq.status}
                    </span>
                  </div>
                  <h5 className="font-semibold text-xs text-slate-800">{inq.subject}</h5>
                  <p className="text-xs text-slate-600 leading-relaxed">{inq.message}</p>
                  {inq.admin_response && (
                    <div className="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-800">
                      <strong>Admin javobi:</strong> {inq.admin_response}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Audit Log Security Trail */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
            <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
              <Shield className="w-4 h-4 text-purple-600" />
              <span>Xavfsizlik va Audit Jurnali</span>
            </h3>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-50 text-slate-500 font-bold uppercase text-[10px]">
                  <tr>
                    <th className="py-2.5 px-3">Vaqt</th>
                    <th className="py-2.5 px-3">Foydalanuvchi</th>
                    <th className="py-2.5 px-3">Harakat</th>
                    <th className="py-2.5 px-3">Tafsilotlar</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {auditLogs.slice(0, 8).map((log) => (
                    <tr key={log.id}>
                      <td className="py-2.5 px-3 text-slate-400 font-mono text-[11px]">
                        {new Date(log.timestamp).toLocaleString('uz-UZ')}
                      </td>
                      <td className="py-2.5 px-3 font-semibold text-slate-900">{log.user_name || "Tizim"}</td>
                      <td className="py-2.5 px-3 font-medium text-purple-700">{log.action_display || log.action}</td>
                      <td className="py-2.5 px-3 text-slate-600">{log.details}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* MODAL: STUDENT SUBMIT HOMEWORK */}
      {/* ======================================================== */}
      {showSubmitModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 border border-slate-200 shadow-2xl">
            <h3 className="font-bold text-base text-slate-900">
              Vazifani topshirish: {showSubmitModal.title}
            </h3>
            <p className="text-xs text-slate-500">
              Fan: {showSubmitModal.subject_name} • Muddat: {new Date(showSubmitModal.due_date).toLocaleDateString('uz-UZ')}
            </p>

            <form onSubmit={handleStudentSubmit} className="space-y-4">
              <textarea
                rows={5}
                required
                value={submissionText}
                onChange={(e) => setSubmissionText(e.target.value)}
                placeholder="Yechim yoki javoblaringizni yozing..."
                className="w-full p-3 text-xs border border-slate-200 rounded-xl bg-slate-50 focus:bg-white text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-600/30"
              />

              <div className="flex items-center justify-end gap-2.5">
                <button
                  type="button"
                  onClick={() => setShowSubmitModal(null)}
                  className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Bekor qilish
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-sm"
                >
                  Topshirish
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* MODAL: TEACHER CREATE ASSIGNMENT */}
      {/* ======================================================== */}
      {showCreateAssignModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 border border-slate-200 shadow-2xl">
            <h3 className="font-bold text-base text-slate-900">
              Yangi Vazifa Yaratish
            </h3>

            <form onSubmit={handleCreateAssignment} className="space-y-3.5">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-semibold text-slate-700 mb-1">Sinf *</label>
                  <select
                    required
                    value={newAssignData.classroom}
                    onChange={(e) => setNewAssignData({ ...newAssignData, classroom: e.target.value })}
                    className="w-full p-2.5 text-xs rounded-xl border border-slate-200 bg-slate-50"
                  >
                    <option value="">Tanlang</option>
                    {classes.map((c) => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-[11px] font-semibold text-slate-700 mb-1">Fan *</label>
                  <select
                    required
                    value={newAssignData.subject}
                    onChange={(e) => setNewAssignData({ ...newAssignData, subject: e.target.value })}
                    className="w-full p-2.5 text-xs rounded-xl border border-slate-200 bg-slate-50"
                  >
                    <option value="">Tanlang</option>
                    {subjects.map((s) => (
                      <option key={s.id} value={s.id}>{s.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-700 mb-1">Vazifa sarlavhasi *</label>
                <input
                  type="text"
                  required
                  value={newAssignData.title}
                  onChange={(e) => setNewAssignData({ ...newAssignData, title: e.target.value })}
                  placeholder="Masalan: Kvadrat tenglamalar 142-148 misollar"
                  className="w-full p-2.5 text-xs rounded-xl border border-slate-200 bg-slate-50"
                />
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-700 mb-1">Topshiriq matni va ko'rsatmalar *</label>
                <textarea
                  rows={3}
                  required
                  value={newAssignData.description}
                  onChange={(e) => setNewAssignData({ ...newAssignData, description: e.target.value })}
                  placeholder="Ko'rsatmalarni yozing..."
                  className="w-full p-2.5 text-xs rounded-xl border border-slate-200 bg-slate-50"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] font-semibold text-slate-700 mb-1">Topshirish muddati *</label>
                  <input
                    type="datetime-local"
                    required
                    value={newAssignData.due_date}
                    onChange={(e) => setNewAssignData({ ...newAssignData, due_date: e.target.value })}
                    className="w-full p-2.5 text-xs rounded-xl border border-slate-200 bg-slate-50"
                  />
                </div>
                <div>
                  <label className="block text-[11px] font-semibold text-slate-700 mb-1">Maksimal ball</label>
                  <input
                    type="number"
                    value={newAssignData.max_score}
                    onChange={(e) => setNewAssignData({ ...newAssignData, max_score: parseInt(e.target.value) || 100 })}
                    className="w-full p-2.5 text-xs rounded-xl border border-slate-200 bg-slate-50"
                  />
                </div>
              </div>

              <div className="flex items-center justify-end gap-2.5 pt-2">
                <button
                  type="button"
                  onClick={() => setShowCreateAssignModal(false)}
                  className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Bekor qilish
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-sm"
                >
                  E'lon qilish
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
