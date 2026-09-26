const state = {
  currentView: 'dashboard',
  skills: [],
  currentSkill: null,
  activeAssessment: null,
  currentQuestionIndex: 0,
  userAnswers: {},
  timerInterval: null,
  remainingSeconds: 600,
  lastResult: null,
  history: []
};

async function apiRequest(url, method = 'GET', body = null) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json'
    }
  };
  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const res = await fetch(url, options);
    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || `HTTP error ${res.status}`);
    }
    return data.data;
  } catch (err) {
    handleApiError(err);
    throw err;
  }
}

function handleApiError(err) {
  console.error('[SkillForge API Error]:', err);
  showToast(err.message || 'An unexpected error occurred.', 'error');
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function formatDate(dateStr) {
  if (!dateStr) return 'N/A';
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (e) {
    return dateStr;
  }
}

function calculateProgress(correct, total) {
  if (!total || total === 0) return 0;
  return Math.round((correct / total) * 100);
}

function navigateTo(viewName, params = {}) {
  state.currentView = viewName;

  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.dataset.view === viewName) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  document.querySelectorAll('.view-section').forEach(sec => {
    sec.classList.remove('active');
  });

  const targetSec = document.getElementById(`view-${viewName}`);
  if (targetSec) {
    targetSec.classList.add('active');
  }

  if (viewName === 'dashboard') {
    loadDashboardView();
  } else if (viewName === 'skills') {
    loadSkillsView();
  } else if (viewName === 'history') {
    loadHistoryView();
  } else if (viewName === 'result') {
    renderResultView();
  }
}

async function loadDashboardView() {
  const container = document.getElementById('dashboardContent');
  if (!container) return;

  container.innerHTML = `
    <div class="state-box">
      <div class="spinner"></div>
      <p>Loading your learning metrics...</p>
    </div>
  `;

  try {
    const dash = await apiRequest('/api/dashboard');
    renderDashboard(dash);
  } catch (e) {
    container.innerHTML = `
      <div class="state-box">
        <div class="state-icon">⚠️</div>
        <h3>Unable to load assessment data</h3>
        <p>Please check your server connection and retry.</p>
        <button class="btn-primary-action" onclick="loadDashboardView()" style="margin-top:1rem;">Retry</button>
      </div>
    `;
  }
}

function renderDashboard(data) {
  const container = document.getElementById('dashboardContent');
  
  const skillCardsHtml = data.skill_progress.map(s => `
    <div class="skill-prog-card">
      <div class="prog-head">
        <span class="prog-name">${s.skill_name}</span>
        <span class="prog-badge">${s.attempt_count} attempts</span>
      </div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="width: ${s.progress_percentage}%"></div>
      </div>
      <div class="prog-metrics">
        <span>Best: <strong>${s.best_score}%</strong></span>
        <span>Avg: <strong>${s.average_score}%</strong></span>
      </div>
    </div>
  `).join('');

  const recentHtml = data.recent_attempts.length === 0 ? `
    <div class="state-box" style="padding:1.5rem;">
      <p>No assessment attempts recorded yet. Choose a skill to start!</p>
    </div>
  ` : `
    <div class="history-table-card">
      <table class="history-table">
        <thead>
          <tr>
            <th>Skill</th>
            <th>Date</th>
            <th>Score</th>
            <th>Percentage</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          ${data.recent_attempts.map(a => `
            <tr>
              <td><strong>${a.skill_name}</strong></td>
              <td>${formatDate(a.timestamp)}</td>
              <td>${a.correct} / ${a.total}</td>
              <td><span class="status-badge ${a.score_percentage >= 70 ? 'correct' : 'incorrect'}">${a.score_percentage}%</span></td>
              <td><button class="btn-secondary" style="padding:0.35rem 0.75rem; font-size:0.8rem;" onclick="viewAttemptDetails('${a.attempt_id}')">Review</button></td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;

  container.innerHTML = `
    <div class="dashboard-welcome">
      <div class="welcome-text">
        <h1>Welcome back, ${data.student_name}!</h1>
        <p>Track your skill assessments and keep sharpening your knowledge.</p>
      </div>
      <button class="btn-primary-action" onclick="navigateTo('skills')">
        Start Assessment →
      </button>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon blue">📝</div>
        <div class="stat-info">
          <div class="stat-value">${data.assessments_taken}</div>
          <div class="stat-label">Assessments Taken</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green">📊</div>
        <div class="stat-info">
          <div class="stat-value">${data.average_score}%</div>
          <div class="stat-label">Average Score</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon amber">🏆</div>
        <div class="stat-info">
          <div class="stat-value">${data.best_score}%</div>
          <div class="stat-label">Best Recorded Score</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon violet">❓</div>
        <div class="stat-info">
          <div class="stat-value">${data.questions_answered}</div>
          <div class="stat-label">Questions Answered</div>
        </div>
      </div>
    </div>

    <div class="section-header">
      <h2 class="section-title">Skill Mastery Progress</h2>
    </div>
    <div class="skills-progress-grid">
      ${skillCardsHtml}
    </div>

    <div class="section-header">
      <h2 class="section-title">Recent Assessments</h2>
    </div>
    ${recentHtml}
  `;
}

async function loadSkillsView() {
  const container = document.getElementById('skillsGrid');
  if (!container) return;

  container.innerHTML = `
    <div class="state-box" style="grid-column: 1 / -1;">
      <div class="spinner"></div>
      <p>Loading available skill assessments...</p>
    </div>
  `;

  try {
    state.skills = await apiRequest('/api/skills');
    renderSkills();
  } catch (e) {
    container.innerHTML = `
      <div class="state-box" style="grid-column: 1 / -1;">
        <p>Unable to load skills. Please check your backend.</p>
      </div>
    `;
  }
}

function renderSkills() {
  const container = document.getElementById('skillsGrid');
  const searchKey = (document.getElementById('skillSearchInput')?.value || '').toLowerCase().trim();
  const catFilter = document.getElementById('categorySelect')?.value || 'all';
  const diffFilter = document.getElementById('difficultySelect')?.value || 'all';

  const filtered = state.skills.filter(s => {
    const matchesSearch = s.name.toLowerCase().includes(searchKey) || s.description.toLowerCase().includes(searchKey);
    const matchesCat = catFilter === 'all' || s.category === catFilter;
    const matchesDiff = diffFilter === 'all' || s.difficulty === diffFilter;
    return matchesSearch && matchesCat && matchesDiff;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="state-box" style="grid-column: 1 / -1;">
        <div class="state-icon">🔍</div>
        <h3>No matching skills found</h3>
        <p>Try clearing your search query or filters.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(s => `
    <div class="skill-card">
      <div class="skill-card-top">
        <span class="skill-category-badge">${s.category}</span>
        <span class="difficulty-badge diff-${s.difficulty.toLowerCase()}">${s.difficulty}</span>
      </div>
      <h3 class="skill-card-title">${s.name}</h3>
      <p class="skill-card-desc">${s.description}</p>
      <div class="skill-card-meta">
        <span>${s.question_count} Questions</span>
        <span>Best: <strong>${s.best_score}%</strong></span>
      </div>
      <button class="btn-start-asm" onclick="openAssessmentSetup('${s.id}')">
        Start Assessment
      </button>
    </div>
  `).join('');
}

function openAssessmentSetup(skillId) {
  const skill = state.skills.find(s => s.id === skillId);
  if (!skill) return;

  state.currentSkill = skill;

  const container = document.getElementById('view-assessment');
  container.innerHTML = `
    <div class="assessment-setup-card">
      <div class="setup-icon">🚀</div>
      <h2 class="setup-title">${skill.name} Assessment</h2>
      <p class="setup-subtitle">Test your knowledge with 10 targeted multiple-choice questions.</p>
      
      <div class="setup-stats-row">
        <div class="setup-stat-item">
          <div class="val">${skill.question_count}</div>
          <div class="lbl">Questions</div>
        </div>
        <div class="setup-stat-item">
          <div class="val">10 Mins</div>
          <div class="lbl">Timer</div>
        </div>
        <div class="setup-stat-item">
          <div class="val">${skill.best_score}%</div>
          <div class="lbl">Best Score</div>
        </div>
      </div>

      <div style="display:flex; gap:1rem; justify-content:center;">
        <button class="btn-secondary" onclick="navigateTo('skills')">Cancel</button>
        <button class="btn-primary-action" onclick="startAssessment('${skill.id}')">Begin Assessment Now</button>
      </div>
    </div>
  `;

  navigateTo('assessment');
}

async function startAssessment(skillId) {
  try {
    const data = await apiRequest('/api/assessments/start', 'POST', { skill_id: skillId });
    
    state.activeAssessment = data;
    state.currentQuestionIndex = 0;
    state.userAnswers = {};
    state.remainingSeconds = data.duration_seconds || 600;

    startTimer();
    renderAssessmentRunner();
  } catch (e) {
    showToast('Failed to start assessment: ' + e.message, 'error');
  }
}

function startTimer() {
  if (state.timerInterval) clearInterval(state.timerInterval);

  state.timerInterval = setInterval(() => {
    state.remainingSeconds--;
    updateTimerUI();

    if (state.remainingSeconds <= 0) {
      clearInterval(state.timerInterval);
      showToast('Time expired! Automatically submitting assessment...', 'error');
      autoSubmitAssessment();
    }
  }, 1000);
}

function updateTimerUI() {
  const timerBadge = document.getElementById('timerBadge');
  if (!timerBadge) return;

  const mins = Math.floor(state.remainingSeconds / 60).toString().padStart(2, '0');
  const secs = (state.remainingSeconds % 60).toString().padStart(2, '0');
  
  timerBadge.innerHTML = `⏱️ ${mins}:${secs} remaining`;
  
  if (state.remainingSeconds <= 60) {
    timerBadge.classList.add('urgent');
  } else {
    timerBadge.classList.remove('urgent');
  }
}

function renderAssessmentRunner() {
  const container = document.getElementById('view-assessment');
  const asm = state.activeAssessment;
  if (!asm) return;

  const qIndex = state.currentQuestionIndex;
  const currentQ = asm.questions[qIndex];
  const total = asm.questions.length;
  const progressPct = Math.round(((qIndex + 1) / total) * 100);

  const navPillsHtml = asm.questions.map((q, idx) => {
    const isCurrent = idx === qIndex;
    const isAnswered = state.userAnswers[q.id] !== undefined;
    let cls = 'q-nav-pill';
    if (isAnswered) cls += ' answered';
    if (isCurrent) cls += ' active';
    return `<button class="${cls}" onclick="jumpToQuestion(${idx})">${idx + 1}</button>`;
  }).join('');

  const selectedOpt = state.userAnswers[currentQ.id];
  const optionsHtml = currentQ.options.map(opt => {
    const isSelected = selectedOpt === opt.id;
    return `
      <div class="option-card ${isSelected ? 'selected' : ''}" onclick="selectOption('${currentQ.id}', '${opt.id}')">
        <div class="option-key">${opt.id}</div>
        <div class="option-text">${opt.text}</div>
      </div>
    `;
  }).join('');

  container.innerHTML = `
    <div class="assessment-container">
      <div class="assessment-header">
        <div class="asm-top-bar">
          <span class="asm-skill-name">${asm.skill.name}</span>
          <div id="timerBadge" class="timer-badge">⏱️ 10:00 remaining</div>
        </div>
        <div class="asm-progress-wrap">
          <div class="asm-progress-bar">
            <div class="asm-progress-fill" style="width: ${progressPct}%"></div>
          </div>
          <span class="asm-q-count">Question ${qIndex + 1} of ${total}</span>
        </div>
      </div>

      <div class="question-nav-grid">
        ${navPillsHtml}
      </div>

      <div class="question-card">
        <span class="difficulty-badge diff-${currentQ.difficulty.toLowerCase()}">Difficulty: ${currentQ.difficulty}</span>
        <h3 class="q-text">${currentQ.question}</h3>
        <div class="options-list">
          ${optionsHtml}
        </div>
      </div>

      <div class="asm-actions">
        <button class="btn-secondary" onclick="navigateQuestion(-1)" ${qIndex === 0 ? 'disabled style="opacity:0.5;cursor:not-allowed;"' : ''}>
          ← Previous
        </button>
        
        <div>
          ${qIndex === total - 1 ? `
            <button class="btn-submit-asm" onclick="confirmAndSubmitAssessment()">
              Submit Assessment ✓
            </button>
          ` : `
            <button class="btn-primary-action" onclick="navigateQuestion(1)">
              Next Question →
            </button>
          `}
        </div>
      </div>
    </div>
  `;

  updateTimerUI();
}

function selectOption(qId, optId) {
  state.userAnswers[qId] = optId;
  renderAssessmentRunner();
}

function navigateQuestion(dir) {
  const newIdx = state.currentQuestionIndex + dir;
  if (newIdx >= 0 && newIdx < state.activeAssessment.questions.length) {
    state.currentQuestionIndex = newIdx;
    renderAssessmentRunner();
  }
}

function jumpToQuestion(idx) {
  if (idx >= 0 && idx < state.activeAssessment.questions.length) {
    state.currentQuestionIndex = idx;
    renderAssessmentRunner();
  }
}

function confirmAndSubmitAssessment() {
  const answeredCount = Object.keys(state.userAnswers).length;
  const total = state.activeAssessment.questions.length;
  const unanswered = total - answeredCount;

  if (unanswered > 0) {
    if (confirm(`You have ${unanswered} unanswered question(s). Are you sure you want to submit?`)) {
      autoSubmitAssessment();
    }
  } else {
    autoSubmitAssessment();
  }
}

async function autoSubmitAssessment() {
  if (state.timerInterval) clearInterval(state.timerInterval);

  const asm = state.activeAssessment;
  if (!asm) return;

  const payload = {
    assessment_id: asm.assessment_id,
    skill_id: asm.skill.id,
    answers: state.userAnswers
  };

  try {
    const result = await apiRequest('/api/assessments/submit', 'POST', payload);
    state.lastResult = result;
    state.activeAssessment = null;
    navigateTo('result');
  } catch (e) {
    showToast('Submission error: ' + e.message, 'error');
  }
}

function renderResultView() {
  const container = document.getElementById('view-result');
  const res = state.lastResult;

  if (!res) {
    container.innerHTML = `
      <div class="state-box">
        <h3>No result data available.</h3>
        <button class="btn-primary-action" onclick="navigateTo('skills')">Choose a Skill</button>
      </div>
    `;
    return;
  }

  const reviewCardsHtml = res.reviews.map((r, idx) => `
    <div class="review-card ${r.status}">
      <div class="review-head">
        <strong>Question ${idx + 1}</strong>
        <span class="status-badge ${r.status}">${r.status}</span>
      </div>
      <p style="font-weight:600; font-size:1.05rem; margin-bottom:0.75rem;">${r.question}</p>
      
      <div class="review-ans-grid">
        <div class="review-ans-box">
          <label>Your Answer</label>
          <strong style="color: ${r.status === 'correct' ? '#047857' : (r.status === 'incorrect' ? '#b91c1c' : '#64748b')}">
            ${r.user_answer ? `${r.user_answer}` : 'Unanswered'}
          </strong>
        </div>
        <div class="review-ans-box">
          <label>Correct Answer</label>
          <strong style="color: #047857;">${r.correct_answer}</strong>
        </div>
      </div>

      <div class="review-explanation">
        💡 <strong>Explanation:</strong> ${r.explanation}
      </div>
    </div>
  `).join('');

  container.innerHTML = `
    <div class="result-card">
      <span class="result-badge ${res.score_percentage >= 70 ? 'diff-easy' : 'diff-hard'}">
        Assessment Complete
      </span>
      <h2 style="font-size:1.8rem; font-weight:800; color:var(--text-dark);">${res.skill_name}</h2>
      
      <div class="score-circle-wrap" style="--pct: ${res.score_percentage}">
        <div class="score-circle-inner">
          <span class="score-percentage">${res.score_percentage}%</span>
          <span class="score-fraction">${res.correct} / ${res.total} Correct</span>
        </div>
      </div>

      <div class="result-breakdown-row">
        <div class="breakdown-box correct">
          <div class="breakdown-val">${res.correct}</div>
          <div class="breakdown-lbl">Correct</div>
        </div>
        <div class="breakdown-box incorrect">
          <div class="breakdown-val">${res.incorrect}</div>
          <div class="breakdown-lbl">Incorrect</div>
        </div>
        <div class="breakdown-box unanswered">
          <div class="breakdown-val">${res.unanswered}</div>
          <div class="breakdown-lbl">Unanswered</div>
        </div>
      </div>

      <div class="result-actions">
        <button class="btn-primary-action" onclick="openAssessmentSetup('${res.skill_id}')">Try Again</button>
        <button class="btn-secondary" onclick="navigateTo('skills')">Choose Another Skill</button>
        <button class="btn-secondary" onclick="navigateTo('dashboard')">View Dashboard</button>
      </div>

      <div class="review-section">
        <h3 class="section-title" style="margin-bottom:1.25rem;">Detailed Answer Review</h3>
        ${reviewCardsHtml}
      </div>
    </div>
  `;
}

async function loadHistoryView() {
  const container = document.getElementById('historyContent');
  if (!container) return;

  container.innerHTML = `
    <div class="state-box">
      <div class="spinner"></div>
      <p>Loading attempt history...</p>
    </div>
  `;

  try {
    const attempts = await apiRequest('/api/attempts');
    renderHistory(attempts);
  } catch (e) {
    container.innerHTML = `
      <div class="state-box">
        <p>Unable to load history.</p>
      </div>
    `;
  }
}

function renderHistory(attempts) {
  const container = document.getElementById('historyContent');

  if (attempts.length === 0) {
    container.innerHTML = `
      <div class="state-box">
        <div class="state-icon">📋</div>
        <h3>No Assessment History Yet</h3>
        <p>You haven't taken any skill assessments yet.</p>
        <button class="btn-primary-action" onclick="navigateTo('skills')" style="margin-top:1rem;">Explore Skills</button>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="history-table-card">
      <table class="history-table">
        <thead>
          <tr>
            <th>Attempt ID</th>
            <th>Skill</th>
            <th>Date / Time</th>
            <th>Score</th>
            <th>Accuracy</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          ${attempts.map(a => `
            <tr>
              <td><code>${a.attempt_id}</code></td>
              <td><strong>${a.skill_name}</strong></td>
              <td>${formatDate(a.timestamp)}</td>
              <td>${a.correct} / ${a.total}</td>
              <td>
                <span class="status-badge ${a.score_percentage >= 70 ? 'correct' : 'incorrect'}">
                  ${a.score_percentage}%
                </span>
              </td>
              <td>
                <button class="btn-secondary" style="padding:0.35rem 0.75rem; font-size:0.8rem;" onclick="viewAttemptDetails('${a.attempt_id}')">
                  View Review
                </button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

async function viewAttemptDetails(attemptId) {
  try {
    const attempt = await apiRequest(`/api/attempts/${attemptId}`);
    state.lastResult = attempt;
    navigateTo('result');
  } catch (e) {
    showToast('Failed to load attempt details.', 'error');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const view = link.dataset.view;
      navigateTo(view);
    });
  });

  navigateTo('dashboard');
});
