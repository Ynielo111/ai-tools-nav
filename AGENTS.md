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

## 注意事项
- 纯静态 HTML 网站，所有页面直接编辑 HTML
- 文章日期要分散到不同日期，不要集中同一天
- 工具页需要深度内容（800+字）、真实logo、适用场景
- 链接使用 affiliate.js 集中管理，不要在文章里直接写推广链接
- 所有页面不需要 no-cache meta 标签
- 新工具页参考 template/ 下的模板创建
- 新文章参考 articles/ 下已有文章的格式
- 修改完内容后，主动提醒用户是否需要部署
