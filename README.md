# AI ToolNav — AI 工具导航

收录全品类 AI 工具的导航网站，支持按分类浏览、关键词搜索，内嵌广告位。

## 本地运行

双击 `index.html` 即可在浏览器中打开，无需安装任何东西。

## 添加/修改工具

打开 `index.html`，找到 `DATA` 对象（约第 80 行），在 `tools` 数组中增删改条目：

```js
{
  name: "工具名称",
  description: "简短描述，20字以内",
  url: "https://...",
  category: "llm",       // 见下方分类ID
  icon: "🤖",             // 一个 emoji 作为图标
  tags: ["标签1", "标签2"]
}
```

可用分类 ID：`llm` `image` `code` `video` `writing` `audio` `office` `platform`

## 修改广告

编辑 `DATA` 对象中的 `ads` 数组，每条广告：`{ title, description, link }`。

## 部署到 Vercel

1. 将 `ai-tools-nav` 文件夹推送到 GitHub 仓库
2. 在 Vercel 中导入该仓库
3. Vercel 自动识别为静态站点，无需额外配置
