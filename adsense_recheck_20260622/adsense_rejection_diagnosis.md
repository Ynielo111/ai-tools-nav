# AI ToolNav AdSense 拒审排查记录

排查日期：2026-06-22

## 结论

目前看，拒审主因不像是 AdSense 技术接入错误。更可能的风险点是：部分收录文章模板化痕迹明显、原创/实测证据不足、内容差异度不够，容易被归入“低价值内容”或“网站暂未准备好”的审核判断。

2026-06-22 追加确认：用户提供的 AdSense 后台截图显示 `aitnav.com` 的状态详情为“低价值内容”。因此本轮修复按“过审优先模式”处理：减少 indexed 页面数量，只保留少数更完整、更有实测和来源说明的文章，其余模板化文章暂时 noindex。

## 已验证通过的技术项

本地审计结果：

- 扫描 HTML 页面：138 个
- indexed 页面：23 个
- noindex 页面：115 个
- AdSense 本地审计：通过

线上审计结果：

- `https://www.aitnav.com/`：200，可访问
- `robots.txt`：200，指向 `https://www.aitnav.com/sitemap.xml`
- `sitemap.xml`：200，共 23 个 URL
- `ads.txt`：200，包含 `google.com, pub-6233913596766498, DIRECT, f08c47fec0942fa0`
- sitemap 内页面：全部 200
- sitemap 内页面：无 noindex 混入
- sitemap 内页面：无 canonical 缺失
- sitemap 内页面：无非 www canonical
- sitemap 内文章页：未发现 AdSense 脚本缺失
- sitemap 内非隐私/条款页面：未发现正文少于 1000 字符的页面

## 内容质量风险

抽查 18 篇 AdSense 审核文章后，发现部分页面存在明显重复句式：

| 文章 | 正文长度 | 模板化短语命中 |
| --- | ---: | ---: |
| academic-research-ai | 2312 | 12 |
| best-ai-coding-tools | 2525 | 11 |
| deepseek-vs-chatgpt | 2442 | 8 |
| chatgpt-vs-claude-vs-gemini | 2943 | 8 |
| github-copilot-vs-cursor-vs-windsurf | 2118 | 4 |
| ai-tools-pricing-2026 | 2294 | 4 |
| notion-vs-feishu-vs-copilot | 2172 | 4 |
| midjourney-vs-dalle-vs-sd | 2283 | 4 |

典型重复句包括：

- “以上推荐的工具各有侧重……建议根据自己的具体需求……”
- “上表从多个关键维度进行了直观对比……”
- “选对工具只是第一步……”

这类表述对读者未必没用，但在审核视角里会显得像批量生成内容。AdSense 审核更看重网站是否有足够独特、原创、有实际价值的内容。

## 建议修复顺序

第一步：请先提供 AdSense 后台拒审原文或截图，尤其是“网站需要注意”“低价值内容”“政策违规”“无法访问网站”等具体分类。没有这个信息，只能做概率判断。

第二步：优先重写 4 篇风险最高的收录文章：

- `articles/academic-research-ai.html`
- `articles/best-ai-coding-tools.html`
- `articles/deepseek-vs-chatgpt.html`
- `articles/chatgpt-vs-claude-vs-gemini.html`

重写方向：

- 删除模板化套话
- 增加真实使用场景、选择标准、限制条件
- 给出可执行判断，例如“预算多少选哪个”“学生/研究生/程序员分别怎么选”
- 增加来源说明或实测说明
- 少用空泛最高级，例如“最好”“神器”“最强”

第三步：暂时不要扩大广告覆盖。保持现在的 18 篇文章策略，等核心内容质量提升后再复审。

第四步：复审前重新跑：

- 本地 `scripts/audit_adsense.ps1`
- 线上 sitemap 抽查
- Google Search Console 里的覆盖率/索引状态检查

## 需要用户补充的信息

请贴出 AdSense 后台本次拒审的原文，最好包含：

- 拒审原因标题
- 详细说明
- 是否显示具体违规页面
- 提交审核的日期

拿到这段文字后，可以把修改范围从“猜测型优化”收敛到“针对性修复”。

## 2026-06-22 实际修复

本轮已完成以下调整：

- 新增 `scripts/audit_low_value.ps1`，用于检查 indexed 文章的低价值内容信号。
- 将 AdSense 审核文章从 18 篇收缩为 7 篇。
- 同步更新 `scripts/build.py`、`scripts/audit_adsense.ps1` 和 `AGENTS.md`。
- 重写并增强以下生成文章：
  - `articles/academic-research-ai.html`
  - `articles/best-ai-coding-tools.html`
  - `articles/deepseek-complete-guide.html`
  - `articles/chatgpt-prompt-guide.html`
- 增强 `articles/index.html`，增加编辑说明、选文标准和低价值内容整改说明。
- 重新生成 `articles/*.html`、`articles/index.html`、`compare/index.html` 和 `sitemap.xml`。

当前 sitemap 只包含 12 个 URL：

- 首页
- 文章列表页
- `privacy.html`
- `terms.html`
- `about.html`
- `ai-cli-tools-setup-guide`
- `best-ai-coding-tools`
- `academic-research-ai`
- `chatgpt-prompt-guide`
- `deepseek-complete-guide`
- `codex-vs-claude-code-vs-gemini-cli`
- `open-source-ai-coding-assistants`

验证结果：

- `scripts/audit_adsense.ps1`：通过
- `scripts/audit_low_value.ps1`：通过

复审建议：

1. 部署到线上后，先确认线上 `sitemap.xml` 已变为 12 个 URL。
2. 在 Google Search Console 重新提交 sitemap，并等待 Google 重新抓取。
3. 确认 AdSense 后台 `ads.txt` 仍为“已授权”。
4. 再点击 AdSense 里的“申请审核”。

