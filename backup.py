#!/usr/bin/env python3
"""存档当前数据——每次更新前运行一次"""
import os, shutil, json
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ts = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_dir = os.path.join(BASE, 'backups', ts)
os.makedirs(backup_dir, exist_ok=True)

# 复制数据文件
src_files = ['data/tools.json', 'data/articles.json', 'build.py',
             'template/article.html', 'index.html', 'about.html',
             'privacy.html', 'terms.html']
for f in src_files:
    src = os.path.join(BASE, f)
    if os.path.exists(src):
        dst = os.path.join(backup_dir, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

# 记录元信息
with open('data/articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

meta = {
    'backup_time': ts,
    'total_articles': len(articles),
    'types': {
        t: sum(1 for a in articles if a['type'] == t)
        for t in ['comparison', 'recommendation', 'pricing']
    }
}
with open(os.path.join(backup_dir, 'meta.json'), 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print(f'存档完成: backups/{ts}')
print(f'  文章: {meta["total_articles"]} 篇')
print(f'  对比: {meta["types"]["comparison"]} / 推荐: {meta["types"]["recommendation"]} / 价格: {meta["types"]["pricing"]}')
