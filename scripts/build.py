#!/usr/bin/env python3
"""AI ToolNav 静态页面生成器 — 从 JSON 数据 + HTML 模板批量生成文章页面"""
import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
DOMAIN = "https://www.aitnav.com"
ADSENSE_SNIPPET = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6233913596766498" crossorigin="anonymous"></script>'
REVIEW_INDEXED_ARTICLE_IDS = {
    "ai-cli-tools-setup-guide",
    "open-source-ai-coding-assistants",
    "codex-vs-claude-code-vs-gemini-cli",
    "chatgpt-prompt-guide",
    "deepseek-complete-guide",
    "best-ai-coding-tools",
    "academic-research-ai",
}
EXTRA_REVIEW_ARTICLES = [
    {
        "id": "codex-vs-claude-code-vs-gemini-cli",
        "title": "Codex vs Claude Code vs Gemini CLI：三大AI编程命令行工具深度对比 2026",
        "type": "comparison",
        "reading_time": "10分钟",
        "published": "2026-05-16",
    },
    {
        "id": "open-source-ai-coding-assistants",
        "title": "开源AI编程助手推荐：OpenClaw、OpenCode、Hermes Agent 完全指南 2026",
        "type": "recommendation",
        "reading_time": "9分钟",
        "published": "2026-05-16",
    },
]
STATIC_REVIEW_ARTICLE_IDS = {
    "ai-cli-tools-setup-guide",
}

def load_json(path):
    with open(os.path.join(BASE, path), 'r', encoding='utf-8') as f:
        return json.load(f)

def read_template(path):
    with open(os.path.join(BASE, path), 'r', encoding='utf-8') as f:
        return f.read()

def write_html(path, html):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(html)

def type_label(t):
    return {"comparison": "横向对比", "recommendation": "场景推荐", "pricing": "价格指南"}.get(t, t)

def build_toc(toc_items):
    return ''.join(f'<li><a href="#sec{i+1}">{h}</a></li>' for i, h in enumerate(toc_items))

def build_tool_card(tool):
    stars = '⭐' * tool['rating']
    return (
        f'<a href="{tool["url"]}" target="_blank" rel="noopener" class="tool-card-inline">'
        f'<span class="tci-icon">{tool["icon"]}</span>'
        f'<span class="tci-name">{tool["name"]}</span>'
        f'<span class="tci-rating">{stars}</span>'
        f'</a>'
    )

def build_comparison_table(table_data, tools_map):
    if not table_data:
        return ''
    dims = table_data.get('dimensions', [])
    rows = table_data.get('rows', [])
    if not dims or not rows:
        return ''
    th = '<th></th>' + ''.join(f'<th>{d}</th>' for d in dims)
    trs = ''
    for row in rows:
        tds = f'<td>{row["label"]}</td>'
        for v in row.get('values', []):
            tds += f'<td>{v}</td>'
        trs += f'<tr>{tds}</tr>'
    return f'<div class="compare-table-wrap"><table class="compare-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'

def build_pros_cons(tool_ids, tools_map):
    cards = ''
    for tid in tool_ids:
        tool = tools_map.get(tid)
        if not tool:
            continue
        pros = ''.join(f'<li style="color:#10b981;">✅ {p}</li>' for p in tool.get('pros', []))
        cons = ''.join(f'<li style="color:#ef4444;">❌ {c}</li>' for c in tool.get('cons', []))
        cards += (
            f'<div class="pc-card">'
            f'<div class="pc-tool-name">{tool["icon"]} {tool["name"]} {"⭐"*tool["rating"]}</div>'
            f'<ul>{pros}{cons}</ul>'
            f'</div>'
        )
    return f'<div class="pros-cons">{cards}</div>' if cards else ''

def build_related(related_ids, articles_map, tools_map):
    cards = ''
    for rid in related_ids:
        a = articles_map.get(rid)
        if not a:
            continue
        cards += (
            f'<a href="/articles/{rid}.html" class="ra-card">'
            f'<div class="ra-title">{a["title"]}</div>'
            f'<div class="ra-type">{type_label(a["type"])} · {a.get("reading_time","")}</div>'
            f'</a>'
        )
    return cards

def render_article(article, tools_map, articles_map):
    template = read_template('template/article.html')

    # Build content HTML
    content_parts = []
    for i, sec in enumerate(article.get('sections', [])):
        anchor = f'id="sec{i+1}"'
        content_parts.append(f'<h2 {anchor}>{sec["heading"]}</h2>')
        content_parts.append(sec.get('content', ''))

        # Tool cards in section
        tool_cards = sec.get('tool_cards', [])
        if tool_cards:
            cards_html = ''.join(build_tool_card(tools_map[tid]) for tid in tool_cards if tid in tools_map)
            content_parts.append(f'<p>{cards_html}</p>')

        # Comparison table in section
        if sec.get('comparison_table'):
            content_parts.append(build_comparison_table(sec['comparison_table'], tools_map))

        # Pros/cons in section
        if sec.get('pros_cons'):
            content_parts.append(build_pros_cons(sec['pros_cons'], tools_map))

    content_html = '\n'.join(content_parts)

    # Replacements
    title = article['title']
    tid = article['id']
    is_review_indexed = tid in REVIEW_INDEXED_ARTICLE_IDS
    replacements = {
        '{{TITLE}}': title,
        '{{ID}}': tid,
        '{{META_DESC}}': article.get('meta_description', title),
        '{{KEYWORDS}}': ', '.join(article.get('keywords', [])),
        '{{PUBLISHED}}': article.get('published', '2026-05-21'),
        '{{READING_TIME}}': article.get('reading_time', '5分钟'),
        '{{TYPE}}': article.get('type', 'recommendation'),
        '{{TYPE_LABEL}}': type_label(article.get('type', 'recommendation')),
        '{{SUMMARY}}': article.get('summary', ''),
        '{{TOC}}': build_toc(article.get('toc', [])),
        '{{CONTENT}}': content_html,
        '{{RELATED}}': build_related(article.get('related', []), articles_map, tools_map),
        '{{ADSENSE_SNIPPET}}': ADSENSE_SNIPPET if is_review_indexed else '',
        '{{ROBOTS}}': 'index, follow' if is_review_indexed else 'noindex, follow',
    }

    html = template
    for k, v in replacements.items():
        html = html.replace(k, v)

    return html

def build_article_index(articles, tools_map):
    """Generate articles/index.html — article listing page"""
    article_ids = {a["id"] for a in articles}
    articles = [a for a in articles if a["id"] in REVIEW_INDEXED_ARTICLE_IDS]
    articles += [a for a in EXTRA_REVIEW_ARTICLES if a["id"] not in article_ids]
    type_filter_js = '''
    <div class="article-filter" style="max-width:800px;margin:0 auto 24px;display:flex;gap:8px;flex-wrap:wrap;">
      <button class="af-btn active" data-type="all">全部</button>
      <button class="af-btn" data-type="comparison">横向对比</button>
      <button class="af-btn" data-type="recommendation">场景推荐</button>
      <button class="af-btn" data-type="pricing">价格指南</button>
    </div>
    <style>
    .af-btn { padding:6px 14px; border-radius:20px; font-size:12px; border:1px solid var(--card-border); background:var(--card-bg); color:var(--text-secondary); cursor:pointer; transition:all 0.2s; }
    .af-btn:hover { border-color:var(--accent-start); color:var(--accent-start); }
    .af-btn.active { background:linear-gradient(135deg,var(--accent-start),var(--accent-end)); color:#fff; border-color:transparent; }
    </style>
    <script>
    document.addEventListener('DOMContentLoaded', function(){
      const cards = document.querySelectorAll('.article-card');
      const counts = { all: cards.length };
      cards.forEach(c => { const t = c.dataset.type; counts[t] = (counts[t]||0)+1; });
      document.querySelectorAll('.af-btn').forEach(btn => {
        const t = btn.dataset.type;
        const n = counts[t]||0;
        btn.textContent += ' (' + n + ')';
        btn.addEventListener('click', () => {
          document.querySelectorAll('.af-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          document.querySelectorAll('.article-card').forEach(card => {
            card.style.display = (t==='all' || card.dataset.type===t) ? '' : 'none';
          });
        });
      });
    });
    </script>'''

    cards = ''
    for a in articles:
        cards += (
            f'<a href="/articles/{a["id"]}.html" class="article-card" data-type="{a["type"]}">'
            f'<span class="article-badge type-{a["type"]}">{type_label(a["type"])}</span>'
            f'<div class="article-title">{a["title"]}</div>'
            f'<div class="article-meta">{a.get("reading_time","")} &middot; {a.get("published","")}</div>'
            f'</a>'
        )

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="google-site-verification" content="VpHmBjp4J_z2x-rAtb7swV1jeCyoCpOuCQbC9Yfrkgw" />
<link rel="icon" type="image/svg+xml" href="/logo.svg">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NQTV1YBBLK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag("js", new Date());
  gtag("config", "G-NQTV1YBBLK");
</script>
<title>AI工具推荐文章 | AI ToolNav</title>
<meta name="description" content="AI ToolNav精选文章，涵盖AI工具对比、场景推荐和价格指南，帮你找到最合适的AI工具。">
<link rel="canonical" href="{DOMAIN}/articles/">
<meta name="robots" content="index, follow">
<style>
:root {{
  --bg: #0a0a1a; --card-bg: rgba(255,255,255,0.06); --card-border: rgba(255,255,255,0.10);
  --text-primary: #e2e8f0; --text-secondary: #94a3b8; --text-muted: #64748b;
  --accent-start: #818cf8; --accent-end: #a78bfa;
  --glow-1: rgba(168,85,247,0.30); --glow-2: rgba(59,130,246,0.25); --glow-3: rgba(6,182,212,0.20);
  --tag-bg: rgba(255,255,255,0.08); --radius: 14px; --shadow-sm: 0 2px 8px rgba(0,0,0,0.2);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.3); --shadow-lg: 0 8px 30px rgba(0,0,0,0.4);
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif; background: var(--bg); color: var(--text-primary); line-height: 1.6; position:relative; z-index:0; }}
body::before {{ content:''; position:fixed; inset:0; z-index:0; pointer-events:none; background:radial-gradient(circle at 20% 40%, var(--glow-1) 0%, transparent 50%), radial-gradient(circle at 70% 15%, var(--glow-2) 0%, transparent 50%), radial-gradient(circle at 85% 80%, var(--glow-3) 0%, transparent 50%); filter:blur(60px); animation:meshDrift 16s ease-in-out infinite alternate; }}
@media (prefers-reduced-motion:reduce){{ body::before {{ animation:none; }} }}
@keyframes meshDrift {{ 0% {{ transform:translate(0,0) scale(1); }} 50% {{ opacity:0.8; }} 100% {{ transform:translate(-3%,2%) scale(1.08); }} }}
.header {{ background:rgba(10,10,26,0.85); backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); border-bottom:1px solid var(--card-border); position:sticky; top:0; z-index:100; }}
.header-inner {{ max-width:1200px; margin:0 auto; padding:0 24px; height:56px; display:flex; align-items:center; justify-content:space-between; }}
.logo {{ font-size:20px; font-weight:700; color:var(--text-primary); text-decoration:none; }}
.nav {{ display:flex; gap:20px; }}
.nav a {{ font-size:13px; color:var(--text-secondary); text-decoration:none; }}
.nav a:hover {{ color:var(--accent-start); }}
.main {{ max-width:800px; margin:0 auto; padding:24px; position:relative; z-index:1; }}
.page-title {{ font-size:28px; font-weight:800; margin-bottom:8px; color:var(--text-primary); }}
.page-desc {{ font-size:13px; color:var(--text-muted); margin-bottom:24px; }}
.type-comparison {{ background:rgba(139,92,246,0.2); color:#c4b5fd; }}
.type-recommendation {{ background:rgba(59,130,246,0.2); color:#93c5fd; }}
.type-pricing {{ background:rgba(251,191,36,0.2); color:#fde68a; }}
.article-type {{ display:inline-block; padding:4px 14px; border-radius:20px; font-size:12px; font-weight:600; }}
.footer {{ text-align:center; padding:32px 24px; border-top:1px solid var(--card-border); margin-top:40px; position:relative; z-index:1; }}
.footer p {{ font-size:11px; color:var(--text-muted); }}
.article-card {{ display:block; background:var(--card-bg); border:1px solid var(--card-border); border-radius:14px; padding:22px 24px; text-decoration:none; color:var(--text-primary); transition:all 0.2s; margin-bottom:16px; backdrop-filter:blur(8px); }}
.article-card:hover {{ transform:translateY(-1px); box-shadow:0 4px 16px rgba(129,140,248,0.2); border-color:var(--accent-start); background:rgba(255,255,255,0.1); }}
.article-badge {{ display:inline-block; padding:4px 14px; border-radius:20px; font-size:12px; font-weight:600; margin-bottom:10px; }}
.article-title {{ font-size:16px; font-weight:600; color:var(--text-primary); margin:8px 0 6px; line-height:1.4; }}
.article-meta {{ font-size:12px; color:var(--text-muted); }}
.editor-note {{ max-width:800px; margin:0 auto 28px; background:rgba(129,140,248,0.08); border:1px solid var(--card-border); border-left:5px solid var(--accent-start); border-radius:14px; padding:22px 24px; backdrop-filter:blur(8px); }}
.editor-note h2 {{ font-size:17px; margin-bottom:10px; color:var(--text-primary); }}
.editor-note p {{ font-size:14px; color:var(--text-secondary); margin-bottom:12px; line-height:1.8; }}
.editor-note ul {{ padding-left:20px; margin:8px 0 0; }}
.editor-note li {{ font-size:13px; color:var(--text-secondary); margin-bottom:6px; }}

</style>
</head>
<body>
<header class="header">
  <div class="header-inner">
    <a href="/" class="logo">AI ToolNav</a>
    <nav class="nav">
      <a href="/">首页</a>
      <a href="/articles/">文章</a>
      <a href="/compare/">对比</a>
    </nav>
  </div>
</header>
<main class="main">
  <h1 class="page-title">📝 AI工具精选文章</h1>
  <p class="page-desc">复审阶段仅展示少量经过整理的深度文章，重点保留有实测、来源和明确适用边界的内容。</p>
  <section class="editor-note">
    <h2>为什么这里只保留少数文章</h2>
    <p>AI ToolNav 过去收录了大量工具清单和横向对比，但 AdSense 审核更看重页面是否有独特价值，而不是数量。当前我们把文章列表收缩为少数更完整的指南，优先展示安装教程、编程工具选择、学术研究流程、提示词方法和 DeepSeek 上手说明。</p>
    <p>每篇保留文章都会尽量说明三件事：适合什么人、哪些场景不适合、哪些信息需要回到官方文档或实际操作中核验。工具价格、免费额度、模型能力和地区可用性变化很快，文章结论会定期复查，正式订阅或用于工作前请以工具官网说明为准。</p>
    <ul>
      <li>保留：有实测流程、限制说明、来源提示的深度文章。</li>
      <li>暂缓：模板化明显、正文偏短、只做简单罗列的旧文章。</li>
      <li>后续：旧文章会逐篇重写，达到质量标准后再恢复索引。</li>
    </ul>
  </section>
  {type_filter_js}
  <div class="article-list" style="max-width:800px;margin:0 auto;">{cards}</div>
</main>
<footer class="footer">
  <p>&copy; 2026 AI ToolNav &middot; <a href="/privacy.html" style="color:var(--accent-start);text-decoration:none;">隐私政策</a> &middot; <a href="/terms.html" style="color:var(--accent-start);text-decoration:none;">服务条款</a> &middot; <a href="/about.html" style="color:var(--accent-start);text-decoration:none;">关于我们</a></p>
</footer>
</body>
</html>'''
    return html

def build_sitemap(articles):
    urls = [f'{DOMAIN}/', f'{DOMAIN}/articles/', f'{DOMAIN}/privacy.html', f'{DOMAIN}/terms.html', f'{DOMAIN}/about.html']
    article_ids = set()
    for a in articles:
        if a["id"] in REVIEW_INDEXED_ARTICLE_IDS:
            article_ids.add(a["id"])
            urls.append(f'{DOMAIN}/articles/{a["id"]}.html')
    for slug in sorted(REVIEW_INDEXED_ARTICLE_IDS - article_ids):
        if os.path.exists(os.path.join(BASE, "articles", f"{slug}.html")):
            urls.append(f"{DOMAIN}/articles/{slug}.html")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml += f'  <url><loc>{u}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
    xml += '</urlset>'
    return xml

def build_compare_page(tools_data):
    """Generate compare/index.html with embedded tools data"""
    tools_json = json.dumps(tools_data, ensure_ascii=False, separators=(',', ':'))

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="google-site-verification" content="VpHmBjp4J_z2x-rAtb7swV1jeCyoCpOuCQbC9Yfrkgw" />
<link rel="icon" type="image/svg+xml" href="/logo.svg">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NQTV1YBBLK"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag("js", new Date());
  gtag("config", "G-NQTV1YBBLK");
</script>
<title>AI工具对比 | AI ToolNav</title>
<meta name="description" content="选择2-4个AI工具进行横向对比，涵盖评分、价格、功能、优缺点等维度，帮你做出最佳选择。">
<link rel="canonical" href="{DOMAIN}/compare/">
<meta name="robots" content="noindex, follow">
<style>
:root {{
  --bg: #0a0a1a; --card-bg: rgba(255,255,255,0.06); --card-border: rgba(255,255,255,0.10);
  --text-primary: #e2e8f0; --text-secondary: #94a3b8; --text-muted: #64748b;
  --accent-start: #818cf8; --accent-end: #a78bfa;
  --glow-1: rgba(168,85,247,0.30); --glow-2: rgba(59,130,246,0.25); --glow-3: rgba(6,182,212,0.20);
  --tag-bg: rgba(255,255,255,0.08); --ad-bg-start: rgba(251,191,36,0.15); --ad-bg-end: rgba(245,158,11,0.10);
  --ad-border: rgba(251,191,36,0.3); --star-color: #fbbf24; --radius: 14px;
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.2); --shadow-md: 0 4px 16px rgba(0,0,0,0.3);
  --shadow-lg: 0 8px 30px rgba(0,0,0,0.4);
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif; background: var(--bg); color: var(--text-primary); line-height: 1.6; position:relative; z-index:0; }}
body::before {{ content:''; position:fixed; inset:0; z-index:0; pointer-events:none; background:radial-gradient(circle at 20% 40%, var(--glow-1) 0%, transparent 50%), radial-gradient(circle at 70% 15%, var(--glow-2) 0%, transparent 50%), radial-gradient(circle at 85% 80%, var(--glow-3) 0%, transparent 50%); filter:blur(60px); animation:meshDrift 16s ease-in-out infinite alternate; }}
@media (prefers-reduced-motion:reduce){{ body::before {{ animation:none; }} }}
@keyframes meshDrift {{ 0% {{ transform:translate(0,0) scale(1); }} 50% {{ opacity:0.8; }} 100% {{ transform:translate(-3%,2%) scale(1.08); }} }}
.header {{ background:rgba(10,10,26,0.85); backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); border-bottom:1px solid var(--card-border); position:sticky; top:0; z-index:100; }}
.header-inner {{ max-width:1200px; margin:0 auto; padding:0 24px; height:56px; display:flex; align-items:center; justify-content:space-between; }}
.logo {{ font-size:20px; font-weight:700; color:var(--text-primary); text-decoration:none; }}
.nav {{ display:flex; gap:20px; }}
.nav a {{ font-size:13px; color:var(--text-secondary); text-decoration:none; }}
.nav a:hover {{ color:var(--accent-start); }}
.main {{ max-width:1200px; margin:0 auto; padding:24px; position:relative; z-index:1; }}
.page-title {{ font-size:28px; font-weight:800; margin-bottom:8px; color:var(--text-primary); }}
.page-desc {{ font-size:13px; color:var(--text-muted); margin-bottom:24px; }}
.selected-bar {{ background:rgba(129,140,248,0.08); border-radius:var(--radius); padding:16px 24px; margin-bottom:24px; display:none; align-items:center; gap:12px; backdrop-filter:blur(8px); border:1px solid var(--card-border); }}
.selected-bar.show {{ display:flex; }}
.selected-bar .sel-tools {{ flex:1; display:flex; gap:8px; flex-wrap:wrap; }}
.selected-bar .sel-tag {{ background:linear-gradient(135deg,var(--accent-start),var(--accent-end)); color:#fff; padding:4px 12px; border-radius:16px; font-size:12px; display:flex; align-items:center; gap:4px; }}
.selected-bar .sel-tag .remove {{ cursor:pointer; font-weight:bold; }}
.btn-compare {{ padding:8px 24px; border-radius:20px; background:linear-gradient(135deg,var(--accent-start),var(--accent-end)); color:#fff; border:none; font-size:13px; font-weight:600; cursor:pointer; text-decoration:none; display:inline-block; }}
.btn-compare:disabled {{ opacity:0.4; cursor:not-allowed; }}
.cat-section {{ margin-bottom:32px; }}
.cat-title {{ font-size:18px; font-weight:700; margin-bottom:12px; color:var(--text-primary); }}
.tool-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(180px, 1fr)); gap:8px; }}
.tool-check {{ background:var(--card-bg); border:2px solid var(--card-border); border-radius:10px; padding:12px; cursor:pointer; transition:all 0.2s; display:flex; align-items:center; gap:8px; user-select:none; backdrop-filter:blur(8px); }}
.tool-check:hover {{ border-color:var(--accent-start); }}
.tool-check.selected {{ border-color:var(--accent-start); background:rgba(129,140,248,0.15); }}
.tool-check .tc-checkbox {{ width:18px; height:18px; border:2px solid var(--card-border); border-radius:4px; display:flex; align-items:center; justify-content:center; font-size:12px; flex-shrink:0; transition:all 0.2s; }}
.tool-check.selected .tc-checkbox {{ background:var(--accent-start); border-color:var(--accent-start); color:#fff; }}
.tool-check .tc-name {{ font-size:13px; font-weight:600; color:var(--text-primary); }}
.tool-check .tc-rating {{ font-size:10px; color:var(--star-color); margin-left:auto; }}
.quick-compare {{ margin-bottom:32px; }}
.quick-compare h3 {{ font-size:16px; margin-bottom:12px; color:var(--text-primary); }}
.qc-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(220px, 1fr)); gap:8px; }}
.qc-card {{ background:var(--card-bg); border:1px solid var(--card-border); border-radius:10px; padding:14px; text-decoration:none; color:inherit; transition:all 0.2s; backdrop-filter:blur(8px); }}
.qc-card:hover {{ border-color:var(--accent-start); box-shadow:var(--shadow-sm); background:rgba(255,255,255,0.1); }}
.qc-card .qc-title {{ font-size:13px; font-weight:600; color:var(--text-primary); }}
.qc-card .qc-tools {{ font-size:11px; color:var(--text-muted); margin-top:4px; }}
.footer {{ text-align:center; padding:32px 24px; border-top:1px solid var(--card-border); margin-top:40px; }}
.footer p {{ font-size:11px; color:var(--text-muted); }}
</style>
</head>
<body>
<header class="header">
  <div class="header-inner">
    <a href="/" class="logo">AI ToolNav</a>
    <nav class="nav">
      <a href="/">首页</a>
      <a href="/articles/">文章</a>
      <a href="/compare/">对比</a>
    </nav>
  </div>
</header>
<main class="main">
  <h1 class="page-title">🔬 AI工具对比</h1>
  <p class="page-desc">勾选2-4个你想对比的工具，查看它们在评分、价格、功能、优缺点等维度的横向对比</p>

  <div class="selected-bar" id="selectedBar">
    <span style="font-size:13px;color:var(--text-secondary);white-space:nowrap;">已选 <span id="selCount">0</span>/4：</span>
    <div class="sel-tools" id="selTools"></div>
    <button class="btn-compare" id="btnCompare" disabled onclick="doCompare()">开始对比</button>
  </div>

  <div class="quick-compare">
    <h3>🔥 热门对比</h3>
    <div class="qc-grid" id="hotCompares"></div>
  </div>

  <div id="toolSections"></div>
</main>
<footer class="footer">
  <p>&copy; 2026 AI ToolNav &middot; <a href="/privacy.html" style="color:var(--accent-start);text-decoration:none;">隐私政策</a> &middot; <a href="/terms.html" style="color:var(--accent-start);text-decoration:none;">服务条款</a> &middot; <a href="/about.html" style="color:var(--accent-start);text-decoration:none;">关于我们</a></p>
</footer>

<script>
const TOOLS_DATA = {tools_json};

let selected = [];

function init() {{
  const hotCompares = [
    {{ title: 'ChatGPT vs Claude vs Gemini', tools: ['ChatGPT','Claude','Gemini'], link: '/articles/chatgpt-vs-claude-vs-gemini.html' }},
    {{ title: 'GitHub Copilot vs Cursor vs Windsurf', tools: ['GitHub Copilot','Cursor','Windsurf'], link: '/articles/github-copilot-vs-cursor-vs-windsurf.html' }},
    {{ title: 'Midjourney vs DALL·E 3 vs SD', tools: ['Midjourney','DALL·E 3','Stable Diffusion'], link: '/articles/midjourney-vs-dalle-vs-sd.html' }},
    {{ title: 'DeepSeek vs ChatGPT', tools: ['DeepSeek','ChatGPT'], link: '/articles/deepseek-vs-chatgpt.html' }},
    {{ title: 'Sora vs Runway vs Pika', tools: ['Sora','Runway','Pika'], link: '/articles/sora-vs-runway-vs-pika.html' }},
    {{ title: 'Suno vs ElevenLabs', tools: ['Suno','ElevenLabs'], link: '/articles/suno-vs-elevenlabs.html' }},
  ];
  document.getElementById('hotCompares').innerHTML = hotCompares.map(h =>
    `<a href="${{h.link}}" class="qc-card">
      <div class="qc-title">${{h.title}}</div>
      <div class="qc-tools">${{h.tools.join(' · ')}}</div>
    </a>`
  ).join('');

  const cats = {{}};
  TOOLS_DATA.tools.forEach(t => {{
    if (!cats[t.category]) cats[t.category] = [];
    cats[t.category].push(t);
  }});
  const catNames = {{ llm:'🤖 大语言模型', image:'🎨 AI绘画', code:'💻 AI编程', video:'🎬 AI视频', writing:'✍️ AI写作', audio:'🎵 AI音频', office:'📊 AI办公', platform:'🔧 开发平台' }};

  document.getElementById('toolSections').innerHTML = TOOLS_DATA.categories.map(cat => {{
    const tools = cats[cat.id] || [];
    return `<div class="cat-section">
      <div class="cat-title">${{catNames[cat.id] || cat.name}}</div>
      <div class="tool-grid">${{tools.map(t =>
        `<div class="tool-check" data-id="${{t.id}}" onclick="toggleTool(this, '${{t.id}}')">
          <div class="tc-checkbox">✓</div>
          <span class="tc-name">${{t.icon}} ${{t.name}}</span>
          <span class="tc-rating">${{'⭐'.repeat(t.rating)}}</span>
        </div>`
      ).join('')}}</div>
    </div>`;
  }}).join('');
}}

function toggleTool(el, id) {{
  if (el.classList.contains('selected')) {{
    el.classList.remove('selected');
    selected = selected.filter(s => s !== id);
  }} else {{
    if (selected.length >= 4) {{
      alert('最多选择4个工具进行对比');
      return;
    }}
    el.classList.add('selected');
    selected.push(id);
  }}
  updateBar();
}}

function updateBar() {{
  const bar = document.getElementById('selectedBar');
  const count = document.getElementById('selCount');
  const toolsDiv = document.getElementById('selTools');
  const btn = document.getElementById('btnCompare');

  count.textContent = selected.length;
  if (selected.length >= 2) {{
    bar.classList.add('show');
    btn.disabled = false;
  }} else {{
    bar.classList.remove('show');
    btn.disabled = true;
  }}

  toolsDiv.innerHTML = selected.map(id => {{
    const t = TOOLS_DATA.tools.find(t => t.id === id);
    return t ? `<span class="sel-tag">${{t.icon}} ${{t.name}} <span class="remove" onclick="event.stopPropagation();removeTool('${{id}}')">×</span></span>` : '';
  }}).join('');
}}

function removeTool(id) {{
  selected = selected.filter(s => s !== id);
  document.querySelectorAll('.tool-check').forEach(el => {{
    if (el.dataset.id === id) el.classList.remove('selected');
  }});
  updateBar();
}}

function doCompare() {{
  if (selected.length < 2) return;
  const sorted = selected.slice().sort();
  const compareArticles = {{
    'chatgpt,claude,gemini': '/articles/chatgpt-vs-claude-vs-gemini.html',
    'deepseek,chatgpt': '/articles/deepseek-vs-chatgpt.html',
    'claude,deepseek': '/articles/deepseek-vs-chatgpt.html',
    'kimi,tongyi': '/articles/kimi-vs-tongyi.html',
    'dalle3,midjourney,stable-diffusion': '/articles/midjourney-vs-dalle-vs-sd.html',
    'cursor,github-copilot,windsurf': '/articles/github-copilot-vs-cursor-vs-windsurf.html',
    'pika,runway,sora': '/articles/sora-vs-runway-vs-pika.html',
    'elevenlabs,suno': '/articles/suno-vs-elevenlabs.html',
  }};
  const key = sorted.join(',');
  if (compareArticles[key]) {{
    window.location.href = compareArticles[key];
  }} else {{
    alert('该组合暂无专属对比文章，请浏览 /articles/ 查看相关对比内容。');
  }}
}}

init();
</script>
</body>
</html>'''
    return html

def main():
    tools_data = load_json('data/tools.json')
    articles = load_json('data/articles.json')

    tools_map = {t['id']: t for t in tools_data['tools']}
    articles_map = {a['id']: a for a in articles}

    # Generate each article
    for article in articles:
        if article["id"] in STATIC_REVIEW_ARTICLE_IDS:
            print(f'  SKIP static article articles/{article["id"]}.html')
            continue
        html = render_article(article, tools_map, articles_map)
        write_html(f'articles/{article["id"]}.html', html)
        print(f'  OK articles/{article["id"]}.html')

    # Generate article index
    index_html = build_article_index(articles, tools_map)
    write_html('articles/index.html', index_html)
    print('  OK articles/index.html')

    # Generate compare selection page
    compare_html = build_compare_page(tools_data)
    write_html('compare/index.html', compare_html)
    print('  OK compare/index.html')

    # Generate sitemap
    sitemap = build_sitemap(articles)
    write_html('sitemap.xml', sitemap)
    print('  OK sitemap.xml')

    print(f'\nDone! Generated {len(articles)} articles + index + compare + sitemap.')

if __name__ == '__main__':
    main()
