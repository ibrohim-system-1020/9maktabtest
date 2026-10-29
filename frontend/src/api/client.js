// API Client for 9-Maktab Smart School Management Platform

const API_BASE = '/api';

export async function apiFetch(endpoint, options = {}) {
  const token = localStorage.getItem('access_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...(options.headers || {}),
  };

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    if (token && !endpoint.includes('/token/')) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_info');
      window.dispatchEvent(new Event('auth_logout'));
    }
  }

  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    const data = await response.json();
    if (!response.ok) {
      let errorMsg = data.detail || data.error;
      if (!errorMsg && typeof data === 'object') {
        const firstKey = Object.keys(data)[0];
        const val = data[firstKey];
        errorMsg = Array.isArray(val) ? `${firstKey}: ${val[0]}` : JSON.stringify(val);
      }
      throw new Error(errorMsg || `Xatolik yuz berdi (${response.status})`);
    }
    return data;
  }

  if (!response.ok) {
    throw new Error(`Xatolik yuz berdi (${response.status})`);
  }

  return response;
}

export const api = {
  // Auth & Registration
  login: async (username, password) => {
    const res = await apiFetch('/auth/token/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    localStorage.setItem('access_token', res.access);
    localStorage.setItem('refresh_token', res.refresh);
    localStorage.setItem('user_info', JSON.stringify(res.user));
    return res;
  },

  register: async (registrationData) => {
    const res = await apiFetch('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(registrationData),
    });
    if (res.access) {
      localStorage.setItem('access_token', res.access);
      localStorage.setItem('refresh_token', res.refresh);
      localStorage.setItem('user_info', JSON.stringify(res.user));
    }
    return res;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_info');
    window.dispatchEvent(new Event('auth_logout'));
  },

  getMe: () => apiFetch('/auth/me/'),
  changePassword: (data) => apiFetch('/auth/change-password/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  // User Management (Admin)
  getUsers: (params = '') => apiFetch(`/auth/users/${params}`),
  toggleUserActive: (id) => apiFetch(`/auth/users/${id}/toggle_active/`, { method: 'POST' }),
  resetUserPassword: (id, new_password) => apiFetch(`/auth/users/${id}/reset_password/`, {
    method: 'POST',
    body: JSON.stringify({ new_password }),
  }),

  // Portal & Website
  getSchoolInfo: () => apiFetch('/portal/info/'),
  getAnnouncements: (params = '') => apiFetch(`/portal/announcements/${params}`),
  getEvents: () => apiFetch('/portal/events/'),
  getAchievements: () => apiFetch('/portal/achievements/'),
  getFAQs: () => apiFetch('/portal/faq/'),
  getResources: (params = '') => apiFetch(`/resources/resources/${params}`),
  trackDownload: (id) => apiFetch(`/resources/resources/${id}/track_download/`, { method: 'POST' }),
  submitInquiry: (data) => apiFetch('/portal/inquiries/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  getInquiries: () => apiFetch('/portal/inquiries/'),
  respondInquiry: (id, data) => apiFetch(`/portal/inquiries/${id}/respond/`, {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  // Academics
  getClassrooms: () => apiFetch('/academics/classrooms/'),
  getSubjects: () => apiFetch('/academics/subjects/'),
  getStudents: (params = '') => apiFetch(`/academics/students/${params}`),
  
  // Teachers Module
  getTeachers: (params = '') => apiFetch(`/academics/teachers/${params}`),
  createTeacher: (data) => apiFetch('/academics/teachers/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  updateTeacher: (id, data) => apiFetch(`/academics/teachers/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  toggleTeacherActive: (id) => apiFetch(`/academics/teachers/${id}/toggle_active/`, {
    method: 'POST',
  }),
  assignTeacherClass: (id, data) => apiFetch(`/academics/teachers/${id}/assign_class/`, {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  getMyClasses: () => apiFetch('/academics/teachers/my_classes/'),
  getMyChildren: () => apiFetch('/academics/guardians/my_children/'),

  // Timetables
  getTimetable: (params = '') => apiFetch(`/timetables/entries/${params}`),

  // Attendance
  getAttendanceSessions: (params = '') => apiFetch(`/attendance/sessions/${params}`),
  getAttendanceRecords: (params = '') => apiFetch(`/attendance/records/${params}`),
  saveBulkAttendance: (data) => apiFetch('/attendance/sessions/save_bulk/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  // Assignments
  getAssignments: (params = '') => apiFetch(`/assignments/assignments/${params}`),
  createAssignment: (data) => apiFetch('/assignments/assignments/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  submitAssignment: (data) => apiFetch('/assignments/submissions/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  gradeSubmission: (id, data) => apiFetch(`/assignments/submissions/${id}/grade/`, {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  // Assessments
  getAssessments: (params = '') => apiFetch(`/assessments/assessments/${params}`),
  getAssessmentResults: (params = '') => apiFetch(`/assessments/results/${params}`),
  saveBulkAssessmentResults: (data) => apiFetch('/assessments/assessments/save_bulk_results/', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  // Analytics & Exports
  getSchoolOverview: () => apiFetch('/analytics/overview/'),
  getAttendanceAnalytics: (params = '') => apiFetch(`/analytics/attendance/${params}`),
  getAcademicAnalytics: (params = '') => apiFetch(`/analytics/academic/${params}`),
  getTeacherAnalytics: () => apiFetch('/analytics/teachers/'),
  getEngagementAnalytics: () => apiFetch('/analytics/engagement/'),

  // Audit Logs
  getAuditLogs: () => apiFetch('/audit/logs/'),

  // Export URLs
  getExportUrl: (type, params = '') => `/api/analytics/export/${type}/${params ? '?' + params : ''}`,
};
