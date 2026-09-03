# Google PMLE Practice Application & Grounded Study Suite

This is a standalone, local web application and rapid-revision suite for the **Google Professional Machine Learning Engineer (PMLE)** certification exam. All **375 exam questions** and **4 HTML study guides** are verified against the authoritative **Grounded Notebook sources** (June 2026 PMLE Exam Guide, PMLE Learning Path Study Guide v2.0, Google ML Glossary, ML Crash Course, and Official Google Cloud AI/ML Documentation).

## Features
- **All 375 Audited Questions:** Complete dataset including single-choice, multi-select, and architectural diagram questions, graded strictly by the **📓 Notebook Grounded Final Key**.
- **Grounded Notebook Truth (3-Way Comparison):** Every question displays a side-by-side comparison of **📓 Notebook Grounded (Final Key)** (with authoritative document citations & distractor eliminations), **✨ Gemini's Answer**, and **👥 Community Discussion** — highlighting all **42 Grounded Overrides** (`23 NB ≠ Gemini`, `32 NB ≠ Vote`).
- **Layered Filtering:** Combine **Your Progress** scope filters (`All (375)`, `Q#200–375 (176)`, `📓 NB Overrides (42)`, `⚡ NB ≠ Gemini (23)`, `👥 NB ≠ Vote (32)`, `✨ Notes (65)`, `🚩 Flagged`, `✗ Wrong`) with the **6 Official Exam Sections** and **Technical Topics**.
- **4 Interactive HTML Study Guides (Cross-Linked in Header & Offline-Ready):**
  1. `PMLE_Reliable_Patterns.html` — *The 10 Most Reliable Exam Patterns & 8 Official GCP Platform-Limit Red Flags*
  2. `PMLE_Patterns_and_Core_Concepts_Guide.html` — *4 Visual Decision Flowcharts, Skew/Drift/XAI/DLP/MinDiff Matrices & Q#22 Tensor Shape Verification*
  3. `PMLE_Rapid_Revision_Cheat_Sheet.html` — *2-Day Sprint Cheat Sheet, Hard GCP Quotas & All 65 Grounded Override/Curated Rules*
  4. `PMLE_Q200_to_375_Rapid_Revision.html` — *Q#200–375 Trigger Keywords, Winning Solutions & 3-Distractor Elimination Matrix*
- **Bundled Authoritative Source PDFs:** Includes `Professional Machine Learning Engineer Exam Guide _ English new - Google Docs.pdf` (June 2026 Guide) and `PMLE Learning Path.pdf` (PMLE Study Guide v2.0).
- **Offline Progress Tracking:** Automatically saves attempted questions, accuracy, and flagged items in browser `localStorage` with Dark/Light mode support.

## How to Run the App Locally

Because this application fetches the questions dynamically from the `questions.json` file, modern browsers will block it if you try to double-click `index.html` directly (due to CORS security policies). *(Note: The 4 HTML study guides can be opened either via the local server below or directly in any browser.)*

To run it, you simply need to start a local HTTP server in this directory.

### Step 1: Open your Terminal / Command Prompt
Navigate to the extracted folder containing this README:
```bash
cd path/to/pmle-practice-app
```

### Step 2: Start a Local Server
If you have **Python** installed (which most Mac/Linux machines do by default), run:
```bash
python3 -m http.server 8000
# (or `python -m http.server 8000` on Windows)
```

If you have **Node.js/npm** installed, you can use:
```bash
npx serve
# or
npx http-server
```

### Step 3: Open in Browser
Open your favorite web browser and navigate to:
[http://localhost:8000](http://localhost:8000)

## Resetting Progress
Your progress is saved in the browser. You can clear it anytime by clicking the **Reset Practice** button twice in the top right corner of the app, or by clearing your browser's local storage.
