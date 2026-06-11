# AdSense Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve AI ToolNav's AdSense re-review readiness by fixing sitewide metadata, ad-script coverage, crawl signals, and thin-page indexing.

**Architecture:** Keep the site static and avoid broad visual redesign. Centralize future-proof fixes in generation scripts where possible, then apply mechanical rewrites to existing generated HTML so the live site matches the intended policy immediately.

**Tech Stack:** Static HTML, CSS, PowerShell audit script, Python generation scripts.

---

### Task 1: Add AdSense Audit Baseline

**Files:**
- Create: `scripts/audit_adsense.ps1`

- [ ] Create an audit script that scans all HTML files except templates.
- [ ] Report indexed pages missing AdSense scripts.
- [ ] Report indexed pages missing canonical URLs.
- [ ] Report indexed pages still using non-www canonical URLs.
- [ ] Report indexed pages with very short body text.
- [ ] Report whether the home page still contains the splash overlay.

### Task 2: Fix Generation Sources

**Files:**
- Modify: `scripts/build.py`
- Modify: `scripts/generate.py`
- Modify: `template/article.html`

- [ ] Change canonical domain constants to `https://www.aitnav.com`.
- [ ] Make generation scripts write to the project root, not the `scripts` directory.
- [ ] Add AdSense and analytics snippets to generated tool, category, and tool index pages.
- [ ] Generate `noindex, follow` for thin generated tool pages outside the five core indexed tools.
- [ ] Keep category pages, tool index, articles, and five core tool pages indexable.

### Task 3: Fix Existing Static HTML

**Files:**
- Modify: `index.html`
- Modify: `robots.txt`
- Modify: `sitemap.xml`
- Modify: generated and manual HTML pages under `articles/`, `categories/`, `compare/`, `reports/`, `tools/`, and `workflows/`

- [ ] Remove the home page splash markup and splash-only JavaScript.
- [ ] Replace `https://aitnav.com` with `https://www.aitnav.com` in metadata, sitemap, robots, Open Graph, and structured data.
- [ ] Insert AdSense script into pages that should keep indexability.
- [ ] Add canonical tags to manual pages that do not have them.
- [ ] Apply `noindex, follow` to thin temporary pages.
- [ ] Remove noindexed pages from `sitemap.xml`.

### Task 4: Verify

**Files:**
- Run: `scripts/audit_adsense.ps1`

- [ ] Run the audit and confirm there are no indexed pages missing AdSense scripts.
- [ ] Confirm indexed pages use `https://www.aitnav.com` canonical URLs.
- [ ] Confirm thin pages are noindexed or removed from the sitemap.
- [ ] Start a local static server and request the home page.
- [ ] Check Git diff before reporting.
