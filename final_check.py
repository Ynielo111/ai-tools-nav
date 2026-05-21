#!/usr/bin/env python3
"""All Pages Quality Check"""
import os, json

errors = []

# 1. Check data files
for f in ['data/tools.json', 'data/articles.json']:
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            json.load(fh)
    except Exception as e:
        errors.append(f'{f}: {e}')

# 2. Check all HTML pages
html_files = ['index.html', 'privacy.html', 'about.html', 'terms.html']
for d in ['articles', 'compare']:
    for fn in os.listdir(d):
        if fn.endswith('.html'):
            html_files.append(os.path.join(d, fn))

required_meta = [
    '<meta charset="UTF-8">',
    '<meta name="viewport"',
    'google-site-verification',
    'adsbygoogle.js?client=ca-pub-6233913596766498',
]
required_links = ['/privacy.html', '/about.html']

for fp in html_files:
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()

    # Structure checks
    if not html.startswith('<!DOCTYPE html>'):
        errors.append(f'{fp}: missing DOCTYPE')
    if '</html>' not in html:
        errors.append(f'{fp}: missing closing html')
    if '<head>' not in html or '</head>' not in html:
        errors.append(f'{fp}: head tag issue')
    if '</body>' not in html:
        errors.append(f'{fp}: missing closing body')

    for meta in required_meta:
        if meta not in html:
            errors.append(f'{fp}: missing {meta[:50]}...')

    # Check for leftover placeholders
    if '{{' in html:
        for line in html.split('\n'):
            if '{{' in line:
                errors.append(f'{fp}: unrendered placeholder: {line.strip()[:80]}')

    # Check for broken links (only internal .html links)
    import re
    links = re.findall(r'href="(/[^"]+\.html)"', html)
    for link in links:
        target = os.path.join(os.path.dirname(fp), link.lstrip('/'))
        if not os.path.exists(target) and not os.path.exists(link.lstrip('/')):
            # Try base dir
            base = link.lstrip('/')
            if not os.path.exists(base):
                errors.append(f'{fp}: broken link -> {link}')

# 3. Check sitemap and robots
for f in ['sitemap.xml', 'robots.txt']:
    if not os.path.exists(f):
        errors.append(f'{f}: missing')

# 4. Count articles
article_count = len([f for f in os.listdir('articles') if f.endswith('.html') and f != 'index.html'])

if errors:
    print(f'[ERRORS] {len(errors)} issues:')
    for e in errors:
        print(f'  - {e}')
else:
    print(f'[PASS] All checks passed! {article_count} articles, {len(html_files)} total pages')

# 5. Content quality check - article sizes
import os
sizes = {}
for f in os.listdir('articles'):
    if f.endswith('.html') and f != 'index.html':
        p = os.path.join('articles', f)
        sizes[f] = os.path.getsize(p)
print(f'  Article size: {min(sizes.values())/1024:.0f}-{max(sizes.values())/1024:.0f}KB (avg {sum(sizes.values())/len(sizes)/1024:.0f}KB)')
