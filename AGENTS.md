# AI ToolNav - AI 工具导航网站

## 仓库信息
- GitHub: git@github.com:Ynielo111/ai-tools-nav.git
- 分支: main
- 托管: Vercel（GitHub 集成，main 分支自动部署）
- 域名: aitnav.com

## 一键部署
当用户说"部署""推送""上线""发布""deploy"时，直接执行以下完整链路，不需要等用户单独确认：

```bash
git add .
git commit -m "更新网站内容"
git push origin main
```

推送后 Vercel 自动发布，约 1 分钟生效。

## 项目结构
- index.html — 首页
- articles/ — 63篇原创文章
- tools/ — 48个工具详情页
- categories/ — 8个分类页
- compare/ — 工具对比页
- js/affiliate.js — 集中式推广链接管理
- template/article.html — 文章模板
- scripts/build.py — 静态页面生成器

## 环境备注
- 本机 Git 路径：`C:\Program Files\Git\cmd\git.exe`（部分 AI 工具环境需完整路径）

## AdSense 索引策略（2026-06-22 更新）

当前 AdSense 后台明确提示“低价值内容”。复审前采用更保守的过审优先策略：减少 Google 审核时看到的模板化页面，只保留少数更有实测和编辑价值的文章。

### 纳入索引 + 投放 AdSense 的文章（7 篇）
`ai-cli-tools-setup-guide` `open-source-ai-coding-assistants` `codex-vs-claude-code-vs-gemini-cli` `chatgpt-prompt-guide` `deepseek-complete-guide` `best-ai-coding-tools` `academic-research-ai`

### 索引但不放 AdSense 的页面
`index.html` `articles/index.html` `about.html` `privacy.html` `terms.html`

### 全部 noindex（后续扩充内容后可恢复索引）
- 模板化明显或正文偏短的文章暂时 noindex，尤其是多数横向对比、价格清单、泛推荐页
- `tools/*`（全部 48 个工具页 + tools/index.html）
- `categories/*`（全部 8 个分类页）
- `compare/` `reports/` `workflows/`

### 技术要点
- 域名统一使用 `https://www.aitnav.com`（canonical、sitemap、og、结构化数据）
- 首页 splash 遮罩已移除
- AdSense 只在上述 7 篇文章中加载
- sitemap.xml 只包含索引页面
- robots.txt 指向 `https://www.aitnav.com/sitemap.xml`
- 审计脚本：`scripts/audit_adsense.ps1`
- 低价值内容审计脚本：`scripts/audit_low_value.ps1`

### ⚠️ 与原始设计的分歧
设计文档原计划保留 5 个核心工具页（chatgpt/claude/cursor/midjourney/deepseek）索引，但第二次提交"Reduce low-value AdSense inventory"将其全部设为 noindex。如需恢复，将这 5 个工具页的 robots meta 改回 `index, follow` 并加入 sitemap。

### 重新生成命令
修改 `data/articles.json` 或 `data/tools.json` 后，运行 `python scripts/build.py` 重新生成页面和 sitemap。

## 注意事项
- 纯静态 HTML 网站，所有页面直接编辑 HTML
- 文章日期要分散到不同日期，不要集中同一天
- 工具页需要深度内容（800+字）、真实logo、适用场景
- 链接使用 affiliate.js 集中管理，不要在文章里直接写推广链接
- 所有页面不需要 no-cache meta 标签
- 新工具页参考 template/ 下的模板创建
- 新文章参考 articles/ 下已有文章的格式
- 修改完内容后，主动提醒用户是否需要部署
