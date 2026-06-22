# AdSense Low Value Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce Google AdSense "low value content" signals by exposing fewer, stronger pages during review and adding a repeatable local audit.

**Architecture:** Keep the static site architecture. Use `scripts/build.py` as the source of truth for review-indexed articles, update `scripts/audit_adsense.ps1` to match, add `scripts/audit_low_value.ps1` for low-value signals, and regenerate static HTML/sitemap from source data. Avoid visual redesign and broad unrelated content changes.

**Tech Stack:** Static HTML, Python page generator, PowerShell audit scripts, JSON article data.

---

### Task 1: Add Low-Value Audit

**Files:**
- Create: `scripts/audit_low_value.ps1`

- [ ] **Step 1: Write the failing audit**

Create a PowerShell audit that scans indexed HTML pages and fails when review pages contain common template phrases, have too little visible text, or omit an evidence/source note.

- [ ] **Step 2: Run audit and verify it fails**

Run: `& .\scripts\audit_low_value.ps1`

Expected before remediation: FAIL because several currently indexed review articles contain repeated template phrases and weak evidence signals.

### Task 2: Shrink Review Index Set

**Files:**
- Modify: `scripts/build.py`
- Modify: `scripts/audit_adsense.ps1`
- Modify: `AGENTS.md`

- [ ] **Step 1: Reduce `REVIEW_INDEXED_ARTICLE_IDS`**

Keep only the strongest review pages for AdSense re-review:

- `ai-cli-tools-setup-guide`
- `open-source-ai-coding-assistants`
- `codex-vs-claude-code-vs-gemini-cli`
- `academic-research-ai`
- `best-ai-coding-tools`
- `deepseek-complete-guide`
- `chatgpt-prompt-guide`

- [ ] **Step 2: Align AdSense audit allowlist**

Update `scripts/audit_adsense.ps1` so AdSense script expectations match the new review set.

- [ ] **Step 3: Update project notes**

Update `AGENTS.md` to document the 8-page review strategy and explain that previously indexed comparison pages are temporarily noindexed for quality improvement.

### Task 3: Rewrite Priority Generated Articles

**Files:**
- Modify: `data/articles.json`

- [ ] **Step 1: Rewrite `academic-research-ai`**

Replace generic recommendation sections with researcher-oriented workflow content, tool limitations, responsible academic use, and source/evidence notes.

- [ ] **Step 2: Rewrite `best-ai-coding-tools`**

Replace generic ranking language with developer task-based guidance, limitations, local verification advice, and source/evidence notes.

- [ ] **Step 3: Rewrite `deepseek-complete-guide`**

Add practical onboarding, use-case boundaries, API caution, verification advice, and source/evidence notes.

- [ ] **Step 4: Rewrite `chatgpt-prompt-guide`**

Add concrete prompt workflow examples, common failure modes, quality checklist, and source/evidence notes.

### Task 4: Regenerate and Verify

**Files:**
- Generated: `articles/*.html`
- Generated: `articles/index.html`
- Generated: `sitemap.xml`
- Modify as needed: `adsense_recheck_20260622/adsense_rejection_diagnosis.md`

- [ ] **Step 1: Regenerate static pages**

Run: `python scripts/build.py`

- [ ] **Step 2: Run technical audit**

Run: `& .\scripts\audit_adsense.ps1`

Expected: PASS.

- [ ] **Step 3: Run low-value audit**

Run: `& .\scripts\audit_low_value.ps1`

Expected: PASS after remediation.

- [ ] **Step 4: Record final remediation notes**

Update the rejection diagnosis report with the final review set and verification outputs.
