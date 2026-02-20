/* ============================================
   EduGuard - Shared Utilities
   ============================================ */

// ── Toast Notification System ──
const Toast = {
  container: null,

  init() {
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    }
  },

  show(message, type = 'info', duration = 4000) {
    this.init();
    const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
      <span class="toast-icon">${icons[type]}</span>
      <span class="toast-message">${message}</span>
      <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
    `;
    this.container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }
};

// ── Simple Canvas Charts ──
const Charts = {
  colors: {
    purple: '#7c3aed',
    coral: '#ff6b6b',
    teal: '#2dd4bf',
    amber: '#f59e0b',
    sky: '#38bdf8',
    emerald: '#10b981',
    rose: '#f43f5e',
    lavender: '#c49bff'
  },

  barChart(canvasId, labels, data, barColors) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = rect.height + 'px';
    ctx.scale(dpr, dpr);

    const w = rect.width, h = rect.height;
    const padding = { top: 20, right: 20, bottom: 40, left: 50 };
    const chartW = w - padding.left - padding.right;
    const chartH = h - padding.top - padding.bottom;
    const max = Math.max(...data) * 1.15;
    const barWidth = (chartW / labels.length) * 0.55;
    const gap = chartW / labels.length;

    ctx.clearRect(0, 0, w, h);

    // Grid lines
    for (let i = 0; i <= 4; i++) {
      const y = padding.top + (chartH / 4) * i;
      ctx.strokeStyle = 'rgba(255,255,255,0.06)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(w - padding.right, y);
      ctx.stroke();

      ctx.fillStyle = '#71717a';
      ctx.font = '11px Inter';
      ctx.textAlign = 'right';
      ctx.fillText(Math.round(max - (max / 4) * i), padding.left - 8, y + 4);
    }

    // Bars
    labels.forEach((label, i) => {
      const x = padding.left + gap * i + (gap - barWidth) / 2;
      const barH = (data[i] / max) * chartH;
      const y = padding.top + chartH - barH;
      const color = barColors ? barColors[i % barColors.length] : this.colors.purple;

      const grad = ctx.createLinearGradient(x, y, x, y + barH);
      grad.addColorStop(0, color);
      grad.addColorStop(1, color + '66');
      ctx.fillStyle = grad;

      this.roundRect(ctx, x, y, barWidth, barH, 6);
      ctx.fill();

      // Label
      ctx.fillStyle = '#a1a1aa';
      ctx.font = '11px Inter';
      ctx.textAlign = 'center';
      ctx.fillText(label, x + barWidth / 2, h - padding.bottom + 20);
    });
  },

  lineChart(canvasId, labels, datasets) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = rect.height + 'px';
    ctx.scale(dpr, dpr);

    const w = rect.width, h = rect.height;
    const padding = { top: 20, right: 20, bottom: 40, left: 50 };
    const chartW = w - padding.left - padding.right;
    const chartH = h - padding.top - padding.bottom;

    const allData = datasets.flatMap(d => d.data);
    const max = Math.max(...allData) * 1.15;

    ctx.clearRect(0, 0, w, h);

    // Grid
    for (let i = 0; i <= 4; i++) {
      const y = padding.top + (chartH / 4) * i;
      ctx.strokeStyle = 'rgba(255,255,255,0.06)';
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(w - padding.right, y);
      ctx.stroke();

      ctx.fillStyle = '#71717a';
      ctx.font = '11px Inter';
      ctx.textAlign = 'right';
      ctx.fillText(Math.round(max - (max / 4) * i), padding.left - 8, y + 4);
    }

    // X labels
    labels.forEach((label, i) => {
      const x = padding.left + (chartW / (labels.length - 1)) * i;
      ctx.fillStyle = '#a1a1aa';
      ctx.font = '11px Inter';
      ctx.textAlign = 'center';
      ctx.fillText(label, x, h - padding.bottom + 20);
    });

    // Lines
    datasets.forEach(dataset => {
      ctx.beginPath();
      ctx.strokeStyle = dataset.color;
      ctx.lineWidth = 2.5;
      ctx.lineJoin = 'round';

      dataset.data.forEach((val, i) => {
        const x = padding.left + (chartW / (labels.length - 1)) * i;
        const y = padding.top + chartH - (val / max) * chartH;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.stroke();

      // Area fill
      const lastX = padding.left + chartW;
      ctx.lineTo(lastX, padding.top + chartH);
      ctx.lineTo(padding.left, padding.top + chartH);
      ctx.closePath();
      ctx.fillStyle = dataset.color + '15';
      ctx.fill();

      // Points
      dataset.data.forEach((val, i) => {
        const x = padding.left + (chartW / (labels.length - 1)) * i;
        const y = padding.top + chartH - (val / max) * chartH;
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fillStyle = dataset.color;
        ctx.fill();
        ctx.beginPath();
        ctx.arc(x, y, 2, 0, Math.PI * 2);
        ctx.fillStyle = '#0f0a1a';
        ctx.fill();
      });
    });
  },

  donutChart(canvasId, labels, data, colors) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = rect.height + 'px';
    ctx.scale(dpr, dpr);

    const w = rect.width, h = rect.height;
    const cx = w / 2, cy = h / 2 - 10;
    const radius = Math.min(w, h) / 2 - 30;
    const total = data.reduce((a, b) => a + b, 0);
    let startAngle = -Math.PI / 2;

    ctx.clearRect(0, 0, w, h);

    data.forEach((val, i) => {
      const sliceAngle = (val / total) * Math.PI * 2;
      ctx.beginPath();
      ctx.arc(cx, cy, radius, startAngle, startAngle + sliceAngle);
      ctx.arc(cx, cy, radius * 0.6, startAngle + sliceAngle, startAngle, true);
      ctx.closePath();
      ctx.fillStyle = colors[i % colors.length];
      ctx.fill();
      startAngle += sliceAngle;
    });

    // Center text
    ctx.fillStyle = '#f4f4f5';
    ctx.font = 'bold 24px Outfit';
    ctx.textAlign = 'center';
    ctx.fillText(total, cx, cy + 4);
    ctx.fillStyle = '#71717a';
    ctx.font = '11px Inter';
    ctx.fillText('Total', cx, cy + 20);

    // Legend
    const legendY = cy + radius + 30;
    const legendWidth = labels.length * 90;
    let lx = cx - legendWidth / 2;
    labels.forEach((label, i) => {
      ctx.fillStyle = colors[i % colors.length];
      ctx.fillRect(lx, legendY, 10, 10);
      ctx.fillStyle = '#a1a1aa';
      ctx.font = '11px Inter';
      ctx.textAlign = 'left';
      ctx.fillText(label, lx + 14, legendY + 9);
      lx += 90;
    });
  },

  roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h);
    ctx.lineTo(x, y + h);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }
};

// ── Form Validation ──
const Validator = {
  email(val) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
  },
  phone(val) {
    return /^[0-9]{10}$/.test(val.replace(/[\s\-\+]/g, ''));
  },
  required(val) {
    return val && val.trim().length > 0;
  },
  minLength(val, len) {
    return val && val.length >= len;
  },
  match(val1, val2) {
    return val1 === val2;
  },
  showError(input, msg) {
    const group = input.closest('.form-group');
    if (group) {
      group.classList.add('error');
      let errEl = group.querySelector('.error-msg');
      if (!errEl) {
        errEl = document.createElement('div');
        errEl.className = 'error-msg';
        group.appendChild(errEl);
      }
      errEl.textContent = msg;
      errEl.style.display = 'block';
    }
  },
  clearError(input) {
    const group = input.closest('.form-group');
    if (group) {
      group.classList.remove('error');
      const errEl = group.querySelector('.error-msg');
      if (errEl) errEl.style.display = 'none';
    }
  },
  clearAll(form) {
    form.querySelectorAll('.form-group').forEach(g => {
      g.classList.remove('error');
      const e = g.querySelector('.error-msg');
      if (e) e.style.display = 'none';
    });
  }
};

// ── Auth Helpers ──
const Auth = {
  setToken(token, role, userData) {
    localStorage.setItem('eduguard_token', token);
    localStorage.setItem('eduguard_role', role);
    localStorage.setItem('eduguard_user', JSON.stringify(userData));
  },
  getToken() {
    return localStorage.getItem('eduguard_token');
  },
  getRole() {
    return localStorage.getItem('eduguard_role');
  },
  getUser() {
    try { return JSON.parse(localStorage.getItem('eduguard_user')); }
    catch { return null; }
  },
  logout() {
    localStorage.removeItem('eduguard_token');
    localStorage.removeItem('eduguard_role');
    localStorage.removeItem('eduguard_user');
    window.location.href = 'index.html';
  },
  isLoggedIn() {
    return !!this.getToken();
  },
  requireAuth(allowedRoles) {
    if (!this.isLoggedIn()) {
      window.location.href = 'index.html';
      return false;
    }
    if (allowedRoles && !allowedRoles.includes(this.getRole())) {
      window.location.href = 'index.html';
      return false;
    }
    return true;
  },
  generateToken() {
    return 'eyJ' + btoa(Math.random().toString(36).substring(2) + Date.now());
  }
};

// ── Date/Time ──
function formatTime(date) {
  return new Date(date).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function timeAgo(date) {
  const secs = Math.floor((Date.now() - new Date(date)) / 1000);
  if (secs < 60) return 'just now';
  if (secs < 3600) return Math.floor(secs / 60) + 'm ago';
  if (secs < 86400) return Math.floor(secs / 3600) + 'h ago';
  return Math.floor(secs / 86400) + 'd ago';
}

// ── Sidebar Toggle (mobile) ──
function toggleSidebar() {
  document.querySelector('.sidebar')?.classList.toggle('open');
  document.querySelector('.sidebar-overlay')?.classList.toggle('open');
}

// ── Section Tabs ──
function initSectionTabs() {
  document.querySelectorAll('.section-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const parent = tab.closest('.content-card') || document;
      parent.querySelectorAll('.section-tab').forEach(t => t.classList.remove('active'));
      parent.querySelectorAll('.section-content').forEach(s => s.classList.remove('active'));
      tab.classList.add('active');
      const target = document.getElementById(tab.dataset.target);
      if (target) target.classList.add('active');
    });
  });
}

// Close sidebar on overlay click
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('sidebar-overlay')) {
    toggleSidebar();
  }
});

// ── Mock Data ──
const MockData = {
  students: [
    { id: 1, name: 'Priya Sharma', class: '10th', email: 'priya@edu.in', phone: '9876543210', attendance: 82, marks: 76, risk: 'low', fees: 'paid', behavior: 'good', complaints: 1 },
    { id: 2, name: 'Ananya Patel', class: '9th', email: 'ananya@edu.in', phone: '9876543211', attendance: 65, marks: 58, risk: 'high', fees: 'partial', behavior: 'concerning', complaints: 3 },
    { id: 3, name: 'Kavya Reddy', class: '11th', email: 'kavya@edu.in', phone: '9876543212', attendance: 91, marks: 88, risk: 'low', fees: 'paid', behavior: 'excellent', complaints: 0 },
    { id: 4, name: 'Meera Nair', class: '10th', email: 'meera@edu.in', phone: '9876543213', attendance: 55, marks: 42, risk: 'critical', fees: 'unpaid', behavior: 'at-risk', complaints: 5 },
    { id: 5, name: 'Riya Gupta', class: '12th', email: 'riya@edu.in', phone: '9876543214', attendance: 78, marks: 71, risk: 'medium', fees: 'paid', behavior: 'good', complaints: 2 },
    { id: 6, name: 'Sneha Das', class: '8th', email: 'sneha@edu.in', phone: '9876543215', attendance: 45, marks: 35, risk: 'critical', fees: 'unpaid', behavior: 'at-risk', complaints: 4 },
    { id: 7, name: 'Aisha Khan', class: '11th', email: 'aisha@edu.in', phone: '9876543216', attendance: 88, marks: 82, risk: 'low', fees: 'paid', behavior: 'excellent', complaints: 0 },
    { id: 8, name: 'Divya Joshi', class: '9th', email: 'divya@edu.in', phone: '9876543217', attendance: 69, marks: 55, risk: 'high', fees: 'partial', behavior: 'concerning', complaints: 2 }
  ],

  schemes: [
    { id: 1, name: 'Beti Bachao Beti Padhao', category: 'Government', description: 'Financial aid for girl students to continue education. Covers tuition fees and study materials.', eligibility: 'Girls in classes 8-12 from low-income families', amount: '₹12,000/year', deadline: 'Mar 31, 2026' },
    { id: 2, name: 'CBSE Merit Scholarship', category: 'Academic', description: 'Merit-based scholarship for students scoring above 80% in board exams.', eligibility: 'Students with 80%+ marks', amount: '₹25,000', deadline: 'Apr 15, 2026' },
    { id: 3, name: 'NSP Post-Matric Scholarship', category: 'Government', description: 'National Scholarship Portal scheme for post-matric girl students from minority communities.', eligibility: 'Minority community girl students', amount: '₹15,000/year', deadline: 'May 30, 2026' },
    { id: 4, name: 'Pragati Scholarship (AICTE)', category: 'Technical', description: 'For girl students pursuing technical education in AICTE institutions.', eligibility: 'Girls in AICTE colleges, family income < 8L/year', amount: '₹50,000/year', deadline: 'Jun 10, 2026' },
    { id: 5, name: 'Sukanya Samriddhi Yojana', category: 'Savings', description: 'Government savings scheme for girl children with attractive interest rates.', eligibility: 'Girls below 10 years', amount: 'Varies', deadline: 'Ongoing' },
    { id: 6, name: 'Kasturba Gandhi Balika Vidyalaya', category: 'Government', description: 'Free residential schooling for girls from disadvantaged groups.', eligibility: 'SC/ST/OBC/Minority girls in rural areas', amount: 'Full boarding + education', deadline: 'Ongoing' }
  ],

  complaints: [
    { id: 1, student: 'Priya Sharma', title: 'Library access issue', category: 'Academic', priority: 'medium', status: 'pending', date: '2026-02-18', description: 'Unable to access library after 5 PM during exam season.' },
    { id: 2, student: 'Ananya Patel', title: 'Bullying incident', category: 'Harassment', priority: 'high', status: 'in-progress', date: '2026-02-17', description: 'Facing verbal harassment from senior students near hostel area.' },
    { id: 3, student: 'Meera Nair', title: 'Fee payment difficulty', category: 'General', priority: 'high', status: 'pending', date: '2026-02-19', description: 'Parents unable to pay fees due to financial crisis. Request waiver consideration.' },
    { id: 4, student: 'Riya Gupta', title: 'Hostel water issue', category: 'Hostel', priority: 'medium', status: 'resolved', date: '2026-02-15', description: 'No hot water supply in hostel for past 3 days.' },
    { id: 5, student: 'Sneha Das', title: 'Transport safety concern', category: 'General', priority: 'high', status: 'pending', date: '2026-02-20', description: 'School bus route has become unsafe due to construction work.' }
  ],

  authorities: [
    { id: 1, name: 'Dr. Sunita Verma', institution: 'Delhi Public School', role: 'Principal', students: 342, email: 'sunita@dps.edu', phone: '9988776611' },
    { id: 2, name: 'Mr. Rajesh Kumar', institution: 'Govt. Girls High School', role: 'Headmaster', students: 518, email: 'rajesh@gghs.edu', phone: '9988776622' },
    { id: 3, name: 'Ms. Fatima Begum', institution: 'St. Mary\'s Convent', role: 'Vice Principal', students: 275, email: 'fatima@stmary.edu', phone: '9988776633' },
    { id: 4, name: 'Dr. Lakshmi Iyer', institution: 'Kendriya Vidyalaya', role: 'Principal', students: 450, email: 'lakshmi@kv.edu', phone: '9988776644' }
  ],

  documents: [
    { id: 1, name: 'Annual Exam Schedule 2026', type: 'PDF', size: '245 KB', date: '2026-02-10', uploadedBy: 'Dr. Sunita Verma' },
    { id: 2, name: 'Fee Structure Update', type: 'PDF', size: '128 KB', date: '2026-02-12', uploadedBy: 'Mr. Rajesh Kumar' },
    { id: 3, name: 'Holiday Calendar', type: 'PDF', size: '89 KB', date: '2026-02-05', uploadedBy: 'Ms. Fatima Begum' },
    { id: 4, name: 'Science Fair Guidelines', type: 'DOCX', size: '312 KB', date: '2026-02-18', uploadedBy: 'Dr. Lakshmi Iyer' }
  ]
};
