# Editorial Methodology Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one indexed trust page explaining AI ToolNav's review method, editorial principles, source checks, and correction process.

**Architecture:** Keep the site static. Add `methodology.html` as a hand-written trust page, include it in `scripts/build.py` sitemap output and `scripts/audit_adsense.ps1` indexed allowlist, then add footer links from trust pages.

**Tech Stack:** Static HTML, Python sitemap generator, PowerShell audits.

---

### Task 1: Add Trust Page

**Files:**
- Create: `methodology.html`
- Modify: `about.html`
- Modify: `privacy.html`
- Modify: `terms.html`

- [ ] Create an indexed `methodology.html` page with canonical URL, clear editorial method content, and >1000 visible characters.
- [ ] Add footer links to the methodology page from existing trust pages.

### Task 2: Add Sitemap and Audit Support

**Files:**
- Modify: `scripts/build.py`
- Modify: `scripts/audit_adsense.ps1`
- Generated: `sitemap.xml`

- [ ] Add `https://www.aitnav.com/methodology.html` to generated sitemap.
- [ ] Add `methodology.html` to the indexed allowlist in `scripts/audit_adsense.ps1`.
- [ ] Run `python scripts/build.py`.

### Task 3: Verify

**Files:**
- No additional edits expected.

- [ ] Run `scripts/audit_adsense.ps1`.
- [ ] Run `scripts/audit_low_value.ps1`.
- [ ] Confirm sitemap contains 13 URLs and includes `methodology.html`.

