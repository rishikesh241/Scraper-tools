document.addEventListener('DOMContentLoaded', () => {
  // Official 6 Google Cloud PMLE Exam Sections (Aligned with June 2026 Exam Guide & Study Guide v2.0)
  const EXAM_SECTIONS = [
    {
      num: 1,
      id: 'Section 1',
      title: 'Section 1: Architecting low-code AI solutions',
      shortTitle: 'Low-Code AI & GenAI Solutions',
      weight: '13%',
      badgeClass: 'bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300',
      barClass: 'bg-blue-500',
      activeBorder: 'border-blue-500 bg-blue-50/60 dark:bg-blue-900/25'
    },
    {
      num: 2,
      id: 'Section 2',
      title: 'Section 2: Collaborating within and across teams to manage data and models',
      shortTitle: 'Data, Governance & Collaboration',
      weight: '16%',
      badgeClass: 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/40 dark:text-indigo-300',
      barClass: 'bg-indigo-500',
      activeBorder: 'border-indigo-500 bg-indigo-50/60 dark:bg-indigo-900/25'
    },
    {
      num: 3,
      id: 'Section 3',
      title: 'Section 3: Scaling prototypes into ML models',
      shortTitle: 'Scaling Prototypes & SFT/HPC',
      weight: '21%',
      badgeClass: 'bg-purple-100 text-purple-800 dark:bg-purple-900/40 dark:text-purple-300',
      barClass: 'bg-purple-500',
      activeBorder: 'border-purple-500 bg-purple-50/60 dark:bg-purple-900/25'
    },
    {
      num: 4,
      id: 'Section 4',
      title: 'Section 4: Serving and scaling models',
      shortTitle: 'Serving, Endpoints & Edge/MaaS',
      weight: '20%',
      badgeClass: 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300',
      barClass: 'bg-amber-500',
      activeBorder: 'border-amber-500 bg-amber-50/60 dark:bg-amber-900/25'
    },
    {
      num: 5,
      id: 'Section 5',
      title: 'Section 5: Automating and orchestrating ML pipelines',
      shortTitle: 'Automating & Orchestrating Pipelines',
      weight: '18%',
      badgeClass: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300',
      barClass: 'bg-emerald-500',
      activeBorder: 'border-emerald-500 bg-emerald-50/60 dark:bg-emerald-900/25'
    },
    {
      num: 6,
      id: 'Section 6',
      title: 'Section 6: Monitoring AI solutions',
      shortTitle: 'Monitoring, XAI & Model Armor',
      weight: '13%',
      badgeClass: 'bg-rose-100 text-rose-800 dark:bg-rose-900/40 dark:text-rose-300',
      barClass: 'bg-rose-500',
      activeBorder: 'border-rose-500 bg-rose-50/60 dark:bg-rose-900/25'
    }
  ];

  // Complete 1-indexed Section mapping for all 375 questions (Q#1 to Q#375 -> Section 1..6)
  // Section counts: Sec 1 = 60, Sec 2 = 31, Sec 3 = 104, Sec 4 = 66, Sec 5 = 66, Sec 6 = 48 (Total = 375)
  const QUESTION_SECTION_MAP = [
    0,
    1,3,3,3,5,3,1,5,5,3,3,4,3,3,3,3,2,1,5,3,3,4,2,3,3,
    3,3,3,4,3,6,5,3,5,5,3,5,4,5,3,3,3,3,1,3,4,2,2,3,2,
    2,3,3,5,3,1,3,3,5,3,3,3,1,3,3,3,1,1,1,3,1,6,5,4,6,
    2,4,3,3,3,6,3,4,3,3,2,1,1,6,3,3,1,3,3,5,3,1,3,5,3,
    3,6,2,1,1,1,3,6,3,1,1,3,2,3,3,2,3,3,3,3,2,3,3,5,5,
    6,3,6,5,4,4,3,3,5,3,6,6,5,3,3,3,5,4,3,4,3,2,2,3,3,
    5,3,3,3,3,1,3,1,3,6,3,3,3,4,1,5,4,5,1,4,3,2,6,6,4,
    2,3,6,4,5,4,4,3,3,6,5,4,6,4,6,4,6,4,4,4,1,5,3,5,1,
    5,3,5,5,2,6,1,5,3,4,5,3,5,5,1,5,5,4,5,3,1,6,4,2,6,
    4,6,5,6,5,3,2,5,4,6,1,1,4,4,4,5,5,2,4,6,4,6,4,2,1,
    5,1,4,2,5,4,4,6,5,2,2,4,5,1,1,6,5,3,6,5,5,4,4,6,6,
    1,4,3,5,5,4,1,1,5,1,1,5,4,5,3,6,5,5,1,1,1,1,1,5,2,
    6,1,4,4,5,1,4,1,6,6,2,4,2,2,5,6,6,6,4,2,1,1,4,3,6,
    4,5,4,4,6,3,1,6,6,5,6,1,3,4,1,3,5,5,3,3,4,1,1,2,4,
    1,4,4,1,4,4,4,3,5,4,5,4,5,1,2,3,6,1,1,6,6,4,4,6,1
  ];

  // 65 Grounded Notebook Overrides (42) + Curated High-Yield Study Note IDs (23)
  const COUNTER_NOTE_IDS = new Set([
    10, 18, 28, 40, 48, 69, 80, 85, 90, 94, 96, 99, 104, 105, 113, 116, 132, 138, 139, 140, 141,
    146, 149, 163, 164, 169, 184, 198, 200, 202, 207, 222, 223, 260, 263, 264, 265, 269, 277, 286,
    289, 290, 291, 295, 299, 301, 303, 305, 307, 311, 313, 318, 319, 320, 325, 327, 329, 330, 338,
    339, 341, 342, 344, 351, 373
  ]);

  let allQuestions = [];
  let activeQuestions = [];
  let currentIndex = 0;
  let activeFilter = {
    scope: 'all',    // 'all' | 'recent' | 'nb_diff' | 'nb_vs_gemini' | 'nb_vs_comm' | 'counter' | 'flagged' | 'wrong'
    section: null,   // null | 'Section 1'..'Section 6'
    topic: null,     // null | topic string
    label: 'All 6 Sections (375)'
  };
  let progress = {};
  let flags = [];
  try {
    progress = JSON.parse(localStorage.getItem('pmleProgress')) || {};
    flags = JSON.parse(localStorage.getItem('pmleFlags')) || [];
  } catch (_) {
    progress = {};
    flags = [];
  }
  let currentSelection = [];
  let resetPendingTimer = null;

  // Ensure DOM elements exist even if an older index.html is cached (built safely without innerHTML)
  function ensureDomStructure() {
    // 1. Add Study Suite quick-links in header if not already present
    const headerEl = document.querySelector('header');
    if (headerEl && !document.getElementById('study-suite-links')) {
      const brandWrap = headerEl.firstElementChild;
      if (brandWrap) {
        brandWrap.className = 'flex flex-col sm:flex-row sm:items-center gap-3 mb-4 sm:mb-0';
        const navWrap = document.createElement('nav');
        navWrap.id = 'study-suite-links';
        navWrap.setAttribute('aria-label', 'PMLE Study Guides');
        navWrap.className = 'flex flex-wrap items-center gap-1.5';
        const guides = [
          { href: 'PMLE_Reliable_Patterns.html', text: '1. Reliable Patterns' },
          { href: 'PMLE_Patterns_and_Core_Concepts_Guide.html', text: '2. Core Concepts' },
          { href: 'PMLE_Rapid_Revision_Cheat_Sheet.html', text: '3. Cheat Sheet (65 Notes)' },
          { href: 'PMLE_Q200_to_375_Rapid_Revision.html', text: '4. Q#200–375 Matrix' }
        ];
        guides.forEach(g => {
          const a = document.createElement('a');
          a.href = g.href;
          a.textContent = g.text;
          a.className = 'px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-100 hover:bg-blue-50 text-slate-600 hover:text-blue-700 dark:bg-slate-700/70 dark:hover:bg-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-600 transition';
          navWrap.appendChild(a);
        });
        brandWrap.appendChild(navWrap);
      }
    }

    // 2. Ensure 6 Exam Sections sidebar card exists
    const topicListEl = document.getElementById('topic-list');
    if (topicListEl && !document.getElementById('section-list')) {
      const topicCard = topicListEl.closest('div.bg-white');
      if (topicCard && topicCard.parentNode) {
        const secCard = document.createElement('div');
        secCard.className = 'bg-white dark:bg-slate-800 p-5 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700';

        const headRow = document.createElement('div');
        headRow.className = 'flex justify-between items-center mb-3';
        const h3 = document.createElement('h3');
        h3.className = 'font-bold text-slate-700 dark:text-slate-300';
        h3.textContent = '6 Exam Sections';
        const hint = document.createElement('span');
        hint.className = 'text-xs text-slate-500';
        hint.textContent = 'Click section to filter';
        headRow.appendChild(h3);
        headRow.appendChild(hint);

        const secListDiv = document.createElement('div');
        secListDiv.id = 'section-list';
        secListDiv.className = 'space-y-2 text-sm';

        secCard.appendChild(headRow);
        secCard.appendChild(secListDiv);
        topicCard.parentNode.insertBefore(secCard, topicCard);
      }
    }

    // 3. Ensure q-section-badge exists
    const qTopicBadge = document.getElementById('q-topic-badge');
    if (qTopicBadge && !document.getElementById('q-section-badge')) {
      const secBadge = document.createElement('span');
      secBadge.id = 'q-section-badge';
      secBadge.className = 'inline-block px-2.5 py-1 text-xs font-bold bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300 rounded-md mr-1.5 mb-1';
      qTopicBadge.parentNode.insertBefore(secBadge, qTopicBadge);
    }

    // 4. Ensure 3-card Grounded Notebook comparison exists even on older index.html
    const geminiBadgeEl = document.getElementById('gemini-answer-badge');
    if (geminiBadgeEl && !document.getElementById('notebook-answer-badge')) {
      const geminiCard = geminiBadgeEl.parentElement;
      const cardsGrid = geminiCard ? geminiCard.parentElement : null;
      if (cardsGrid) {
        cardsGrid.className = 'grid grid-cols-1 xl:grid-cols-3 gap-4';

        const nbCard = document.createElement('div');
        nbCard.className = 'bg-emerald-50/90 dark:bg-emerald-950/30 p-5 rounded-xl border-2 border-emerald-300 dark:border-emerald-700 flex flex-col';

        const nbHead = document.createElement('div');
        nbHead.className = 'flex items-center justify-between gap-2 mb-3';
        const nbTitleWrap = document.createElement('div');
        nbTitleWrap.className = 'flex items-center gap-2';
        const nbIcon = document.createElement('span');
        nbIcon.className = 'text-xl';
        nbIcon.textContent = '📓';
        const nbH4 = document.createElement('h4');
        nbH4.className = 'font-bold text-sm uppercase tracking-wider text-emerald-800 dark:text-emerald-300';
        nbH4.textContent = 'Notebook Grounded';
        nbTitleWrap.appendChild(nbIcon);
        nbTitleWrap.appendChild(nbH4);

        const nbTag = document.createElement('span');
        nbTag.className = 'text-[10px] font-extrabold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-200/80 text-emerald-900 dark:bg-emerald-800 dark:text-emerald-100';
        nbTag.textContent = 'Final Key';
        nbHead.appendChild(nbTitleWrap);
        nbHead.appendChild(nbTag);

        const nbBadge = document.createElement('div');
        nbBadge.id = 'notebook-answer-badge';
        nbBadge.className = 'self-start mb-2 px-3 py-1 bg-emerald-600 text-white text-xs font-bold rounded';

        const nbSrc = document.createElement('div');
        nbSrc.id = 'notebook-source-ref';
        nbSrc.className = 'mb-3 text-[11px] font-medium text-emerald-800/90 dark:text-emerald-300/90 bg-emerald-100/70 dark:bg-emerald-900/40 px-2.5 py-1 rounded border border-emerald-200 dark:border-emerald-800/60';

        const nbRat = document.createElement('div');
        nbRat.id = 'notebook-rationale';
        nbRat.className = 'text-sm leading-relaxed text-slate-700 dark:text-slate-300 whitespace-pre-line max-h-72 overflow-y-auto custom-scrollbar pr-2';

        nbCard.appendChild(nbHead);
        nbCard.appendChild(nbBadge);
        nbCard.appendChild(nbSrc);
        nbCard.appendChild(nbRat);
        cardsGrid.insertBefore(nbCard, geminiCard);
      }
    }
  }

  ensureDomStructure();

  // DOM Elements
  const els = {
    total: document.getElementById('stat-total'),
    attempted: document.getElementById('stat-attempted'),
    accuracy: document.getElementById('stat-accuracy'),
    wrong: document.getElementById('stat-wrong'),
    activeFilterLabel: document.getElementById('active-filter-label'),
    quickFilterList: document.getElementById('quick-filter-list'),
    sectionList: document.getElementById('section-list'),
    topicList: document.getElementById('topic-list'),
    grid: document.getElementById('grid-container'),
    gridCountLabel: document.getElementById('grid-count-label'),
    qHeader: document.getElementById('q-header'),
    qSectionBadge: document.getElementById('q-section-badge'),
    qTopicBadge: document.getElementById('q-topic-badge'),
    qMultiBadge: document.getElementById('q-multi-badge'),
    qText: document.getElementById('q-text'),
    qImageBox: document.getElementById('q-image-container'),
    qImage: document.getElementById('q-image'),
    optionsBox: document.getElementById('options-container'),
    feedbackSec: document.getElementById('feedback-section'),
    feedbackAlert: document.getElementById('feedback-alert'),
    discList: document.getElementById('discussion-list'),
    prevBtn: document.getElementById('prevBtn'),
    nextBtn: document.getElementById('nextBtn'),
    submitBtn: document.getElementById('submitBtn'),
    flagBtn: document.getElementById('flagBtn'),
    shuffleBtn: document.getElementById('shuffleBtn'),
    resetBtn: document.getElementById('resetBtn'),
    themeToggle: document.getElementById('themeToggle')
  };

  // Theme Init
  try {
    if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  } catch (_) {}

  if (els.themeToggle) {
    els.themeToggle.addEventListener('click', () => {
      document.documentElement.classList.toggle('dark');
      try {
        localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
      } catch (_) {}
    });
  }

  function getSectionMeta(sectionNum) {
    return EXAM_SECTIONS.find(s => s.num === sectionNum) || EXAM_SECTIONS[2];
  }

  function enrichQuestionsWithSections(data) {
    return data.map((q, idx) => {
      const qid = q.id || (idx + 1);
      const secNum = q.section_num || QUESTION_SECTION_MAP[qid] || 3;
      const meta = getSectionMeta(secNum);
      return {
        ...q,
        id: qid,
        section_num: secNum,
        section_id: meta.id,
        section: meta.title,
        section_short: meta.shortTitle,
        section_weight: meta.weight,
        domain: `${meta.title} (~${meta.weight})`
      };
    });
  }

  function optsEqual(a, b) {
    const sa = [...(a || [])].sort().join(',');
    const sb = [...(b || [])].sort().join(',');
    return sa === sb;
  }

  function isNotebookOverride(q) {
    const nb = q.notebook_correct_option || q.correct_option;
    const gem = q.gemini_correct_option || q.correct_option;
    const comm = q.community_option || q.correct_option;
    return !optsEqual(nb, gem) || !optsEqual(nb, comm);
  }

  function isNotebookVsGemini(q) {
    const nb = q.notebook_correct_option || q.correct_option;
    const gem = q.gemini_correct_option || q.correct_option;
    return !optsEqual(nb, gem);
  }

  function isNotebookVsCommunity(q) {
    const nb = q.notebook_correct_option || q.correct_option;
    const comm = q.community_option || q.correct_option;
    return !optsEqual(nb, comm);
  }

  const VALID_SCOPES = ['recent', 'nb_diff', 'nb_vs_gemini', 'nb_vs_comm', 'counter', 'flagged', 'wrong'];

  function matchesScope(q, scope) {
    if (scope === 'recent') return q.id >= 200;
    if (scope === 'nb_diff') return isNotebookOverride(q);
    if (scope === 'nb_vs_gemini') return isNotebookVsGemini(q);
    if (scope === 'nb_vs_comm') return isNotebookVsCommunity(q);
    if (scope === 'counter') return COUNTER_NOTE_IDS.has(q.id);
    if (scope === 'flagged') return flags.includes(q.id);
    if (scope === 'wrong') return Boolean(progress[q.id] && !progress[q.id].isCorrect);
    return true;
  }

  function getScopeShortName(scope) {
    if (scope === 'recent') return 'Q#200–375';
    if (scope === 'nb_diff') return '📓 NB Overrides';
    if (scope === 'nb_vs_gemini') return '⚡ NB ≠ Gemini';
    if (scope === 'nb_vs_comm') return '📓 NB ≠ Vote';
    if (scope === 'counter') return '✨ Notes & Overrides';
    if (scope === 'flagged') return 'Flagged 🚩';
    if (scope === 'wrong') return 'Incorrect ✗';
    return null;
  }

  function recomputeActiveQuestions() {
    activeQuestions = allQuestions.filter(q => {
      if (!matchesScope(q, activeFilter.scope)) return false;
      if (activeFilter.section && q.section_id !== activeFilter.section) return false;
      if (activeFilter.topic && q.topic !== activeFilter.topic) return false;
      return true;
    });

    const parts = [];
    const scopeName = getScopeShortName(activeFilter.scope);
    if (scopeName) parts.push(scopeName);
    if (activeFilter.section) parts.push(activeFilter.section);
    if (activeFilter.topic) parts.push(activeFilter.topic);

    if (parts.length === 0) {
      activeFilter.label = `All 6 Sections (${activeQuestions.length})`;
    } else {
      activeFilter.label = `${parts.join(' • ')} (${activeQuestions.length})`;
    }
  }

  // Fetch Data
  fetch('questions.json')
    .then(r => r.json())
    .then(data => {
      allQuestions = enrichQuestionsWithSections(data);

      // Re-score any cached progress against the Grounded Notebook final correct_option
      let progressUpdated = false;
      allQuestions.forEach(q => {
        const finalOpts = q.notebook_correct_option || q.correct_option;
        if (progress[q.id] && Array.isArray(progress[q.id].selected)) {
          const expectedCorrect = optsEqual(progress[q.id].selected, finalOpts);
          if (progress[q.id].isCorrect !== expectedCorrect) {
            progress[q.id].isCorrect = expectedCorrect;
            progressUpdated = true;
          }
        }
      });
      if (progressUpdated) {
        try {
          localStorage.setItem('pmleProgress', JSON.stringify(progress));
        } catch (_) {}
      }

      recomputeActiveQuestions();
      refreshAllViews(true);
    });

  function refreshAllViews(resetIndex = false) {
    recomputeActiveQuestions();
    if (resetIndex) currentIndex = 0;
    if (currentIndex >= activeQuestions.length) currentIndex = Math.max(0, activeQuestions.length - 1);

    renderQuickFilters();
    renderSections();
    renderTopics();
    updateStats();
    renderGrid();
    if (activeQuestions.length > 0) {
      loadQuestion(currentIndex);
    } else {
      renderEmptyFilterState();
    }
  }

  function renderEmptyFilterState() {
    if (els.qHeader) els.qHeader.textContent = '0 Questions Match Current Filter';
    if (els.qSectionBadge) els.qSectionBadge.textContent = activeFilter.section || 'All Sections';
    if (els.qTopicBadge) els.qTopicBadge.textContent = activeFilter.topic || 'All Topics';
    if (els.qMultiBadge) els.qMultiBadge.classList.add('hidden');
    if (els.qText) {
      els.qText.textContent = `No questions match "${activeFilter.label}". Click any highlighted filter pill or section on the left to unselect it, or click "All" to reset.`;
    }
    if (els.qImageBox) els.qImageBox.classList.add('hidden');
    if (els.optionsBox) els.optionsBox.replaceChildren();
    if (els.feedbackSec) els.feedbackSec.classList.add('hidden');
    if (els.submitBtn) els.submitBtn.disabled = true;
    if (els.prevBtn) els.prevBtn.disabled = true;
    if (els.nextBtn) els.nextBtn.disabled = true;
  }

  window.applyFilter = (type, value) => {
    if (type === 'section') {
      activeFilter.section = (activeFilter.section === value) ? null : value;
    } else if (type === 'topic') {
      activeFilter.topic = (activeFilter.topic === value) ? null : value;
    } else if (type === 'all') {
      if (activeFilter.scope !== 'all') {
        activeFilter.scope = 'all';
      } else {
        activeFilter.section = null;
        activeFilter.topic = null;
      }
    } else if (VALID_SCOPES.includes(type)) {
      activeFilter.scope = (activeFilter.scope === type) ? 'all' : type;
    }

    refreshAllViews(true);
  };

  function renderQuickFilters() {
    if (!els.quickFilterList) return;
    const layerPool = allQuestions.filter(q => {
      if (activeFilter.section && q.section_id !== activeFilter.section) return false;
      if (activeFilter.topic && q.topic !== activeFilter.topic) return false;
      return true;
    });

    const recentCount = layerPool.filter(q => q.id >= 200).length;
    const nbDiffCount = layerPool.filter(q => isNotebookOverride(q)).length;
    const nbVsGeminiCount = layerPool.filter(q => isNotebookVsGemini(q)).length;
    const nbVsCommCount = layerPool.filter(q => isNotebookVsCommunity(q)).length;
    const counterCount = layerPool.filter(q => COUNTER_NOTE_IDS.has(q.id)).length;
    const flaggedCount = layerPool.filter(q => flags.includes(q.id)).length;
    const wrongCount = layerPool.filter(q => progress[q.id] && !progress[q.id].isCorrect).length;

    const pills = [
      { type: 'all', value: null, text: `All (${layerPool.length})` },
      { type: 'recent', value: '200-375', text: `Q#200–375 (${recentCount})` },
      { type: 'nb_diff', value: 'nb_diff', text: `📓 NB Overrides (${nbDiffCount})` },
      { type: 'nb_vs_gemini', value: 'nb_vs_gemini', text: `⚡ NB ≠ Gemini (${nbVsGeminiCount})` },
      { type: 'nb_vs_comm', value: 'nb_vs_comm', text: `👥 NB ≠ Vote (${nbVsCommCount})` },
      { type: 'counter', value: 'counter', text: `✨ Notes (${counterCount})` },
      { type: 'flagged', value: 'flagged', text: `🚩 (${flaggedCount})` },
      { type: 'wrong', value: 'wrong', text: `✗ Wrong (${wrongCount})` }
    ];

    els.quickFilterList.replaceChildren();
    pills.forEach(p => {
      const isActive = activeFilter.scope === p.type;
      const cls = isActive
        ? 'bg-google-blue text-white border-google-blue font-bold'
        : 'bg-slate-50 hover:bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-900 dark:hover:bg-slate-700 dark:text-slate-300 dark:border-slate-700 font-medium';
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `px-2.5 py-1 rounded-md text-xs border transition ${cls}`;
      btn.textContent = p.text;
      btn.addEventListener('click', () => window.applyFilter(p.type, p.value));
      els.quickFilterList.appendChild(btn);
    });
  }

  function renderSections() {
    if (!els.sectionList) return;
    const scopeTopicPool = allQuestions.filter(q => {
      if (!matchesScope(q, activeFilter.scope)) return false;
      if (activeFilter.topic && q.topic !== activeFilter.topic) return false;
      return true;
    });

    els.sectionList.replaceChildren();
    EXAM_SECTIONS.forEach(sec => {
      const secQuestions = scopeTopicPool.filter(q => q.section_id === sec.id);
      const count = secQuestions.length;
      let attempted = 0;
      let correct = 0;
      secQuestions.forEach(q => {
        if (progress[q.id]) {
          attempted++;
          if (progress[q.id].isCorrect) correct++;
        }
      });
      const acc = attempted > 0 ? Math.round((correct / attempted) * 100) : null;
      const pctDone = count > 0 ? Math.round((attempted / count) * 100) : 0;
      const isActive = activeFilter.section === sec.id;

      const cardCls = isActive
        ? `border-2 ${sec.activeBorder} shadow-sm`
        : 'border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/40';

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `w-full text-left p-2.5 rounded-lg transition block ${cardCls}`;
      btn.addEventListener('click', () => window.applyFilter('section', sec.id));

      const topRow = document.createElement('div');
      topRow.className = 'flex justify-between items-center gap-2 mb-1';

      const leftGroup = document.createElement('div');
      leftGroup.className = 'flex items-center gap-1.5';
      const secSpan = document.createElement('span');
      secSpan.className = `px-2 py-0.5 rounded text-[11px] font-bold ${sec.badgeClass}`;
      secSpan.textContent = sec.id;
      const weightSpan = document.createElement('span');
      weightSpan.className = 'text-[11px] font-semibold text-slate-400 dark:text-slate-500';
      weightSpan.textContent = `~${sec.weight}`;
      leftGroup.appendChild(secSpan);
      leftGroup.appendChild(weightSpan);

      const countSpan = document.createElement('span');
      countSpan.className = 'bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded text-xs font-bold text-slate-700 dark:text-slate-200';
      countSpan.textContent = `${count} Qs`;

      topRow.appendChild(leftGroup);
      topRow.appendChild(countSpan);

      const titleDiv = document.createElement('div');
      titleDiv.className = 'text-xs font-medium text-slate-700 dark:text-slate-300 leading-snug mb-1.5';
      titleDiv.textContent = sec.shortTitle;

      const statsRow = document.createElement('div');
      statsRow.className = 'flex justify-between items-center text-[11px] text-slate-500 dark:text-slate-400 mb-1';
      const ansSpan = document.createElement('span');
      ansSpan.textContent = `${attempted}/${count} answered`;
      const accSpan = document.createElement('span');
      accSpan.textContent = acc !== null ? `${acc}% acc` : 'Not started';
      statsRow.appendChild(ansSpan);
      statsRow.appendChild(accSpan);

      const barBg = document.createElement('div');
      barBg.className = 'w-full h-1.5 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden';
      const barFill = document.createElement('div');
      barFill.className = `h-full ${sec.barClass} transition-all duration-300`;
      barFill.style.width = `${pctDone}%`;
      barBg.appendChild(barFill);

      btn.appendChild(topRow);
      btn.appendChild(titleDiv);
      btn.appendChild(statsRow);
      btn.appendChild(barBg);
      els.sectionList.appendChild(btn);
    });
  }

  function renderTopics() {
    if (!els.topicList) return;
    const scopeSectionPool = allQuestions.filter(q => {
      if (!matchesScope(q, activeFilter.scope)) return false;
      if (activeFilter.section && q.section_id !== activeFilter.section) return false;
      return true;
    });

    const allTopicNames = [...new Set(allQuestions.map(q => q.topic))];
    const counts = {};
    allTopicNames.forEach(t => { counts[t] = 0; });
    scopeSectionPool.forEach(q => { counts[q.topic] = (counts[q.topic] || 0) + 1; });

    els.topicList.replaceChildren();
    for (const [topic, count] of Object.entries(counts)) {
      if (count === 0 && activeFilter.topic !== topic) continue;
      const isActive = activeFilter.topic === topic;
      const rowCls = isActive
        ? 'bg-indigo-50 dark:bg-indigo-900/30 border border-indigo-400 font-semibold'
        : 'hover:bg-slate-50 dark:hover:bg-slate-700/40 border border-transparent';

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `w-full flex justify-between items-center px-2.5 py-1.5 rounded-lg transition text-left ${rowCls}`;
      btn.addEventListener('click', () => window.applyFilter('topic', topic));

      const nameSpan = document.createElement('span');
      nameSpan.className = 'text-slate-600 dark:text-slate-300 text-xs';
      nameSpan.textContent = topic;

      const countSpan = document.createElement('span');
      countSpan.className = 'bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded text-xs font-bold';
      countSpan.textContent = String(count);

      btn.appendChild(nameSpan);
      btn.appendChild(countSpan);
      els.topicList.appendChild(btn);
    }
  }

  function updateStats() {
    let attempted = 0;
    let correct = 0;

    activeQuestions.forEach(q => {
      if (progress[q.id]) {
        attempted++;
        if (progress[q.id].isCorrect) correct++;
      }
    });

    const wrong = attempted - correct;
    const acc = attempted === 0 ? 0 : Math.round((correct / attempted) * 100);

    if (els.total) els.total.textContent = String(activeQuestions.length);
    if (els.attempted) els.attempted.textContent = String(attempted);
    if (els.wrong) els.wrong.textContent = String(wrong);
    if (els.accuracy) els.accuracy.textContent = acc + '%';
    if (els.activeFilterLabel) {
      els.activeFilterLabel.textContent = activeFilter.label;
    }
    if (els.gridCountLabel) {
      els.gridCountLabel.textContent = `${activeQuestions.length} question${activeQuestions.length === 1 ? '' : 's'}`;
    }
  }

  function renderGrid() {
    if (!els.grid) return;
    els.grid.replaceChildren();
    activeQuestions.forEach((q, idx) => {
      let bg = 'bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-400';
      if (progress[q.id]) {
        bg = progress[q.id].isCorrect
          ? 'bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-400'
          : 'bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-400';
      }

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.title = `Question #${q.id} (${q.section_id}: ${q.section_short})`;
      btn.className = `relative h-8 rounded text-xs font-bold hover:opacity-80 transition ${bg} ${idx === currentIndex ? 'ring-2 ring-google-blue' : ''}`;
      btn.textContent = String(q.id);
      btn.addEventListener('click', () => window.goToQuestion(idx));

      if (flags.includes(q.id)) {
        const dot = document.createElement('div');
        dot.className = 'absolute -top-1 -right-1 w-2 h-2 bg-yellow-400 rounded-full';
        btn.appendChild(dot);
      }

      els.grid.appendChild(btn);
    });
  }

  window.goToQuestion = (idx) => {
    currentIndex = idx;
    loadQuestion(idx);
    renderGrid();
  };

  function loadQuestion(idx) {
    const q = activeQuestions[idx];
    if (!q) return;
    currentSelection = [];

    const isUnfiltered = activeFilter.scope === 'all' && !activeFilter.section && !activeFilter.topic;
    if (isUnfiltered) {
      els.qHeader.textContent = `Question ${q.id} of ${allQuestions.length}`;
    } else {
      els.qHeader.textContent = `Question #${q.id} (${idx + 1} of ${activeQuestions.length} in ${activeFilter.label})`;
    }

    const secMeta = getSectionMeta(q.section_num);
    if (els.qSectionBadge) {
      els.qSectionBadge.className = `inline-block px-2.5 py-1 text-xs font-bold rounded-md ${secMeta.badgeClass}`;
      els.qSectionBadge.textContent = `${secMeta.title} (~${secMeta.weight})`;
    }
    if (els.qTopicBadge) els.qTopicBadge.textContent = q.topic;

    if (els.qMultiBadge) {
      if (q.is_multi) {
        els.qMultiBadge.classList.remove('hidden');
        els.qMultiBadge.classList.add('inline-block');
      } else {
        els.qMultiBadge.classList.add('hidden');
        els.qMultiBadge.classList.remove('inline-block');
      }
    }

    els.qText.textContent = q.question;
    if (els.qImageBox && els.qImage) {
      if (q.image) {
        els.qImage.src = q.image;
        els.qImageBox.classList.remove('hidden');
      } else {
        els.qImage.removeAttribute('src');
        els.qImageBox.classList.add('hidden');
      }
    }

    // Check if flagged
    if (els.flagBtn) {
      els.flagBtn.style.opacity = flags.includes(q.id) ? '1' : '0.3';
    }

    // Render Options safely via DOM APIs (prevents '<' or '>' in option text from breaking HTML)
    els.optionsBox.replaceChildren();
    for (const [key, val] of Object.entries(q.options)) {
      const type = q.is_multi ? 'checkbox' : 'radio';
      const lbl = document.createElement('label');
      lbl.id = `lbl-${key}`;
      lbl.className = 'option-btn block p-4 rounded-xl border-2 border-slate-200 dark:border-slate-700 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/50 transition relative';

      const row = document.createElement('div');
      row.className = 'flex gap-3';

      const inp = document.createElement('input');
      inp.type = type;
      inp.name = 'q-opt';
      inp.value = key;
      inp.className = 'mt-1';
      inp.addEventListener('change', () => window.toggleOpt(key, Boolean(q.is_multi)));

      const textWrap = document.createElement('div');
      const keySpan = document.createElement('span');
      keySpan.className = 'font-bold mr-2';
      keySpan.textContent = `${key}.`;
      const valSpan = document.createElement('span');
      valSpan.textContent = val;

      textWrap.appendChild(keySpan);
      textWrap.appendChild(valSpan);
      row.appendChild(inp);
      row.appendChild(textWrap);
      lbl.appendChild(row);
      els.optionsBox.appendChild(lbl);
    }

    // Reset UI
    els.feedbackSec.classList.add('hidden');
    els.submitBtn.disabled = false;
    els.submitBtn.textContent = 'Submit';
    els.prevBtn.disabled = idx === 0;
    els.nextBtn.disabled = idx === activeQuestions.length - 1;

    // Restore state if answered
    if (progress[q.id]) {
      showFeedback(q, progress[q.id].selected);
    }
  }

  window.toggleOpt = (key, isMulti) => {
    const q = activeQuestions[currentIndex];
    if (!q || progress[q.id]) return; // locked if answered

    const targetLbl = document.getElementById(`lbl-${key}`);
    if (!isMulti) {
      currentSelection = [key];
      document.querySelectorAll('.option-btn').forEach(el => el.classList.remove('selected'));
      if (targetLbl) targetLbl.classList.add('selected');
    } else {
      const idx = currentSelection.indexOf(key);
      if (idx > -1) {
        currentSelection.splice(idx, 1);
        if (targetLbl) targetLbl.classList.remove('selected');
      } else {
        currentSelection.push(key);
        if (targetLbl) targetLbl.classList.add('selected');
      }
    }
  };

  els.submitBtn.addEventListener('click', () => {
    const q = activeQuestions[currentIndex];
    if (!q || progress[q.id] || currentSelection.length === 0) return;

    currentSelection.sort();
    const finalKey = q.notebook_correct_option || q.correct_option;
    const isCorrect = optsEqual(currentSelection, finalKey);

    progress[q.id] = { selected: [...currentSelection], isCorrect };
    try {
      localStorage.setItem('pmleProgress', JSON.stringify(progress));
    } catch (_) {}

    renderQuickFilters();
    renderSections();
    renderTopics();
    updateStats();
    renderGrid();
    showFeedback(q, currentSelection);
  });

  function showFeedback(q, selected) {
    els.submitBtn.disabled = true;
    els.submitBtn.textContent = 'Submitted';

    // Disable inputs once submitted
    document.querySelectorAll('.option-btn input').forEach(inp => { inp.disabled = true; });

    const notebookOpts = q.notebook_correct_option || q.correct_option;
    const correctOpts = notebookOpts; // Grounded Notebook answer is the authoritative final truth
    const geminiOpts = q.gemini_correct_option || correctOpts;
    const communityOpts = q.community_option || correctOpts;
    const isCorrect = optsEqual(selected, correctOpts);

    // Highlight correct & wrong
    for (const [key] of Object.entries(q.options)) {
      const lbl = document.getElementById(`lbl-${key}`);
      if (!lbl) continue;
      const inp = lbl.querySelector('input');

      if (inp && selected.includes(key)) inp.checked = true;

      if (correctOpts.includes(key)) {
        lbl.classList.add('correct-show');
      } else if (selected.includes(key) && !correctOpts.includes(key)) {
        lbl.classList.add('wrong-show');
      }
    }

    // Alert Banner
    els.feedbackAlert.className = `p-4 rounded-lg font-bold border ${isCorrect ? 'bg-green-100 text-green-800 border-green-300 dark:bg-green-900/30 dark:text-green-400 dark:border-green-800' : 'bg-red-100 text-red-800 border-red-300 dark:bg-red-900/30 dark:text-red-400 dark:border-red-800'}`;
    els.feedbackAlert.textContent = isCorrect
      ? `✓ Correct Answer! (Matches Grounded Notebook Key: ${correctOpts.join(', ')})`
      : `✗ Incorrect (Grounded Notebook Final Key: ${correctOpts.join(', ')})`;

    // 1. Notebook Grounded Card (Final Key)
    const nbBadge = document.getElementById('notebook-answer-badge');
    const nbSourceEl = document.getElementById('notebook-source-ref');
    const nbRationaleEl = document.getElementById('notebook-rationale');

    if (nbBadge) {
      const diffGem = !optsEqual(notebookOpts, geminiOpts);
      const diffComm = !optsEqual(notebookOpts, communityOpts);
      if (diffGem && diffComm) {
        nbBadge.className = 'self-start mb-2 px-3 py-1 bg-amber-600 text-white text-xs font-bold rounded shadow-sm';
        nbBadge.textContent = `Grounded Key: ${notebookOpts.join(', ')} (Overrides Gemini: ${geminiOpts.join(', ')} & Community: ${communityOpts.join(', ')})`;
      } else if (diffGem) {
        nbBadge.className = 'self-start mb-2 px-3 py-1 bg-amber-600 text-white text-xs font-bold rounded shadow-sm';
        nbBadge.textContent = `Grounded Key: ${notebookOpts.join(', ')} (Overrides Gemini: ${geminiOpts.join(', ')})`;
      } else if (diffComm) {
        nbBadge.className = 'self-start mb-2 px-3 py-1 bg-teal-600 text-white text-xs font-bold rounded shadow-sm';
        nbBadge.textContent = `Grounded Key: ${notebookOpts.join(', ')} (Overrides Community: ${communityOpts.join(', ')})`;
      } else {
        nbBadge.className = 'self-start mb-2 px-3 py-1 bg-emerald-600 text-white text-xs font-bold rounded';
        nbBadge.textContent = `Grounded Key: ${notebookOpts.join(', ')} (All 3 Agree ✓)`;
      }
    }
    if (nbSourceEl) {
      nbSourceEl.textContent = `📚 Source: ${q.notebook_source_ref || 'Official Google Cloud AI/ML Docs & PMLE Study Guide'}`;
    }
    if (nbRationaleEl) {
      nbRationaleEl.textContent = q.notebook_rationale || q.gemini_rationale || 'Grounded verification rationale unavailable.';
    }

    // 2. Gemini Card
    const geminiRationaleEl = document.getElementById('gemini-rationale');
    const geminiBadge = document.getElementById('gemini-answer-badge');
    if (geminiBadge) {
      if (!optsEqual(geminiOpts, notebookOpts)) {
        geminiBadge.className = 'self-start mb-3 px-3 py-1 bg-rose-600 text-white text-xs font-bold rounded';
        geminiBadge.textContent = `Gemini Picked: ${geminiOpts.join(', ')} (≠ Notebook: ${notebookOpts.join(', ')})`;
      } else if (!optsEqual(geminiOpts, communityOpts)) {
        geminiBadge.className = 'self-start mb-3 px-3 py-1 bg-indigo-600 text-white text-xs font-bold rounded';
        geminiBadge.textContent = `Gemini Answer: ${geminiOpts.join(', ')} (✓ Matches Notebook • ≠ Community: ${communityOpts.join(', ')})`;
      } else {
        geminiBadge.className = 'self-start mb-3 px-3 py-1 bg-indigo-600 text-white text-xs font-bold rounded';
        geminiBadge.textContent = `Gemini Answer: ${geminiOpts.join(', ')} (✓ Matches Notebook)`;
      }
    }
    if (geminiRationaleEl) {
      geminiRationaleEl.textContent = q.gemini_rationale || 'Validation pending or failed.';
    }

    // 3. Community Card
    const commBadge = document.getElementById('community-answer-badge');
    if (commBadge) {
      if (!optsEqual(communityOpts, notebookOpts)) {
        commBadge.className = 'self-start mb-3 px-3 py-1 bg-amber-600 text-white text-xs font-bold rounded';
        commBadge.textContent = `Voted Answer: ${communityOpts.join(', ')} (≠ Notebook: ${notebookOpts.join(', ')})`;
      } else {
        commBadge.className = 'self-start mb-3 px-3 py-1 bg-slate-600 text-white text-xs font-bold rounded';
        commBadge.textContent = `Voted Answer: ${communityOpts.join(', ')}`;
      }
    }
    els.discList.replaceChildren();
    if (Array.isArray(q.discussion) && q.discussion.length > 0) {
      q.discussion.forEach(d => {
        const li = document.createElement('li');
        li.textContent = `• ${d}`;
        els.discList.appendChild(li);
      });
    } else {
      const li = document.createElement('li');
      li.className = 'text-slate-500 italic';
      li.textContent = 'No discussion notes available.';
      els.discList.appendChild(li);
    }

    els.feedbackSec.classList.remove('hidden');
  }

  // Navigation
  els.prevBtn.addEventListener('click', () => { if (currentIndex > 0) window.goToQuestion(currentIndex - 1); });
  els.nextBtn.addEventListener('click', () => { if (currentIndex < activeQuestions.length - 1) window.goToQuestion(currentIndex + 1); });

  els.flagBtn.addEventListener('click', () => {
    const q = activeQuestions[currentIndex];
    if (!q) return;
    const fIdx = flags.indexOf(q.id);
    if (fIdx > -1) flags.splice(fIdx, 1);
    else flags.push(q.id);

    try {
      localStorage.setItem('pmleFlags', JSON.stringify(flags));
    } catch (_) {}
    els.flagBtn.style.opacity = flags.includes(q.id) ? '1' : '0.3';
    renderQuickFilters();
    renderSections();
    renderTopics();
    renderGrid();
  });

  // Non-blocking two-step reset confirmation (avoids native blocking confirm() dialog)
  els.resetBtn.addEventListener('click', () => {
    if (!els.resetBtn.dataset.confirming) {
      els.resetBtn.dataset.confirming = 'true';
      els.resetBtn.textContent = '⚠️ Click Again to Confirm Reset';
      if (resetPendingTimer) clearTimeout(resetPendingTimer);
      resetPendingTimer = setTimeout(() => {
        delete els.resetBtn.dataset.confirming;
        els.resetBtn.textContent = '🗑️ Reset Practice';
      }, 4000);
      return;
    }
    if (resetPendingTimer) clearTimeout(resetPendingTimer);
    delete els.resetBtn.dataset.confirming;
    els.resetBtn.textContent = '🗑️ Reset Practice';
    progress = {};
    flags = [];
    try {
      localStorage.removeItem('pmleProgress');
      localStorage.removeItem('pmleFlags');
    } catch (_) {}
    refreshAllViews(true);
  });

  els.shuffleBtn.addEventListener('click', () => {
    // Fisher-Yates shuffle on activeQuestions
    for (let i = activeQuestions.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [activeQuestions[i], activeQuestions[j]] = [activeQuestions[j], activeQuestions[i]];
    }
    currentIndex = 0;
    renderGrid();
    loadQuestion(0);
  });
});
