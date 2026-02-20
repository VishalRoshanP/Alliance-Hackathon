/* ============================================
   EduGuard - Student Dashboard Logic
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    // Auth check
    if (!Auth.requireAuth(['student'])) return;

    const user = Auth.getUser();
    if (user) {
        document.getElementById('student-name').textContent = user.name?.split(' ')[0] || 'Student';
    }

    renderSchemes();
    renderComplaints();
    renderDocuments();
    initCharts();
    initComplaintForm();
    Chatbot.init();
});

// ── Section Navigation ──
function showSection(el) {
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    el.classList.add('active');
    document.querySelectorAll('.section-content').forEach(s => s.classList.remove('active'));
    const target = el.dataset.target;
    if (target) {
        document.getElementById(target).classList.add('active');
    }
    // Close mobile sidebar
    if (window.innerWidth <= 768) toggleSidebar();
}

// ── Charts ──
function initCharts() {
    setTimeout(() => {
        Charts.lineChart('attendance-chart',
            ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'],
            [
                { data: [72, 78, 75, 80, 85, 79, 82], color: Charts.colors.purple, label: 'Attendance' },
                { data: [70, 70, 70, 70, 70, 70, 70], color: Charts.colors.rose, label: 'Minimum' }
            ]
        );

        Charts.barChart('marks-chart',
            ['Math', 'Science', 'English', 'Hindi', 'Social', 'Computer'],
            [85, 72, 88, 65, 74, 92],
            [Charts.colors.purple, Charts.colors.teal, Charts.colors.sky, Charts.colors.amber, Charts.colors.coral, Charts.colors.emerald]
        );
    }, 300);
}

// ── Schemes ──
function renderSchemes() {
    const container = document.getElementById('schemes-list');
    if (!container) return;

    container.innerHTML = MockData.schemes.map(scheme => `
    <div class="scheme-card">
      <span class="scheme-tag">${scheme.category}</span>
      <h4>${scheme.name}</h4>
      <p>${scheme.description}</p>
      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <span style="color: var(--accent-emerald); font-weight: 600; font-size: 14px;">${scheme.amount}</span>
        <span style="color: var(--text-muted); font-size: 12px;">Deadline: ${scheme.deadline}</span>
      </div>
      <button class="btn btn-sm btn-secondary" style="margin-top: 12px; width: 100%;" onclick="Toast.show('Application link coming soon!', 'info')">
        Apply Now →
      </button>
    </div>
  `).join('');
}

// ── Complaints ──
function renderComplaints() {
    const container = document.getElementById('student-complaints-list');
    if (!container) return;

    const studentComplaints = MockData.complaints.filter(c => c.student === 'Priya Sharma');

    if (studentComplaints.length === 0) {
        container.innerHTML = `<p style="color: var(--text-muted); text-align: center; padding: 32px;">No complaints filed yet.</p>`;
        return;
    }

    container.innerHTML = studentComplaints.map(c => {
        const statusClass = c.status === 'resolved' ? 'success' : c.status === 'in-progress' ? 'warning' : 'pending';
        return `
      <div class="complaint-card">
        <div class="complaint-header">
          <h4>${c.title}</h4>
          <span class="badge-status ${statusClass}">${c.status}</span>
        </div>
        <div class="complaint-body">${c.description}</div>
        <div class="complaint-footer">
          <span>📌 ${c.category}</span>
          <span>📅 ${formatDate(c.date)}</span>
        </div>
      </div>
    `;
    }).join('');
}

// ── Documents ──
function renderDocuments() {
    const container = document.getElementById('documents-list');
    if (!container) return;

    container.innerHTML = MockData.documents.map(doc => `
    <div class="file-item">
      <span class="file-icon">${doc.type === 'PDF' ? '📄' : '📝'}</span>
      <div class="file-info">
        <div class="file-name">${doc.name}</div>
        <div class="file-size">${doc.size} • Uploaded by ${doc.uploadedBy} • ${formatDate(doc.date)}</div>
      </div>
      <button class="btn btn-sm btn-secondary" onclick="Toast.show('Download started!', 'success')">⬇️</button>
    </div>
  `).join('');
}

// ── Complaint Modal ──
function openComplaintModal() {
    document.getElementById('complaint-modal').classList.add('open');
}

function closeComplaintModal() {
    document.getElementById('complaint-modal').classList.remove('open');
}

function initComplaintForm() {
    const form = document.getElementById('complaint-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const title = document.getElementById('complaint-title').value;
        const desc = document.getElementById('complaint-desc').value;

        if (!title || !desc) {
            Toast.show('Please fill in all fields', 'warning');
            return;
        }

        Toast.show('Complaint submitted successfully!', 'success');
        closeComplaintModal();
        form.reset();

        // Add to list
        const container = document.getElementById('student-complaints-list');
        const card = document.createElement('div');
        card.className = 'complaint-card';
        card.style.animation = 'fadeInUp 0.4s ease';
        card.innerHTML = `
      <div class="complaint-header">
        <h4>${title}</h4>
        <span class="badge-status pending">pending</span>
      </div>
      <div class="complaint-body">${desc}</div>
      <div class="complaint-footer">
        <span>📌 ${document.getElementById('complaint-category').value}</span>
        <span>📅 ${formatDate(new Date())}</span>
      </div>
    `;
        container.prepend(card);
    });
}

// Handle resize for charts
window.addEventListener('resize', () => {
    clearTimeout(window._resizeTimer);
    window._resizeTimer = setTimeout(initCharts, 250);
});
