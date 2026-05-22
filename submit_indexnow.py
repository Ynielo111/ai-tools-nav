#!/usr/bin/env python3
"""提交所有URL到 IndexNow (Bing/Yandex) — 每次部署后运行"""
import json, urllib.request, urllib.error

KEY = 'aitnav-indexnow-2026-58articles'
HOST = 'aitnav.com'

with open('data/articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

urls = [f'https://{HOST}/', f'https://{HOST}/articles/', f'https://{HOST}/compare/']
for a in articles:
    urls.append(f'https://{HOST}/articles/{a["id"]}.html')

print(f'Submitting {len(urls)} URLs...')
payload = json.dumps({
    'host': HOST,
    'key': KEY,
    'keyLocation': f'https://{HOST}/aitnav-indexnow-2026-58articles.txt',
    'urlList': urls
}).encode('utf-8')

try:
    req = urllib.request.Request('https://api.indexnow.org/indexnow', data=payload,
        headers={'Content-Type': 'application/json; charset=utf-8'})
    resp = urllib.request.urlopen(req, timeout=30)
    print(f'IndexNow: HTTP {resp.status}')
except urllib.error.HTTPError as e:
    print(f'Failed: HTTP {e.code} - {e.read().decode()[:200]}')
