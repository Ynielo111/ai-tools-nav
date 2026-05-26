# AI ToolNav 网站项目

## 部署方式
- 托管：Vercel（GitHub 集成，main 分支自动部署）
- 域名：aitnav.com
- 推送即部署：`git push origin main` 后 Vercel 自动发布，约1分钟生效

## 一键部署指令
用户说"部署"或"推送" = git add . + git commit + git push origin main
不需要等用户单独确认推送，直接执行完整链路。

## 项目结构
- index.html — 首页
- articles/ — 63篇原创文章
- tools/ — 48个工具详情页
- categories/ — 8个分类页
- js/affiliate.js — 集中式推广链接管理
- template/article.html — 文章模板
- build.py — 静态页面生成器

## 注意事项
- 文章日期不能全部集中同一天，需要分散到不同日期
- 工具页需要深度内容（800+字）、真实logo、适用场景
- 链接使用 affiliate.js 集中管理，不要在文章里直接写推广链接
- 所有页面已移除 no-cache meta 标签
