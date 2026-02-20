/* ============================================
   EduGuard - Government/NGO Dashboard Logic
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    if (!Auth.requireAuth(['gov'])) return;

    renderAuthorities();
    renderStudents();
    renderSchemes();
    renderReports();
    renderGovAlerts();
    initCharts();
    initSchemeForm();
});

// ── Section Navigation ──
function showGovSection(el) {
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    el.classList.add('active');
    document.querySelectorAll('.section-content').forEach(s => s.classList.remove('active'));
    const target = el.dataset.target;
    if (target) document.getElementById(target).classList.add('active');
    if (window.innerWidth <= 768) toggleSidebar();
}

// ── Authorities ──
function renderAuthorities() {
    const tbody = document.getElementById('authorities-tbody');
    if (!tbody) return;

    tbody.innerHTML = MockData.authorities.map(a => `
    <tr>
      <td><strong>${a.name}</strong></td>
      <td>${a.institution}</td>
      <td>${a.role}</td>
      <td>${a.students}</td>
      <td>${a.email}</td>
      <td>${a.phone}</td>
    </tr>
  `).join('');
}

// ── Students ──
function renderStudents(filter = 'all') {
    const tbody = document.getElementById('gov-students-tbody');
    if (!tbody) return;

    let students = MockData.students;
    if (filter === 'critical') students = students.filter(s => s.risk === 'critical');
    else if (filter === 'high') students = students.filter(s => s.risk === 'high');
    else if (filter === 'low') students = students.filter(s => s.risk === 'low');

    tbody.innerHTML = students.map(s => {
        const riskClass = s.risk === 'critical' ? 'danger' : s.risk === 'high' ? 'warning' : s.risk === 'medium' ? 'info' : 'success';
        return `
      <tr style="${s.risk === 'critical' ? 'background: rgba(244, 63, 94, 0.05);' : ''}">
        <td><strong>${s.name}</strong></td>
        <td>${s.class}</td>
        <td style="${s.attendance < 70 ? 'color: var(--accent-rose); font-weight: 700;' : ''}">${s.attendance}%</td>
        <td>${s.marks}%</td>
        <td><span class="badge-status ${s.fees === 'paid' ? 'success' : s.fees === 'partial' ? 'warning' : 'danger'}">${s.fees}</span></td>
        <td><span class="badge-status ${riskClass}">${s.risk}</span></td>
        <td>${s.behavior}</td>
      </tr>
    `;
    }).join('');
}

function filterGovStudents(filter, btn) {
    btn.closest('.section-tabs').querySelectorAll('.section-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    renderStudents(filter);
}

// ── Schemes ──
let govSchemes = [...MockData.schemes];

function renderSchemes() {
    const container = document.getElementById('gov-schemes-list');
    if (!container) return;

    container.innerHTML = govSchemes.map(scheme => `
    <div class="scheme-card">
      <span class="scheme-tag">${scheme.category}</span>
      <h4>${scheme.name}</h4>
      <p>${scheme.description}</p>
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 12px;">
        <span style="color: var(--accent-emerald); font-weight: 600;">${scheme.amount}</span>
        <span style="color: var(--text-muted); font-size: 12px;">Deadline: ${scheme.deadline}</span>
      </div>
      <div style="display: flex; gap: 8px;">
        <button class="btn btn-sm btn-secondary" style="flex: 1;" onclick="Toast.show('Broadcasted to all authorities!', 'success')">📢 Broadcast</button>
        <button class="btn btn-sm btn-danger" onclick="removeScheme(${scheme.id})">🗑️</button>
      </div>
    </div>
  `).join('');
}

function removeScheme(id) {
    govSchemes = govSchemes.filter(s => s.id !== id);
    renderSchemes();
    Toast.show('Scheme removed', 'info');
}

function openSchemeModal() {
    document.getElementById('scheme-modal').classList.add('open');
}

function closeSchemeModal() {
    document.getElementById('scheme-modal').classList.remove('open');
}

function initSchemeForm() {
    const form = document.getElementById('scheme-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('scheme-name').value;
        const desc = document.getElementById('scheme-desc').value;
        const amount = document.getElementById('scheme-amount').value;
        const category = document.getElementById('scheme-category').value;
        const deadline = document.getElementById('scheme-deadline').value;
        const eligibility = document.getElementById('scheme-eligibility').value;

        if (!name || !desc) {
            Toast.show('Please fill in scheme name and description', 'warning');
            return;
        }

        govSchemes.push({
            id: Date.now(),
            name,
            description: desc,
            amount: amount || 'TBD',
            category,
            deadline: deadline ? formatDate(deadline) : 'TBD',
            eligibility: eligibility || 'All eligible students'
        });

        renderSchemes();
        closeSchemeModal();
        form.reset();
        Toast.show('New scheme published & broadcasted to all authorities!', 'success');
    });
}

// ── Reports ──
function renderReports() {
    const tbody = document.getElementById('report-tbody');
    if (!tbody) return;

    const atRisk = MockData.students.filter(s => s.risk === 'high' || s.risk === 'critical');
    const institutions = ['Delhi Public School', 'Govt. Girls High School', 'St. Mary\'s Convent', 'Kendriya Vidyalaya'];

    tbody.innerHTML = atRisk.map(s => {
        const inst = institutions[Math.floor(Math.random() * institutions.length)];
        const recommendation = s.risk === 'critical'
            ? 'Immediate intervention: financial aid + counseling'
            : 'Monitor closely; connect with scholarship programs';
        return `
      <tr style="${s.risk === 'critical' ? 'background: rgba(244, 63, 94, 0.05);' : ''}">
        <td><strong>${s.name}</strong></td>
        <td>${inst}</td>
        <td><span class="badge-status ${s.risk === 'critical' ? 'danger' : 'warning'}">${s.risk}</span></td>
        <td style="${s.attendance < 70 ? 'color: var(--accent-rose); font-weight: 700;' : ''}">${s.attendance}%</td>
        <td>${s.marks}%</td>
        <td><span class="badge-status ${s.fees === 'paid' ? 'success' : 'danger'}">${s.fees}</span></td>
        <td style="font-size: 12px; color: var(--text-secondary);">${recommendation}</td>
      </tr>
    `;
    }).join('');
}

// ── Gov Alerts ──
function renderGovAlerts() {
    const container = document.getElementById('gov-alerts');
    if (!container) return;

    const critical = MockData.students.filter(s => s.risk === 'critical');
    container.innerHTML = critical.map(s => `
    <div class="alert-banner alert-danger">
      <span class="alert-icon">🚨</span>
      <span><strong>${s.name}</strong> (${s.class}) — CRITICAL dropout risk. Attendance: ${s.attendance}%, Marks: ${s.marks}%, Fees: ${s.fees}. Requires immediate multi-stakeholder intervention.</span>
    </div>
  `).join('');

    if (critical.length === 0) {
        container.innerHTML = `
      <div class="alert-banner alert-success">
        <span class="alert-icon">✅</span>
        <span>No critical dropout risks detected across institutions.</span>
      </div>
    `;
    }
}

// ── Charts ──
function initCharts() {
    setTimeout(() => {
        Charts.barChart('institution-chart',
            MockData.authorities.map(a => a.institution.split(' ')[0]),
            MockData.authorities.map(a => a.students),
            [Charts.colors.purple, Charts.colors.teal, Charts.colors.sky, Charts.colors.amber]
        );

        Charts.donutChart('gov-risk-chart',
            ['Low', 'Medium', 'High', 'Critical'],
            [
                MockData.students.filter(s => s.risk === 'low').length,
                MockData.students.filter(s => s.risk === 'medium').length,
                MockData.students.filter(s => s.risk === 'high').length,
                MockData.students.filter(s => s.risk === 'critical').length,
            ],
            [Charts.colors.emerald, Charts.colors.amber, Charts.colors.coral, Charts.colors.rose]
        );

        Charts.lineChart('trend-chart',
            ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'],
            [
                { data: [78, 80, 77, 82, 85, 83, 81], color: Charts.colors.purple, label: 'Avg Attendance' },
                { data: [70, 70, 70, 70, 70, 70, 70], color: Charts.colors.rose, label: 'Threshold' }
            ]
        );

        Charts.barChart('scheme-util-chart',
            ['BBBP', 'CBSE', 'NSP', 'Pragati', 'SSY', 'KGBV'],
            [142, 68, 95, 34, 210, 87],
            [Charts.colors.purple, Charts.colors.teal, Charts.colors.sky, Charts.colors.amber, Charts.colors.coral, Charts.colors.emerald]
        );
    }, 300);
}

window.addEventListener('resize', () => {
    clearTimeout(window._resizeTimer);
    window._resizeTimer = setTimeout(initCharts, 250);
});
