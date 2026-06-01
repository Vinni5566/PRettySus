<div align="center">

# 🕵️‍♂️ PRettySus

**Deterministic PR Communication Quality & Repository Memory Analyzer**

*Stop asking "Is this AI-generated?" Start asking "Does this preserve our repository's memory?"*

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?style=flat-square&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat-square&logo=vite)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat-square&logo=typescript)
![Tests](https://img.shields.io/badge/Tests-8%20passing-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

</div>

---

## 📖 Table of Contents

1. [The Problem](#-the-problem-squash-and-merge-amnesia)
2. [The Solution](#-the-solution-repository-memory-integrity)
3. [Key Features](#-key-features)
4. [Architecture](#-architecture-100-ai-free)
5. [Project Structure](#-project-structure)
6. [Requirements](#-requirements)
7. [Installation & Setup](#-installation--setup)
8. [Running the App](#-running-the-app)
9. [Using the Dashboard](#-using-the-dashboard)
10. [CLI Usage](#-cli-usage)
11. [GitHub Actions CI/CD](#-github-actions-cicd)
12. [Running Tests](#-running-tests)
13. [Available Make Commands](#-available-make-commands)
14. [API Reference](#-api-reference)
15. [Scoring Explained](#-scoring-explained)
16. [Limitations & Design Choices](#-limitations--design-choices)
17. [Future Roadmap](#-future-roadmap)

---

## 🔥 The Problem: Squash-and-Merge Amnesia

When engineers use AI to write code, they often submit lazy, generic Pull Request descriptions (e.g., `"update things"`, `"fixed logic"`). Over time, this causes **Squash-and-Merge Amnesia** — the core engineering context, the *why* and the *how*, is **lost forever**.

Existing tools try to detect "AI-generated" text with LLMs. This is fundamentally flawed:
- ❌ Slow and expensive
- ❌ Sends private code to third parties
- ❌ Constant false positives

---

## 💡 The Solution: Repository Memory Integrity

**PRettySus is a 100% deterministic, AI-free static analysis tool for engineering communication.**

Instead of guessing if text is AI-generated, PRettySus measures **Communication Coverage**. It parses the raw Git diff to extract the high-impact code entities modified (e.g., `jwt_manager`, `redis_cache`), and mathematically verifies that the PR description and commit messages actually mention them.

> If you write 400 lines of complex authentication code but your PR description is "fixes auth", PRettySus will **fail your CI/CD pipeline**.

---

## 🚀 Key Features

| Feature | Description |
|:--------|:------------|
| 🎯 **Communication Coverage Map** | Treats English text like code coverage. Extracts code entities from diffs and ensures high-impact files (security, DB, auth) are explicitly explained |
| 🛡️ **Main Branch Sentry** | Prevents noisy, generic PRs from being squash-merged into the main branch history |
| 📊 **Squash Risk Analyzer** | Detects duplicate commits, generic phrasing, and calculates a "Squash Noise Score" |
| 🔍 **Buried Signal Detection** | Finds the single high-value commit hidden underneath 20 generic "fix logic" micro-commits |
| ⚙️ **Deterministic Summary Generator** | Synthesizes a copyable, context-rich PR summary from diff analysis — **zero LLM calls** |
| 🚨 **Critical Policy Gates** | Automatically fails PRs that touch `migration` or `auth` files without high-signal keywords |
| 📊 **Visual Dashboard** | React + Tailwind UI for exploring results interactively |
| 🤖 **GitHub Actions Integration** | Plug-and-play CI/CD gatekeeper workflow |

---

## 🧠 Architecture: 100% AI-Free

```
[ Git Diff ] + [ PR Description ] + [ Commits List ]
      │                │                    │
      ▼                ▼                    ▼
[ Tokenizer ]   [ Entity Extractor ]  [ Cluster Analyzer ]
      │                │                    │
      ├────────────────┼────────────────────┤
      ▼                ▼                    ▼
[ Coverage Map ] [ Policy Checker ]  [ Squash Sentry ]
      │                │                    │
      └────────────────┼────────────────────┘
                       ▼
         [ Repository Memory Integrity Score ]
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
  [ Web Dashboard ]            [ CLI / GitHub Action ]
```

**Backend Modules:**
- `app/parsers/` — Git diff tokenizer and entity extractor
- `app/analyzers/` — Coverage map builder and squash commit cluster analyzer
- `app/scoring/` — Deterministic score calculator
- `app/services/` — Orchestration layer, report generator, sentry service
- `app/api/` — FastAPI REST endpoints
- `app/cli.py` — Headless CLI entrypoint

---

## 📁 Project Structure

```
PRettySus/
│
├── backend/                        ← Python FastAPI static analysis engine
│   ├── app/
│   │   ├── analyzers/              ← Coverage map, squash analyzer
│   │   ├── api/                    ← FastAPI route definitions
│   │   ├── models/                 ← Pydantic request/response schemas
│   │   ├── parsers/                ← Git diff parser & entity extractor
│   │   ├── scoring/                ← Score calculator
│   │   ├── services/               ← Main orchestration logic
│   │   └── utils/                  ← Text utilities
│   ├── tests/                      ← Deterministic pytest test suite
│   ├── samples/                    ← Sample PR payloads for testing
│   ├── main.py                     ← FastAPI app entrypoint
│   └── requirements.txt            ← Python dependencies
│
├── frontend/                       ← React + TypeScript + Tailwind dashboard
│   ├── src/
│   │   ├── components/             ← InputForm, ScoreCard components
│   │   ├── pages/                  ← Dashboard page
│   │   ├── services/               ← API client (fetch wrapper)
│   │   ├── types/                  ← TypeScript type definitions
│   │   └── main.tsx                ← React app entrypoint
│   ├── index.html
│   ├── vite.config.ts
│   └── package.json
│
├── .github/
│   └── workflows/
│       └── prettysus.yml           ← GitHub Actions CI/CD workflow
│
├── docs/                           ← Additional documentation
├── scripts/                        ← GitHub Action runner utilities
├── action.yml                      ← GitHub Action definition
├── Makefile                        ← Convenience commands
└── README.md
```

---

## ✅ Requirements

Before you start, make sure you have these installed:

| Tool | Minimum Version | Check Command |
|:-----|:----------------|:--------------|
| **Python** | 3.10+ | `python --version` |
| **pip** | Latest | `pip --version` |
| **Node.js** | 18+ | `node --version` |
| **npm** | 9+ | `npm --version` |
| **Git** | Any | `git --version` |

---

## ⚙️ Installation & Setup

### Step 1 — Clone the repository

```bash
git clone https://github.com/Vinni5566/PRettySus.git
cd PRettySus
```

### Step 2 — Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

This installs:
- `FastAPI` — the web framework for the analysis API
- `uvicorn` — the ASGI server to run FastAPI
- `pydantic` — data validation and schema models
- `pytest` — the test runner

### Step 3 — Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

> **Note:** `node_modules/` is excluded from git. You must run `npm install` locally after cloning.

### Step 4 — (Optional) Configure environment

```bash
# Backend — copy and edit if needed (no required values by default)
cp backend/.env.example backend/.env

# Frontend — copy and edit the API base URL if backend runs on a different port
cp frontend/.env.example frontend/.env
```

---

## 🚀 Running the App

You need **two terminal windows** — one for the backend, one for the frontend.

### Terminal 1 — Start the Backend (FastAPI)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Terminal 2 — Start the Frontend (Vite + React)

```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x  ready in 900ms
  ➜  Local:  http://localhost:5173/
```

> **Note:** If port 5173 is already in use, Vite will try 5174, 5175, etc. Look for the actual URL in the terminal output.

### Using Make (shortcut)

If you have `make` available, you can use these convenience commands instead:

```bash
make install    # Installs both backend and frontend dependencies
make backend    # Starts only the FastAPI backend
make frontend   # Starts only the Vite frontend
```

---

## 🖥️ Using the Dashboard

Once both servers are running, open your browser and go to:

```
http://localhost:5173
```

The dashboard is split into two panels:

**Left Panel — Input:**
- **PR Title** — The title of the pull request
- **PR Description** — The full PR body/description text
- **Commit Messages** — One commit message per line
- **Raw Git Diff** — Paste the output of `git diff` here
- **Proposed Squash Message** — Optional. Simulate a custom squash message

**Quick-Load Sample Buttons:**

| Button | Description |
|:-------|:------------|
| ✅ Good PR | A well-described PR that should pass all checks |
| 🐛 Bad Filler PR | Generic descriptions with no entity coverage |
| 💾 Risky Migration PR | Touches DB migrations without explanation |
| 🔀 Noisy Squash Merge | 15 commits with buried signal |
| ✅ Clean Squash Merge | 2 focused commits with clear context |

**Right Panel — Results:**
After clicking **Analyze PR**, you'll see:
- 📊 **Repository Memory Integrity Score** — Overall quality score
- 🛡️ **Main Branch Sentry** — Pass/Fail gate for main branch merges
- 🎯 **Communication Coverage %** — How many diff entities are explained
- 🔀 **Squash Merge Risk** — Noise score, duplicate/generic commit counts
- 🚨 **Policy Violations** — Critical failures (auth/migration gates)
- 🗂️ **Code Entity Coverage Map** — Which entities are covered vs. missing
- 📋 **Commit Quality** — Warnings about vague or duplicate commits
- 📈 **Scoring Breakdown** — Per-metric breakdown table

**Export Options:**
- **Copy Markdown** — Copies a formatted analysis report to clipboard
- **JSON** — Downloads the full raw result as a `.json` file

---

## 🖥️ CLI Usage

Run PRettySus headlessly without the dashboard (useful for scripts and local pre-commit hooks):

```bash
cd backend
python -m app.cli analyze \
  --title "Implement JWT authentication" \
  --description-file pr_body.md \
  --diff-file changes.patch \
  --commits-file commits.txt \
  --output report.json
```

**Arguments:**

| Argument | Required | Description |
|:---------|:---------|:------------|
| `--title` | ✅ Yes | PR title string |
| `--description-file` | ✅ Yes | Path to a `.md` or `.txt` file containing the PR description |
| `--diff-file` | ✅ Yes | Path to a `.patch` file (output of `git diff`) |
| `--commits-file` | ✅ Yes | Path to a `.txt` file with one commit message per line |
| `--output` | No | Path to write the JSON report (default: prints to stdout) |

**Exit Codes:**
- `0` — PR passed all policy checks
- `1` — PR failed one or more critical policy gates

---

## 🤖 GitHub Actions CI/CD

Automatically block bad PRs from merging. Add this workflow to your own repository:

**`.github/workflows/prettysus.yml`**
```yaml
name: PRettySus Communication Gatekeeper
on: [pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run PRettySus Analysis
        uses: Vinni5566/PRettySus@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

This will automatically:
1. Extract the PR title, description, and diff from the GitHub event
2. Run the full static analysis
3. **Fail the CI check** if any critical policy gates are triggered

---

## 🧪 Running Tests

All 8 tests are deterministic and run without any external API calls:

```bash
cd backend
pytest -v
```

Expected output:
```
tests/test_analyzer.py::test_analyzer_high_risk     PASSED
tests/test_analyzer.py::test_analyzer_low_risk      PASSED
tests/test_phase2.py::test_coverage_and_policies    PASSED
tests/test_phase3.py::test_noisy_squash_merge       PASSED
tests/test_phase3.py::test_clean_squash_merge       PASSED
tests/test_phase3.py::test_api_response_contract    PASSED
tests/test_phase4.py::test_markdown_report_generation PASSED
tests/test_phase4.py::test_report_endpoint          PASSED

============================== 8 passed in 0.99s ==============================
```

---

## 🛠️ Available Make Commands

| Command | Action |
|:--------|:-------|
| `make install` | Installs all Python + Node dependencies |
| `make backend` | Starts FastAPI server on `localhost:8000` |
| `make frontend` | Starts Vite dev server on `localhost:5173` |
| `make test` | Runs the full `pytest` test suite |
| `make demo` | Prints instructions for running both servers |

---

## 📡 API Reference

The backend exposes a REST API. Full interactive docs available at:

```
http://localhost:8000/docs
```

### `POST /api/analyze`

Analyze a PR and get the full Repository Memory Integrity report.

**Request Body:**
```json
{
  "title": "Implement JWT authentication",
  "description": "This PR adds JWT token validation and Redis session caching...",
  "commits": [
    "feat: add jwt token validation",
    "feat: implement redis caching layer"
  ],
  "diff": "+++ b/src/auth/jwt_manager.py\n+def validate_session(): ...",
  "proposedSquashMessage": "Optional custom squash message"
}
```

**Response:**
```json
{
  "score": 82,
  "riskLevel": "low",
  "communicationCoverage": {
    "weightedPercentage": 90,
    "coveredEntities": ["jwt_manager", "redis_cache"],
    "uncoveredEntities": [],
    "highImpactUncoveredEntities": []
  },
  "policyViolations": [],
  "commitWarnings": [],
  "duplicateCommitClusters": [],
  "scoringBreakdown": { ... },
  "mainBranchSentry": { ... },
  "squashAnalysis": { ... },
  "repositoryMemoryIntegrity": { ... }
}
```

### `POST /api/analyze/report`

Same as `/api/analyze` but returns a formatted **Markdown report** ready to paste into GitHub.

**Response:**
```json
{
  "markdown": "## PRettySus Analysis Report\n..."
}
```

### `GET /health`

Health check endpoint.

```json
{ "status": "ok" }
```

---

## 📏 Scoring Explained

The **Repository Memory Integrity Score** (0–100) is calculated deterministically from four weighted dimensions:

| Dimension | Weight | What It Measures |
|:----------|:------:|:-----------------|
| **Communication Coverage** | 40% | What % of code entities from the diff are mentioned in the description |
| **Commit Quality** | 30% | Are commits specific, unique, and signal-rich? |
| **Squash Readiness** | 20% | Is the PR safe to squash-merge without losing history? |
| **Policy Compliance** | 10% | Are critical files (auth, migrations) explicitly documented? |

**Risk Levels:**

| Score | Risk Level | Meaning |
|:-----:|:----------:|:--------|
| 80–100 | 🟢 Low | Safe to merge — excellent communication |
| 60–79 | 🟡 Medium | Some improvement needed |
| 40–59 | 🟠 High | Significant communication gaps |
| 0–39 | 🔴 Critical | Blocked — policy violations or near-zero coverage |

---

## ⚠️ Limitations & Design Choices

PRettySus uses strict **word-boundary matching**, which means:

- Developers must use the **exact terms** found in the codebase inside their PR descriptions
- If code has `user_auth_service` but the description says "login service", it will flag it as **uncovered**
- This is **intentional** — it forces engineers to write searchable, precise documentation that maps directly back to the code artifacts

---

## 🔮 Future Roadmap

- 🤖 **GitHub App Integration** — Native PR commenting with inline suggestions
- 📜 **Historical Repo Scanning** — Retroactively grade historical commits and identify amnesia hotspots
- 🔔 **Slack/Teams Notifications** — Alert teams when PRs with critical policy failures are opened
- 📊 **Trends Dashboard** — Track repo communication quality over time

---

<div align="center">
  <i>Built with React, TypeScript, Tailwind CSS, FastAPI, and strict software engineering principles.</i>
  <br/>
  <i>Zero LLM calls. 100% deterministic. Fully open source.</i>
</div>