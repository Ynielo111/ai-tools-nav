# AdSense Readiness Design

## Goal

Prepare AI ToolNav for a stronger Google AdSense re-review by fixing crawl, metadata, ad-script coverage, and thin-page indexing risks before expanding content.

## Current Findings

- The production site resolves to `https://www.aitnav.com`, but most canonical, sitemap, Open Graph, and structured-data URLs use `https://aitnav.com`.
- The home page uses a full-screen click-to-enter splash overlay that can block the first viewport for crawlers and users.
- Many indexable tool pages have very short body text. Only a small set of core tool pages currently has enough detail to keep indexed confidently.
- Several page groups do not include the AdSense review script.
- Some manually created tool, report, and workflow pages have no canonical URL.
- The generation scripts use the `scripts` directory as their output root, so future regeneration can write to the wrong location.

## Recommended Approach

Use a two-layer repair.

First, fix technical and review-signal consistency across the static site: remove the splash overlay, standardize on `https://www.aitnav.com`, add consistent AdSense scripts, add canonical tags, and keep sitemap/robots aligned.

Second, use a conservative indexing policy while the site is being improved. Keep the home page, article pages, article index, category pages, tool index, and sufficiently detailed core tool pages indexed. Mark thin tool pages, utility pages, reports, workflows, and the thin compare page as `noindex, follow` until they are expanded.

## Indexing Policy

Keep indexed:

- `/`
- `/articles/` and generated article pages
- `/categories/*.html`
- `/tools/`
- `/tools/chatgpt.html`
- `/tools/claude.html`
- `/tools/cursor.html`
- `/tools/midjourney.html`
- `/tools/deepseek.html`
- Legal/trust pages: `/about.html`, `/privacy.html`, `/terms.html`

Temporarily noindex:

- Generated tool detail pages outside the five core pages
- Utility mini tools with very little explanatory content
- `reports/`
- `workflows/`
- `/compare/`

## Verification

Add and use `scripts/audit_adsense.ps1` to check:

- No indexed HTML page is missing the AdSense script.
- No indexed HTML page is missing a canonical URL.
- Indexed canonical URLs use `https://www.aitnav.com`.
- Thin pages are not left as `index, follow`.
- The home page no longer contains the blocking splash markup.
- `robots.txt` and `sitemap.xml` reference `https://www.aitnav.com`.
