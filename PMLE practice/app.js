document.addEventListener('DOMContentLoaded', () => {
  // --- State Variables ---
  let allQuestions = [];
  let currentQuestionsPool = [];
  let currentIndex = 0;
  let userAnswers = {}; // { qId: { selectedOption: 'A', isCorrect: bool, isSubmitted: bool } }

  // --- DOM Elements ---
  const topicFilter = document.getElementById('topicFilter');
  const shuffleBtn = document.getElementById('shuffleBtn');
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');
  const resetBtn = document.getElementById('resetBtn');

  const correctCountEl = document.getElementById('correctCount');
  const wrongCountEl = document.getElementById('wrongCount');
  const remainingCountEl = document.getElementById('remainingCount');
  const accuracyPctEl = document.getElementById('accuracyPct');
  const overallProgress = document.getElementById('overallProgress');
  const topicBreakdown = document.getElementById('topicBreakdown');
  const questionGrid = document.getElementById('questionGrid');

  const badgeTopic = document.getElementById('badgeTopic');
  const badgeIndex = document.getElementById('badgeIndex');
  const originalUrl = document.getElementById('originalUrl');
  const questionPrompt = document.getElementById('questionPrompt');
  const optionsContainer = document.getElementById('optionsContainer');
  const feedbackBox = document.getElementById('feedbackBox');
  const feedbackHeader = document.getElementById('feedbackHeader');
  const correctAnswerText = document.getElementById('correctAnswerText');
  const communityVoteText = document.getElementById('communityVoteText');
  const discussionList = document.getElementById('discussionList');

  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const checkBtn = document.getElementById('checkBtn');

  // --- Initialize App ---
  initTheme();
  loadProgress();
  fetchQuestions();

  // --- Event Listeners ---
  themeToggle.addEventListener('click', toggleTheme);
  topicFilter.addEventListener('change', handleFilterChange);
  shuffleBtn.addEventListener('click', handleShuffle);
  resetBtn.addEventListener('click', handleResetProgress);
  prevBtn.addEventListener('click', () => navigate(-1));
  nextBtn.addEventListener('click', () => navigate(1));
  checkBtn.addEventListener('click', handleCheckAnswer);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') navigate(-1);
    if (e.key === 'ArrowRight') navigate(1);
    if (e.key === 'Enter') handleCheckAnswer();
    if (['a', 'b', 'c', 'd'].includes(e.key.toLowerCase())) {
      const letter = e.key.toUpperCase();
      selectOption(letter);
    }
  });

  // --- Core Functions ---
  async function fetchQuestions() {
    try {
      const resp = await fetch('questions.json');
      allQuestions = await resp.json();
      applyFilter();
    } catch (err) {
      console.error('Failed to load questions.json', err);
      questionPrompt.textContent = 'Error loading questions dataset.';
    }
  }

  function applyFilter() {
    const filter = topicFilter.value;
    if (filter === 'all') {
      currentQuestionsPool = [...allQuestions];
    } else {
      currentQuestionsPool = allQuestions.filter(q => q.topic === filter);
    }
    currentIndex = 0;
    renderCurrentQuestion();
    renderGrid();
    updateScoreboard();
  }

  function handleFilterChange() {
    applyFilter();
  }

  function handleShuffle() {
    // Fisher-Yates shuffle
    for (let i = currentQuestionsPool.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [currentQuestionsPool[i], currentQuestionsPool[j]] = [currentQuestionsPool[j], currentQuestionsPool[i]];
    }
    currentIndex = 0;
    renderCurrentQuestion();
    renderGrid();
  }

  function renderCurrentQuestion() {
    if (!currentQuestionsPool.length) return;

    const q = currentQuestionsPool[currentIndex];
    const qState = userAnswers[q.id] || { selectedOption: null, isSubmitted: false };

    badgeTopic.textContent = `${q.topic} (Q${q.topic_q_num})`;
    badgeIndex.textContent = `Question ${currentIndex + 1} of ${currentQuestionsPool.length}`;
    originalUrl.href = q.url || '#';

    questionPrompt.textContent = q.question;

    // Render Options
    optionsContainer.innerHTML = '';
    const options = q.options || {};
    
    Object.keys(options).sort().forEach(letter => {
      const text = options[letter];
      const optionEl = document.createElement('div');
      optionEl.className = 'option-item';
      if (qState.selectedOption === letter) {
        optionEl.classList.add('selected');
      }

      if (qState.isSubmitted) {
        if (letter === q.correct_option) {
          optionEl.classList.add('correct-answer');
        } else if (qState.selectedOption === letter) {
          optionEl.classList.add('wrong-answer');
        }
      }

      optionEl.innerHTML = `
        <div class="option-key">${letter}</div>
        <div class="option-text">${escapeHtml(text)}</div>
      `;

      optionEl.addEventListener('click', () => {
        if (!qState.isSubmitted) {
          selectOption(letter);
        }
      });

      optionsContainer.appendChild(optionEl);
    });

    // Render Feedback / Explanation Box
    if (qState.isSubmitted) {
      feedbackBox.classList.remove('hidden');
      if (qState.isCorrect) {
        feedbackHeader.className = 'feedback-header is-correct';
        feedbackHeader.innerHTML = '✓ Correct Answer!';
      } else {
        feedbackHeader.className = 'feedback-header is-wrong';
        feedbackHeader.innerHTML = '✗ Incorrect Answer';
      }

      correctAnswerText.textContent = `${q.correct_option}. ${q.options[q.correct_option] || ''}`;

      // Votes
      const votes = q.vote_counts || {};
      const voteStr = Object.keys(votes).map(k => `${k}: ${votes[k]} vote(s)`).join(', ');
      communityVoteText.textContent = voteStr || 'Not available';

      // Discussion notes
      discussionList.innerHTML = '';
      const notes = (q.discussion || []).slice(0, 5);
      if (notes.length) {
        notes.forEach(note => {
          const li = document.createElement('li');
          li.textContent = note;
          discussionList.appendChild(li);
        });
      } else {
        const li = document.createElement('li');
        li.textContent = 'No discussion comments available.';
        discussionList.appendChild(li);
      }

      checkBtn.textContent = 'Submitted';
      checkBtn.disabled = true;
    } else {
      feedbackBox.classList.add('hidden');
      checkBtn.textContent = 'Check Answer';
      checkBtn.disabled = !qState.selectedOption;
    }

    // Update Nav Buttons
    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex === currentQuestionsPool.length - 1;

    highlightGridItem();
  }

  function selectOption(letter) {
    const q = currentQuestionsPool[currentIndex];
    const qState = userAnswers[q.id] || { selectedOption: null, isSubmitted: false };
    if (qState.isSubmitted) return;

    userAnswers[q.id] = { ...qState, selectedOption: letter };
    saveProgress();
    renderCurrentQuestion();
  }

  function handleCheckAnswer() {
    const q = currentQuestionsPool[currentIndex];
    const qState = userAnswers[q.id];
    if (!qState || !qState.selectedOption || qState.isSubmitted) return;

    const isCorrect = (qState.selectedOption === q.correct_option);
    userAnswers[q.id] = {
      ...qState,
      isCorrect,
      isSubmitted: true
    };

    saveProgress();
    renderCurrentQuestion();
    renderGrid();
    updateScoreboard();
  }

  function navigate(direction) {
    const newIdx = currentIndex + direction;
    if (newIdx >= 0 && newIdx < currentQuestionsPool.length) {
      currentIndex = newIdx;
      renderCurrentQuestion();
    }
  }

  function renderGrid() {
    questionGrid.innerHTML = '';
    currentQuestionsPool.forEach((q, idx) => {
      const qState = userAnswers[q.id];
      const gridNum = document.createElement('button');
      gridNum.className = 'grid-num';
      gridNum.textContent = idx + 1;

      if (idx === currentIndex) gridNum.classList.add('current');
      if (qState && qState.isSubmitted) {
        if (qState.isCorrect) gridNum.classList.add('correct');
        else gridNum.classList.add('wrong');
      }

      gridNum.addEventListener('click', () => {
        currentIndex = idx;
        renderCurrentQuestion();
      });

      questionGrid.appendChild(gridNum);
    });
  }

  function highlightGridItem() {
    const items = questionGrid.querySelectorAll('.grid-num');
    items.forEach((item, idx) => {
      if (idx === currentIndex) item.classList.add('current');
      else item.classList.remove('current');
    });
  }

  function updateScoreboard() {
    let correct = 0;
    let wrong = 0;
    const topicStats = {};

    // Initialize topic stats
    ['Topic 1', 'Topic 2', 'Topic 3', 'Topic 4'].forEach(t => {
      topicStats[t] = { total: 0, correct: 0, wrong: 0 };
    });

    allQuestions.forEach(q => {
      if (topicStats[q.topic]) {
        topicStats[q.topic].total += 1;
      }
      const state = userAnswers[q.id];
      if (state && state.isSubmitted) {
        if (state.isCorrect) {
          correct += 1;
          if (topicStats[q.topic]) topicStats[q.topic].correct += 1;
        } else {
          wrong += 1;
          if (topicStats[q.topic]) topicStats[q.topic].wrong += 1;
        }
      }
    });

    const attempted = correct + wrong;
    const totalCount = allQuestions.length;
    const remaining = totalCount - attempted;
    const accuracy = attempted > 0 ? Math.round((correct / attempted) * 100) : 0;

    correctCountEl.textContent = correct;
    wrongCountEl.textContent = wrong;
    remainingCountEl.textContent = remaining;
    accuracyPctEl.textContent = `${accuracy}%`;

    const progressPct = Math.round((attempted / totalCount) * 100);
    overallProgress.style.width = `${progressPct}%`;

    // Render Topic Breakdown
    topicBreakdown.innerHTML = '';
    Object.keys(topicStats).forEach(topicName => {
      const stat = topicStats[topicName];
      const topicAttempted = stat.correct + stat.wrong;
      const topicPct = stat.total > 0 ? Math.round((topicAttempted / stat.total) * 100) : 0;

      const row = document.createElement('div');
      row.className = 'topic-row';
      row.innerHTML = `
        <div class="topic-info">
          <span>${topicName}</span>
          <span>${stat.correct}/${stat.total} (${stat.correct} ✔, ${stat.wrong} ✖)</span>
        </div>
        <div class="topic-bar-bg">
          <div class="topic-bar-fill" style="width: ${topicPct}%;"></div>
        </div>
      `;
      topicBreakdown.appendChild(row);
    });
  }

  function handleResetProgress() {
    if (confirm('Are you sure you want to reset all your practice progress and scores?')) {
      userAnswers = {};
      saveProgress();
      renderCurrentQuestion();
      renderGrid();
      updateScoreboard();
    }
  }

  // --- Persistence & Helpers ---
  function saveProgress() {
    localStorage.setItem('genai_exam_progress', JSON.stringify(userAnswers));
  }

  function loadProgress() {
    const saved = localStorage.getItem('genai_exam_progress');
    if (saved) {
      try {
        userAnswers = JSON.parse(saved);
      } catch (e) {
        userAnswers = {};
      }
    }
  }

  function initTheme() {
    const theme = localStorage.getItem('genai_exam_theme') || 'light';
    if (theme === 'dark') {
      document.body.className = 'dark-theme';
      themeIcon.textContent = '☀️';
    } else {
      document.body.className = 'light-theme';
      themeIcon.textContent = '🌙';
    }
  }

  function toggleTheme() {
    if (document.body.classList.contains('dark-theme')) {
      document.body.className = 'light-theme';
      themeIcon.textContent = '🌙';
      localStorage.setItem('genai_exam_theme', 'light');
    } else {
      document.body.className = 'dark-theme';
      themeIcon.textContent = '☀️';
      localStorage.setItem('genai_exam_theme', 'dark');
    }
  }

  function escapeHtml(str) {
    return (str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
});
