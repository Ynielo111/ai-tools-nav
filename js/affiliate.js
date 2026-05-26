/**
 * AI ToolNav — 集中式 Affiliate 链接管理
 *
 * 用法：在每篇文章的 </body> 前引入
 *   <script src="/js/affiliate.js"></script>
 *
 * 新增工具：在 AFF_DOMAINS 里加一条即可，全站62篇文章自动生效
 * 关闭变现：删掉这个文件的引用，所有链接恢复原状
 *
 * 最后更新：2026-05-26
 */

(function () {
  'use strict';

  // ============================================================
  // 一、Affiliate 链接映射表
  // key   → 域名匹配规则（支持完整域名或路径前缀）
  // value → 替换后的 URL，{original} 会自动替换为原始链接
  // ============================================================

  var AFF_DOMAINS = {

    // ── AI 编程工具 ──────────────────────────────

    // ── AI 聊天机器人 ─────────────────────────

    'robofy.ai': {
      url: 'https://www.robofy.ai/?ref=yang',
      note: 'Robofy AI 聊天机器人 → 30% 长期分成'
    }

    // ── 暂时无法 Affiliate 的工具（保留以备将来） ──
    //
    // chat.openai.com    → OpenAI 无官方 affiliate；建议引导到 API 代理
    // claude.ai          → Anthropic 无官方 affiliate；建议引导到 API 代理
    // gemini.google.com  → Google 无 affiliate
    // midjourney.com     → 无 affiliate
    // github.com/features/copilot → 无 affiliate
    // deepseek.com       → 国产，无 affiliate
    // kimi.moonshot.cn   → 国产，无 affiliate
    // tongyi.aliyun.com  → 国产，无 affiliate
    //
    // 策略：这些工具的链接先不动，保持纯推荐。等你自己做了 API 代理
    // 或找到了合适的国内替代服务后再替换。
  };

  // ============================================================
  // 二、核心替换逻辑（不要改）
  // ============================================================

  function matchDomain(href, domain) {
    // 从完整 URL 中提取 hostname+path 前缀做精确匹配
    var a = document.createElement('a');
    a.href = href;
    var host = (a.hostname || '').replace(/^www\./, '');   // 去掉 www.
    var full = host + a.pathname.replace(/\/+$/, '');       // hostname + path，去末尾斜杠

    // 匹配规则：域名完全命中，或 host+path 前缀命中
    if (host === domain) return true;
    if (full.indexOf(domain) === 0) return true;
    return false;
  }

  function replaceLinks() {
    var links = document.querySelectorAll('a[href^="http"]');
    var replaced = 0;

    for (var i = 0; i < links.length; i++) {
      var link = links[i];
      var href = link.getAttribute('href');
      if (!href) continue;

      // 跳过已有追踪参数的链接（避免重复替换）
      if (/[?&](ref|aff|affiliate|referrer|via|utm_)/i.test(href)) continue;

      // 遍历映射表
      var domains = Object.keys(AFF_DOMAINS);
      for (var j = 0; j < domains.length; j++) {
        var domain = domains[j];
        var cfg = AFF_DOMAINS[domain];

        if (matchDomain(href, domain)) {
          var newUrl = cfg.url;
          // 如果模板里有 {original}，替换为原始链接
          if (newUrl.indexOf('{original}') >= 0) {
            newUrl = newUrl.replace('{original}', encodeURIComponent(href));
          }
          link.setAttribute('href', newUrl);

          // 给链接加 sponsored 标签（SEO 最佳实践）
          var rel = link.getAttribute('rel') || '';
          if (rel.indexOf('sponsored') < 0) {
            link.setAttribute('rel', (rel + ' sponsored').trim());
          }

          replaced++;
          break;  // 一个链接只匹配一次
        }
      }
    }

    // 开发环境打印替换统计（上线后可注释掉）
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      console.log('[Affiliate] 已替换 ' + replaced + ' 条链接');
    }
  }

  // ============================================================
  // 三、执行
  // ============================================================

  // DOM 加载完成后替换
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', replaceLinks);
  } else {
    replaceLinks();
  }

})();
