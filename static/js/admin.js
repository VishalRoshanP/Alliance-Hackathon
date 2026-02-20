/* ============================================
   EduGuard - Admin Dashboard Logic
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    if (!Auth.requireAuth(['admin'])) return;

    renderStudentTable();
    renderAttendanceTable();
    renderComplaints();
    renderAlerts();
    renderDashboardAlerts();
    renderExistingDocs();
    initCharts();
    initFileUpload();
    calculateStats();
});

// ── Section Navigation ──
function showAdminSection(el) {
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    el.classList.add('active');
    document.querySelectorAll('.section-content').forEach(s => s.classList.remove('active'));
    const target = el.dataset.target;
    if (target) document.getElementById(target).classList.add('active');
    if (window.innerWidth <= 768) toggleSidebar();
}

// ── Stats ──
function calculateStats() {
    const students = MockData.students;
    const atRisk = students.filter(s => s.risk === 'high' || s.risk === 'critical').length;
    const avgAtt = Math.round(students.reduce((sum, s) => sum + s.attendance, 0) / students.length);
    document.getElementById('at-risk-count').textContent = atRisk;
    document.getElementById('avg-attendance').textContent = avgAtt + '%';
}

// ── Student Table ──
function renderStudentTable(filter = '') {
    const tbody = document.getElementById('student-tbody');
    if (!tbody) return;

    const students = MockData.students.filter(s =>
        s.name.toLowerCase().includes(filter.toLowerCase())
    );

    tbody.innerHTML = students.map(s => {
        const riskClass = s.risk === 'critical' ? 'danger' : s.risk === 'high' ? 'warning' : s.risk === 'medium' ? 'info' : 'success';
        const attClass = s.attendance < 70 ? 'color: var(--accent-rose); font-weight: 700;' : '';
        return `
      <tr>
        <td><strong>${s.name}</strong></td>
        <td>${s.class}</td>
        <td style="${attClass}">${s.attendance}%</td>
        <td>${s.marks}%</td>
        <td><span class="badge-status ${s.fees === 'paid' ? 'success' : s.fees === 'partial' ? 'warning' : 'danger'}">${s.fees}</span></td>
        <td><span class="badge-status ${riskClass}">${s.risk}</span></td>
        <td><button class="btn btn-sm btn-secondary" onclick="viewStudent(${s.id})">View</button></td>
      </tr>
    `;
    }).join('');
}

function filterStudents() {
    const query = document.getElementById('student-search').value;
    renderStudentTable(query);
}

function viewStudent(id) {
    const s = MockData.students.find(st => st.id === id);
    if (!s) return;
    document.getElementById('modal-student-name').textContent = s.name;
    document.getElementById('modal-student-body').innerHTML = `
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
      <div class="stat-card purple" style="margin: 0; padding: 16px;">
        <div class="stat-value" style="font-size: 22px;">${s.attendance}%</div>
        <div class="stat-label">Attendance</div>
      </div>
      <div class="stat-card teal" style="margin: 0; padding: 16px;">
        <div class="stat-value" style="font-size: 22px;">${s.marks}%</div>
        <div class="stat-label">Marks</div>
      </div>
    </div>
    <div style="display: flex; flex-direction: column; gap: 12px;">
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Class</span><span>${s.class}</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Email</span><span>${s.email}</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Phone</span><span>${s.phone}</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Fee Status</span><span class="badge-status ${s.fees === 'paid' ? 'success' : 'danger'}">${s.fees}</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border-subtle);">
        <span style="color: var(--text-muted);">Behavior</span><span>${s.behavior}</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding: 10px 0;">
        <span style="color: var(--text-muted);">Risk Level</span>
        <span class="badge-status ${s.risk === 'critical' ? 'danger' : s.risk === 'high' ? 'warning' : 'success'}">${s.risk}</span>
      </div>
    </div>
    ${s.attendance < 70 ? `
      <div class="alert-banner alert-danger" style="margin-top: 16px;">
        <span class="alert-icon">⚠️</span>
        <span>Attendance below 70%! Immediate intervention recommended.</span>
      </div>
    ` : ''}
  `;
    document.getElementById('student-modal').classList.add('open');
}

// ── Attendance Table ──
function renderAttendanceTable() {
    const tbody = document.getElementById('attendance-tbody');
    if (!tbody) return;

    const sorted = [...MockData.students].sort((a, b) => a.attendance - b.attendance);
    tbody.innerHTML = sorted.map(s => {
        const isLow = s.attendance < 70;
        const barColor = s.attendance >= 80 ? 'green' : s.attendance >= 70 ? 'amber' : 'red';
        return `
      <tr style="${isLow ? 'background: rgba(244, 63, 94, 0.05);' : ''}">
        <td><strong style="${isLow ? 'color: var(--accent-rose);' : ''}">${s.name}</strong></td>
        <td>${s.class}</td>
        <td style="${isLow ? 'color: var(--accent-rose); font-weight: 700;' : ''}">${s.attendance}%</td>
        <td><span class="badge-status ${isLow ? 'danger' : 'success'}">${isLow ? '⚠️ Below 70%' : '✓ OK'}</span></td>
        <td style="min-width: 120px;">
          <div class="progress-bar">
            <div class="progress-fill ${barColor}" style="width: ${s.attendance}%;"></div>
          </div>
        </td>
      </tr>
    `;
    }).join('');
}

// ── Complaints ──
let allComplaints = [...MockData.complaints];

function renderComplaints(filter = 'all') {
    const container = document.getElementById('admin-complaints-list');
    if (!container) return;

    let filtered = allComplaints;
    if (filter === 'high') filtered = allComplaints.filter(c => c.priority === 'high');
    else if (filter === 'pending') filtered = allComplaints.filter(c => c.status === 'pending');
    else if (filter === 'resolved') filtered = allComplaints.filter(c => c.status === 'resolved');

    container.innerHTML = filtered.map(c => {
        const statusClass = c.status === 'resolved' ? 'success' : c.status === 'in-progress' ? 'warning' : 'pending';
        const priorityClass = c.priority === 'high' ? 'danger' : c.priority === 'medium' ? 'warning' : 'info';
        return `
      <div class="complaint-card">
        <div class="complaint-header">
          <h4>${c.title}</h4>
          <div style="display: flex; gap: 8px;">
            <span class="badge-status ${priorityClass}">${c.priority}</span>
            <span class="badge-status ${statusClass}">${c.status}</span>
          </div>
        </div>
        <div class="complaint-body">${c.description}</div>
        <div class="complaint-footer">
          <span>👤 ${c.student} • 📌 ${c.category}</span>
          <div style="display: flex; gap: 8px;">
            ${c.status !== 'resolved' ? `
              <button class="btn btn-sm btn-success" onclick="resolveComplaint(${c.id})">✓ Resolve</button>
            ` : ''}
          </div>
        </div>
      </div>
    `;
    }).join('');
}

function filterComplaints(filter, btn) {
    btn.closest('.section-tabs').querySelectorAll('.section-tab').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    renderComplaints(filter);
}

function resolveComplaint(id) {
    const c = allComplaints.find(comp => comp.id === id);
    if (c) {
        c.status = 'resolved';
        renderComplaints();
        Toast.show('Complaint marked as resolved!', 'success');
    }
}

// ── Alerts ──
function renderAlerts() {
    const container = document.getElementById('alerts-list');
    if (!container) return;

    const lowAttendance = MockData.students.filter(s => s.attendance < 70);

    container.innerHTML = lowAttendance.map(s => `
    <div class="alert-banner alert-danger">
      <span class="alert-icon">🚨</span>
      <span><strong>${s.name}</strong> (${s.class}) has attendance at <strong>${s.attendance}%</strong> — below the 70% threshold. Risk: <strong>${s.risk}</strong>. Immediate intervention recommended.</span>
      <button class="alert-close" onclick="this.parentElement.remove()">✕</button>
    </div>
  `).join('');

    // Critical cases
    const critical = MockData.students.filter(s => s.risk === 'critical');
    container.innerHTML += critical.map(s => `
    <div class="alert-banner alert-warning">
      <span class="alert-icon">⚠️</span>
      <span><strong>${s.name}</strong> is at <strong>CRITICAL</strong> dropout risk. Fees: ${s.fees}, Behavior: ${s.behavior}. Urgent action needed!</span>
      <button class="alert-close" onclick="this.parentElement.remove()">✕</button>
    </div>
  `).join('');
}

function renderDashboardAlerts() {
    const container = document.getElementById('dashboard-alerts');
    if (!container) return;

    const lowAtt = MockData.students.filter(s => s.attendance < 70);
    if (lowAtt.length > 0) {
        container.innerHTML = `
      <div class="alert-banner alert-danger animate-fade-in-up delay-5">
        <span class="alert-icon">🚨</span>
        <span><strong>${lowAtt.length} students</strong> have attendance below 70%! Review alerts section for details.</span>
        <button class="alert-close" onclick="this.parentElement.remove()">✕</button>
      </div>
    `;
    }
}

// ── File Upload ──
function initFileUpload() {
    const area = document.getElementById('upload-area');
    const input = document.getElementById('file-input');
    if (!area || !input) return;

    area.addEventListener('dragover', (e) => {
        e.preventDefault();
        area.style.borderColor = 'var(--primary-500)';
        area.style.background = 'rgba(124, 58, 237, 0.05)';
    });

    area.addEventListener('dragleave', () => {
        area.style.borderColor = '';
        area.style.background = '';
    });

    area.addEventListener('drop', (e) => {
        e.preventDefault();
        area.style.borderColor = '';
        area.style.background = '';
        handleFiles(e.dataTransfer.files);
    });

    input.addEventListener('change', () => handleFiles(input.files));
}

function handleFiles(files) {
    const container = document.getElementById('uploaded-files');
    Array.from(files).forEach(file => {
        const item = document.createElement('div');
        item.className = 'file-item';
        item.style.animation = 'fadeInUp 0.3s ease';
        item.innerHTML = `
      <span class="file-icon">${file.type.includes('pdf') ? '📄' : '📝'}</span>
      <div class="file-info">
        <div class="file-name">${file.name}</div>
        <div class="file-size">${(file.size / 1024).toFixed(1)} KB • Just now</div>
      </div>
      <button class="btn btn-sm btn-danger" onclick="this.parentElement.remove()">✕</button>
    `;
        container.appendChild(item);
    });
    Toast.show(`${files.length} file(s) uploaded successfully!`, 'success');
}

function renderExistingDocs() {
    const container = document.getElementById('existing-docs');
    if (!container) return;

    container.innerHTML = MockData.documents.map(doc => `
    <div class="file-item">
      <span class="file-icon">${doc.type === 'PDF' ? '📄' : '📝'}</span>
      <div class="file-info">
        <div class="file-name">${doc.name}</div>
        <div class="file-size">${doc.size} • ${formatDate(doc.date)}</div>
      </div>
      <button class="btn btn-sm btn-danger" onclick="this.parentElement.remove(); Toast.show('Document removed', 'info')">🗑️</button>
    </div>
  `).join('');
}

// ── Charts ──
function initCharts() {
    setTimeout(() => {
        Charts.barChart('admin-attendance-chart',
            MockData.students.map(s => s.name.split(' ')[0]),
            MockData.students.map(s => s.attendance),
            MockData.students.map(s => s.attendance < 70 ? Charts.colors.rose : Charts.colors.purple)
        );

        Charts.donutChart('risk-chart',
            ['Low', 'Medium', 'High', 'Critical'],
            [
                MockData.students.filter(s => s.risk === 'low').length,
                MockData.students.filter(s => s.risk === 'medium').length,
                MockData.students.filter(s => s.risk === 'high').length,
                MockData.students.filter(s => s.risk === 'critical').length,
            ],
            [Charts.colors.emerald, Charts.colors.amber, Charts.colors.coral, Charts.colors.rose]
        );
    }, 300);
}

window.addEventListener('resize', () => {
    clearTimeout(window._resizeTimer);
    window._resizeTimer = setTimeout(initCharts, 250);
});
